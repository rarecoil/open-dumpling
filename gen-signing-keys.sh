#!/bin/bash

openssl genrsa -f4 -out custom.pem 2048
openssl pkcs8 -in custom.pem -topk8 -outform DER -out custom.pk8 -nocrypt
openssl req -new -x509 -sha256 -key custom.pem -out custom.x509.pem
openssl x509 -outform DER -in custom.x509.pem -out custom.x509.der
rm custom.x509.pem custom.pem