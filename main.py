#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez

import os
from ncclient import manager
from jinja2 import Template

#https://unix.stackexchange.com/questions/340844/how-to-enable-diffie-hellman-group1-sha1-key-exchange-on-debian-8-0/340853
#https://dev.to/alecbuda/python-automation-on-cisco-routers-in-2019-netconf-yang-jinja2-52ho

project_path = os.path.dirname(__file__)
HOST='ios-xe-mgmt.cisco.com'
PORT=10000
USER='developer'
PSWD='C1sco12345'

# Create a configuration filter
interface_filter = '''
  <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
          <interface>
            <GigabitEthernet>
              <name>1</name>
            </GigabitEthernet>
          </interface>
      </native>
  </filter>
'''

m = manager.connect(host=HOST, port=PORT, username=USER, password=PSWD, hostkey_verify=False, device_params={'name': 'csr'}, look_for_keys=False, allow_agent=False)
'''with manager.connect(host=HOST, port=PORT, username=USER, password=PSWD, hostkey_verify=False, device_params={'name': 'csr'}, look_for_keys=False, allow_agent=False) as m:
    c = m.get_config(source='running').data_xml'''
    #with open("%s.xml" % host, 'w') as f:
    #    f.write(c)

interface_template = Template(open(project_path+'/interface.xml').read())
interface_rendered = interface_template.render(
  INTERFACE_INDEX='2', 
  IP_ADDRESS='10.0.0.1', 
  SUBNET_MASK='255.255.255.252'
)

#edit the router config
result = m.edit_config(target='running', config=interface_rendered)
print(result)

#get config of the router
#result = m.get_config('running', interface_filter)
#print(result)
#result = m.get_config('running')
#print(result)