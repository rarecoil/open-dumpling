#!/usr/bin/env python3
"""
Functions that deal with downloading official TWRP recoveries
from the TWRP website and signing them with the verity key.
"""

import os
import sys
import requests
import re
import hashlib
import subprocess
from bs4 import BeautifulSoup

from config import get_config_data

LINK_VERSION_REGEX = r'/[a-z]+/twrp-(\d+\.\d+\.\d+-\d+)-[a-z]+\.img\.html'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0'

def get_twrp_versions():
    """Get all available TWRP versions."""
    versions = []
    ret = requests.get("https://dl.twrp.me/dumpling/", timeout=10)
    if ret.status_code == 200:
        soup = BeautifulSoup(ret.content, features="html.parser")
        table_rows = soup.find_all('tr')
        for row in table_rows:
            link = row.find('a')
            href = link['href']
            result = re.search(LINK_VERSION_REGEX, href)
            if result != None:
                versions.append(result.groups()[0])
    return versions

def download_twrp_version(version, variant='dumpling', location='/tmp', check_integrity=True):
    """Download a TWRP recovery from the website."""
    image_name = "twrp-%s-%s.img" % (version, variant)
    uri = "https://dl.twrp.me/%s/%s" % (variant, image_name)
    #referer_uri = uri + ".html"
    #sig_uri = uri + ".asc"
    sha256_uri = uri + ".sha256"
    headers = { "Referer": uri, "User-Agent": USER_AGENT }
    filepath = os.path.join(location, image_name)
    # save the file
    checksum = None
    if check_integrity:
        ret = requests.get(sha256_uri, headers=headers, timeout=1, allow_redirects=True)
        if ret.status_code == 200:
            checksum = ret.text
            checksum = checksum[0:63]
    ret = requests.get(uri, headers=headers, timeout=10, allow_redirects=True)
    with open(filepath, 'wb') as f:
        for chunk in ret.iter_content(chunk_size=512 * 1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    # shasum the downloaded file 
    if check_integrity:
        hashsum = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                buf = f.read(16384)
                if not buf:
                    break
                hashsum.update(buf)
        hexstr = hashsum.hexdigest()
        if str(hexstr) != checksum:
            raise IOError("File checksum failed. %s != %s" % (hexstr, checksum))
    return filepath

def sign_recovery(boot_signer_jar_path, unsigned_recovery_file, verity_key_pk8, verity_key_pem, signed_output):
    """Call Java to sign the recovery file."""
    # https://forum.xda-developers.com/android/software-hacking/signing-boot-images-android-verified-t3600606
    retcode = subprocess.call(["java", 
        "-jar", 
        boot_signer_jar_path, 
        "/recovery",
        verity_key_pem,
        verity_key_pk8,
        signed_output]) 
    return (retcode == 0)

def verify_recovery(boot_signer_jar_path, recovery_file):
    """Verify a recovery was signed."""
    retcode = subprocess.call([
        "java",
        "-jar",
        boot_signer_jar_path,
        "-verify",
        recovery_file])
    return (retcode == 0)


if __name__ == "__main__":
    config = get_config_data()
    # get the recoveries directory
    # pull updates into unsigned/
    # check for anything in unsigned/ we have not auto-signed and put in signed/
    # sign them with the keys and place in signed/
    # TODO
    pass