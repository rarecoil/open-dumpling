#!/bin/bash

cp vendor/VerifiedBootSigner-v8.zip .
zip -u ./VerifiedBootSigner-v8.zip custom.pk8
zip -u ./VerifiedBootSigner-v8.zip custom.x509.der