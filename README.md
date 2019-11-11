# Hardened OnePlus 5T (dumpling) LineageOS Build Pipeline

This repository contains a full build pipeline for LineageOS 15.1 (Oreo) on the OnePlus 5T. While Lineage's OnePlus support is great, LineageOS disables the [Android Verified Boot](https://source.android.com/security/verifiedboot/avb) system, which is actually supported by Dumpling. This Dockerised build environment is patched to enable AVB 1.0 on the OnePlus 5T, since the OnePlus allows for signing custom operating systems. This build pipeline also downloads TWRP updates and signs the recoveries with the same keys.

The OnePlus 5T is used because it is easy-to-buy older hardware that is enthusiast-oriented. By maintaining security updates and builds for the 5T yourself, you can keep a very capable device out of [dirty e-waste recycling](https://www.cawrecycles.org/background-on-e-waste) and hopefully continue to use it with security patches for years after it is no longer supported by OnePlus.

This repository will allow you to build your own images from the Lineage repositories, build OTA images, and sign all of it with your own release keys so you can relock the bootloader on the OnePlus and gain some better security guarantees. 

## Build Features

This repo is in active development and will change with more hardening fixes over time as I prove they are stable enough for this hardware. I will generally merge security + privacy fixes into this; if you wish to port features from [Graphene](https://grapheneos.org/) I will add them here. **Google Play Services or OpenGapps will not be supported officially by this pipeline at this time.**

* Signing keys you control - your build pipeline will generate signing keys specific to you
* Android Verified Boot 1.0 Support (signed recoveries and boot images)
* Full-disk encryption
* Mozilla + Nominatim backends
* [MicroG framework](https://microg.org/) instead of Google Play Services
* [FDroid](https://f-droid.org/) for FOSS applications

### Downloading apps from the Play Store

Since the Play Store is not included, you will need to use an alternative Google Play client to download the applications. The _Yalp Store_ and _Aurora Store_ applications in F-Droid allow installs from the Google Play store.


## System Requirements

You will need a system capable of building LineageOS. At the time of writing I would recommend:

* 16 GB RAM minimum
* NVMe with 200GB free space
* As many cores as you possibly can throw at it
* Ubuntu 18.04 LTS
* Docker from [Docker's official repositories](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

My development workstation is an Intel Core i5-8250U (4c/8t) with 32GB RAM and a 2TB NVMe disk. My personal build and OTA server is a dual-processor Intel Xeon E5-2650L v2 (20c/40t) with 160GB RAM. Initial builds on my workstation take about 3 hours; the Xeon server takes about half that time.

## Server Setup

Clone this repository to the location you want to store all your files. Being on SSD or a bcache-backed disk set will make the builds significantly faster.

Run `python install.py` from this repository. The installation script will download the Docker image and configure the scripts/patches required to enable the features above.

> **Advanced Users**: If you are running an OTA Server or want to make changes to the build process, modify `config.ini`.

## Initial Device Flashing

You will need `fastboot` and `adb` for initial device setup.

1. Boot into Fastboot mode.
1. Flash your signed recovery using `fastboot flash recovery your_signed_twrp_version.img`.
1. Boot from Fastboot into recovery by picking "Recovery mode" from the fastboot menu on the device.
1. In TWRP, check to wipe everything.
1. Go back, and choose _ADB Sideload_ from the _Advanced_ menu.
1. From your computer, `adb sideload lineage-your_version_here.zip`.
1. **Do not reboot.** Go back, and then to Reboot, and choose "Reboot Bootloader".
1. From Fastboot with the new device image and recovery, run `fastboot oem lock` from your computer.
1. The phone will reboot. 
1. Boot back into Recovery mode.
1. Choose _Wipe_ and _Format Data_. Completely wipe data.
1. Reboot. You should reboot into Lineage.

## Bugs

If you have issues with the Lineage build process, [check the upstream Docker image](https://github.com/lineageos4microg/docker-lineage-cicd/) for the bug first. Do not report feature requests, version bumps, devices you want added to this pipeline, et cetera.

