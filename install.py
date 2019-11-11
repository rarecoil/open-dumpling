#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import sys
import subprocess

import psutil
from scripts.config import get_config_data, BASE_DIR

config = get_config_data()

print("open-dumpling installation")

print("Configuring directories")
for dirloc in config['filelocations']:
    if not os.path.isdir(dirloc):
        print("Making %s" % dirloc)
        os.makedirs(dirloc)

# TODO: map userscripts/ into userscripts directory

print("Checking system prerequisites")
mem = psutil.virtual_memory()
if mem.total < 16000000000:
    print("This system requires 16GB or more to build Android.")
    sys.exit(1)

ccache_avail = psutil.disk_usage(config['filelocations']['ccache_dir'])
if ccache_avail.free < 50000000000:
    print("CCache disk requires at least 50GB of free space.")
    sys.exit(1)

src_avail = psutil.disk_usage(config['filelocations']['src_dir'])
if src_avail.free < 110000000000:
    print("Source directory requires at least 110 GB free.")
    sys.exit(1)

# TODO: add more checks for mirroring, zips, twrp, etc.



print("Downloading build environment Dockerfile")
os.system("docker pull lineageos4microg/docker-lineage-cicd:latest")

print("Ready for first build. To build, run python scripts/build.py.")
sys.exit(0)