#!/bin/bash

# Build and set verity signing key for boot image signing
if [ "$SIGN_BUILDS" = true ]; then
    if [[ $branch =~ .*lineage-15\.1.* ]]; then
        echo ">> [$(date)] Patching Lineage 15.1 dumpling for boot signing + dm-verity"
        sed -i "1s;^;$(call inherit-product, build/target/product/verity.mk)\n;" "device/oneplus/dumpling/device.mk"
    fi

    if [ ! -f $KEYS_DIR/verity_key ]; then
        echo ">> [$(date)] Building verity key conversion tool"
        make generate_verity_key
        echo ">> [$(date)] Converting verity key"
        out/host/linux-x86/bin/generate_verity_key -convert user-keys/verity.x509.pem user-keys/verity_key
        # the key adds ".pub". we don't want that.
        mv user-keys/verity_key.pub user-keys/verity_key
        sed -i "1s;^;PRODUCT_VERITY_SIGNING_KEY := user-keys/verity_key\n\n;" "vendor/$vendor/config/common.mk"
    fi  
fi