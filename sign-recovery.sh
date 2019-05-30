#!/bin/bash

java -jar BootSignature.jar /recovery $1 custom.pk8 custom.x509.der recovery_signed.img
java -jar BootSignature.jar -verify recovery_signed.img