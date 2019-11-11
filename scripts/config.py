#!/usr/bin/env python3

import os
import configparser

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'fs'))

def get_config_data():
    """Get INI data as a ConfigParser object."""
    FILE_LOCATIONS = [
        os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.ini'))
    ]
    for location in FILE_LOCATIONS:
        if os.path.isfile(location):
            with open(location, 'r') as cfd:
                parser = configparser.ConfigParser()
                parser.read_file(cfd)
                for key in parser['filelocations']:
                    if parser['filelocations'][key] == '0':
                        parser['filelocations'][key] = os.path.join(BASE_DIR, key.replace("_dir", ""))
                return parser
    raise FileNotFoundError("Could not find configuration data at an expected location.")
