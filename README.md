# Encrypted + Locked + LineageOS 16.0 + MicroG on OnePlus 5T

I have a [OnePlus 5T](https://www.oneplus.com/support/spec/oneplus-5t). Interested in a modern Android device running MicroG and F-Droid, I decided to try to build this device. The problem with most Android hacks is that they require unlocked bootloaders. However, locked bootloaders provide some security guarantees, and I wanted to try to build a solid device with this software.

I specifically chose the OnePlus 5 and 5T because of [this XDA post](https://forum.xda-developers.com/oneplus-5/how-to/guide-relock-bootloader-custom-rom-t3849299) that showed a way to allow for a locked bootloader with a custom ROM. Many Android devices will not allow this. It helps that the OnePlus line is extremely overpowered for its release date, cheap used from Android enthusiasts, has extreme enthusiast support, and (hopefully) will have support for a long time because of these things.

The tutorial above requires you to disable [dm-verity](https://source.android.com/security/verifiedboot/dm-verity) or [disable forced encryption](https://source.android.com/security/encryption/full-disk). We want to keep as many security features as LineageOS and MicroG allow, so we aren't going to do that. (Also, LineageOS 16.0 has issues with forced encryption being off. Flashing Magisk, the disable dm-verity/forceencrypt, and then attempting to encrypt failed on my OnePlus 5T.)

## Known Issues

* Push notifications aren't working. It's likely a known problem in MicroG due to Google moving to FCM from GCM. [I have opened an issue](https://github.com/microg/android_packages_apps_GmsCore/issues/794).

## Known-good images

Due to GitHub size restrictions, I've placed the known-good images used for this on DigitalOcean. You may use these to test to make sure that you have done everything properly, however, **do not use these in production** as they are likely to be old/out-of-date. These are unmodified from the original sources I downloaded them from.

* [VerifiedBootSigner-V8.zip](https://rarecoil.sfo2.digitaloceanspaces.com/ecophone/dumpling/known-good/VerifiedBootSigner-v8.zip)
* [addonsu-16.0-arm64-signed.zip](https://rarecoil.sfo2.digitaloceanspaces.com/ecophone/dumpling/known-good/addonsu-16.0-arm64-signed.zip)
* [lineage-16.0-20190506-microG-dumpling.zip](https://rarecoil.sfo2.digitaloceanspaces.com/ecophone/dumpling/known-good/lineage-16.0-20190506-microG-dumpling.zip)


## Preparing signing keys, Verified Boot Signer, and Recovery

You will need to sign your recovery.img and your boot.img for the bootloader to be locked. If you don't have keys, run `gen-signing-keys.sh` that exists in this folder to generate RSA keys for the signing process.

**To generate keys,** run `gen-signing-keys.sh`. This will use openssl to generate keys.

**To update the boot signer ZIP**, run `update-boot-signer.sh`. This will add your generated key files to Chainfire's boot signer ZIP.

**To sign recovery**, run `sign-recovery.sh` with the argument being the TWRP recovery you want to sign.


## Wiping the device in TWRP

Open TWRP, and go to "Advanced Wipe". Completely wipe **Dalvik / ART Cache**, **Cache**, **System**, **Vendor**, and **data**. This gives us a no-OS-installed device. Now, we flash our work.

## Flashing

You can use `adb sideload` or MTP them to TWRP and install from there. I use ADB Sideload, so go to **Advanced > ADB Sideload** and swipe to start sideload. Then, from your computer, load the OS and the SU add-on. Then, flash with your custom VerifiedBootSigner containing your signing keys, and wipe cache at this stage as well just for good measure.

````
adb sideload lineage-16.0-20190506-microG-dumpling.zip
adb sideload addonsu-16.0-arm64-signed.zip 
adb sideload VerifiedBootSigner-v8.zip 
````

Reboot from TWRP **to the bootloader**, *not the system you have just flashed*, and lock the bootloader:

```
fastboot oem lock
```

The OnePlus will show that the "device has loaded a different operating system" and boot into TWRP recovery once. If you have a signature mismatch, you will see an error image that your device is corrupt. If so, re-sign your recovery, make sure your VerifiedBootSigner 1) contained your keys and 2) actually sideloaded, and then try again.

