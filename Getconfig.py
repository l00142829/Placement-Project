#!/usr/bin/env python


import os
import sys
from ncclient import manager
import xmltodict
import xml.dom.minidom



netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>"""


with manager.connect(
        host=10.10.100.1,
        port=830,
        username=l00142829,
        password=Cisco,
        hostkey_verify=False
        ) as m:

    print("Sending a <get-config> operation to the device.\n")
    netconf_reply = m.get_config(source = 'running', filter = netconf_filter)