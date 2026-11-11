## Lazy Action Recovery Builder |TWRP / PBRP / OFRP / SHRP|
Compile your first custom recovery via Github Actions - with ldcheck setup. This workflow supports both TWRP or PBRP or OFRP or SHRP, you can use it with other custom recovery as well, but you have to modify the yaml config yourself.

# How to Use
1. Fork this repository.

2. Go to `Action` tab > `All workflows` > Pick which Build you need (`TWRP or PBRP or OFRP or SHRP`) > `Run workflow`, then pick required information from each drop-down list:
 * Manifest Branch (*12.1, *11.0, *10.0, *9.0, *8.1, *7.1, *6.0, etc.)
 * Device Tree (Your device tree repository link)
 * Device Tree Branch (Your device tree repository branch)
 * Device Name (Your device codename)
 * Device Path (device/brand/codename)
 * Build Target (boot, reecovery, vendorboot)
 * LDCHECK (path to your target binary file, ie. `system/bin/qseecomd`)
   - If you are building manually/locally and you want to use ldcheck for checking dependencies, visit [THIS](https://github.com/TeamWin/android_device_qcom_twrp-common/tree/android-11#using-ldcheck-to-find-dependencies) this for guide.
   
## Notes
   - Manifest 11.0 also supports Android 9 and Android 10 decryption.
   - This workflow supports Skyhawk Android 11 Recovery Branch v3.11.0 Now. Update the Skyhawk source yourself if you want A14 branch support.
   - `Prebuilt-TWRP` is the shared workflow for devices whose kernel is built elsewhere. It accepts a prebuilt Android boot image, optionally injects a device DTB, copies the resulting kernel payload into the device tree, and builds the requested recovery image.
   - Device-specific kernel variants and Wi-Fi configuration belong in the kernel repository; this builder remains device-agnostic.

## Credits
- https://github.com/CaptainThrowback
- https://github.com/azwhikaru
- https://github.com/cd-Crypton
- https://github.com/that1
- https://github.com/carlodandan
- And to all Contributors in every repositories and scripts I used.
