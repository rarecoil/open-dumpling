# Prebuilts

These are files used by the signing process that have been pre-built in my own boot pipeline
to avoid needing to rebuild them. If you do not trust these files, feel free to build them yourself.

## For Lineage 15.1

* **BootSignature.jar** - the underlying Java application wrapped by `boot_signer`
* **generate_verity_key** - the executable to convert your dm-verity key to one for the boot signing process.