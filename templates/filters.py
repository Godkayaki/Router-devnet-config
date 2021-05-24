#!/usr/bin/python3
#-*- coding: utf-8 -*-
#Daniel Gonzalez

# full filter
full_filter = '''
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        </native>
    </filter>
'''

# Create a configuration filter
interface_filter = '''
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <GigabitEthernet>
                </GigabitEthernet>
            </interface>
        </native>
    </filter>
'''

# get hostname
hostname_filter = '''
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>
                </hostname>
            </native>
        </filter>
    '''

# get motd banner
motd_filter = '''
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <banner>
                    <motd>
                        <banner>
                        </banner>
                    </motd>
                </banner>
            </native>
        </filter>
    '''