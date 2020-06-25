#!/usr/bin/env python


import os
import sys
from ncclient import manager
import xmltodict
import xml.dom.minidom



here = os.path.abspath(os.path.dirname(__file__))


project_root = os.path.abspath(os.path.join(here, "../.."))



sys.path.insert(0, project_root)
import env_lab  # noqa


netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>"""

print("Opening NETCONF Connection to {}".format(env_lab.IOS_XE_1["host"]))


with manager.connect(
        host=env_lab.IOS_XE_1["host"],
        port=env_lab.IOS_XE_1["netconf_port"],
        username=env_lab.IOS_XE_1["username"],
        password=env_lab.IOS_XE_1["password"],
        hostkey_verify=False
        ) as m:

    print("Sending a <get-config> operation to the device.\n")
   
    netconf_reply = m.get_config(source = 'running', filter = netconf_filter)

print("Here is the raw XML data returned from the device.\n")

print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")


netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]


interfaces = netconf_data["interfaces"]["interface"]

print("The interface status of the device is: ")

for interface in interfaces:
    print("Interface {} enabled status is {}".format(
            interface["name"],
            interface["enabled"]
            )
        )
print("\n")
