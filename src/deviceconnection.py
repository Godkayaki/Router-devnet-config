#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez

import os
from ncclient import manager
from jinja2 import Template

def test_connection(HOST, PORT, USER, PSWD):
    try:
        m = manager.connect(host=HOST, port=PORT, username=USER, password=PSWD, hostkey_verify=False, device_params={'name': 'csr'}, look_for_keys=False, allow_agent=False)
    except:
        return False
    return True

def return_connection(HOST, PORT, USER, PSWD):
    try:
        m = manager.connect(host=HOST, port=PORT, username=USER, password=PSWD, hostkey_verify=False, device_params={'name': 'csr'}, look_for_keys=False, allow_agent=False)
        return m
    except:
        return False

#x = test_connection('ios-xe-mgmt.cisco.com', 10000, 'developer', 'C1sco12345')
#print(x)