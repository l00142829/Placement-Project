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


IETF_INTERFACE_TYPES = {
        "loopback": "ianaift:softwareLoopback",
        "ethernet": "ianaift:ethernetCsmacd"
    }


netconf_interface_template = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
        	<name>{name}</name>
        </interface>
    </interfaces>
</config>"""


new_loopback = {}
new_loopback["name"] = "Loopback" + input("What loopback number to delete? ")

# Create the NETCONF data payload for this interface
netconf_data = netconf_interface_template.format(
        name = new_loopback["name"]
    )

print("The configuration payload to be sent over NETCONF.\n")
print(netconf_data)

print("Opening NETCONF Connection to {}".format(env_lab.IOS_XE_1["host"]))


with manager.connect(
        host=env_lab.IOS_XE_1["host"],
        port=env_lab.IOS_XE_1["netconf_port"],
        username=env_lab.IOS_XE_1["username"],
        password=env_lab.IOS_XE_1["password"],
        hostkey_verify=False
        ) as m:

    print("Sending a <edit-config> operation to the device.\n")
  
    netconf_reply = m.edit_config(netconf_data, target = 'running')

print("Here is the raw XML data returned from the device.\n")

print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")