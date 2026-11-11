#!/usr/bin/env python3
"""Inject a trailing DTB into an Android boot v1 image template."""

from __future__ import annotations

import argparse
import hashlib
import struct
from pathlib import Path

PAGE_SIZE = 2048
FDT_MAGIC = b"\xd0\x0d\xfe\xed"


def le32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def be32(buf: bytes, off: int) -> int:
    return struct.unpack_from(">I", buf, off)[0]


def trailing_dtb(blob: bytes) -> tuple[bytes, int]:
    pos = blob.rfind(FDT_MAGIC)
    while pos >= 0:
        if pos + 8 <= len(blob):
            size = be32(blob, pos + 4)
            if size >= 40 and pos + size == len(blob):
                return blob[pos:], pos
        pos = blob.rfind(FDT_MAGIC, 0, pos)
    raise ValueError("no trailing DTB found")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", type=Path, required=True)
    ap.add_argument("--kernel", type=Path, required=True)
    ap.add_argument("--dtb", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--kernel-output", type=Path, required=True)
    args = ap.parse_args()

    template = args.template.read_bytes()
    built = args.kernel.read_bytes()
    dtb = args.dtb.read_bytes()
    boot_size = len(template)

    if boot_size < PAGE_SIZE or template[:8] != b"ANDROID!":
        raise ValueError("template is not an Android boot image")
    if le32(template, 36) != PAGE_SIZE or le32(template, 40) != 1:
        raise ValueError("template must use Android boot v1 / 2048-byte pages")
    if dtb[:4] != FDT_MAGIC or be32(dtb, 4) != len(dtb):
        raise ValueError("invalid DTB")

    _, dtb_offset = trailing_dtb(built)
    kernel_gzip = built[:dtb_offset]
    if kernel_gzip[:2] != b"\x1f\x8b":
        raise ValueError("kernel prefix is not gzip")

    combined = kernel_gzip + dtb
    if PAGE_SIZE + len(combined) > boot_size:
        raise ValueError("kernel plus DTB does not fit in the boot image")

    out = bytearray(boot_size)
    out[:PAGE_SIZE] = template[:PAGE_SIZE]
    struct.pack_into("<I", out, 8, len(combined))
    out[PAGE_SIZE : PAGE_SIZE + len(combined)] = combined
    out[576:608] = hashlib.sha1(combined).digest() + bytes(12)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.kernel_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(out)
    args.kernel_output.write_bytes(combined)
    print(f"boot={args.output} bytes={len(out)} sha256={hashlib.sha256(out).hexdigest()}")
    print(f"kernel_payload={args.kernel_output} bytes={len(combined)} dtb={len(dtb)}")


if __name__ == "__main__":
    main()
