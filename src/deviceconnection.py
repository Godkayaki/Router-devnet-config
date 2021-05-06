#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez

import os
from ncclient import manager
from jinja2 import Template

def test_connection(host, port, user, pswd):
    try:
        m = manager.connect(host=HOST, port=PORT, username=USER, password=PSWD, hostkey_verify=False, device_params={'name': 'csr'}, look_for_keys=False, allow_agent=False)
    except:
        return False
    return True