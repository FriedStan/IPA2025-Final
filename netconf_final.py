from ncclient import manager
import xmltodict

def connect(ip_address):
    return manager.connect(
        host=ip_address,
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )

def create(ip_address):
    m = connect(ip_address)
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070030</name>
                <description>Created by IPA script</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>172.0.30.1</ip>
                        <netmask>255.255.255.0</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>"""

    try:
        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070030 is created successfully using Netconf"
    except:
        return "Cannot create: Interface loopback 66070030"

def delete(ip_address):
    m = connect(ip_address)
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback66070030</name>
            </interface>
        </interfaces>
    </config>"""

    try:
        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070030 is deleted successfully using Netconf"
    except:
        return "Cannot delete: Interface loopback 66070030"

def enable(ip_address):
    m = connect(ip_address)
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070030</name>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>"""

    try:
        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070030 is enabled successfully using Netconf"
    except:
        return "Cannot enable: Interface loopback 66070030"

def disable(ip_address):
    m = connect(ip_address)
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070030</name>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>"""

    try:
        netconf_reply = m.edit_config(target="running", config=netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070030 is shutdowned successfully using Netconf"
    except:
        return "Cannot shutdown: Interface loopback 66070030"

def status(ip_address):
    m = connect(ip_address)
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070030</name>
            </interface>
        </interfaces-state>
    </filter>"""

    try:
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        
        # Check if data exists and is not None
        if ('data' in netconf_reply_dict['rpc-reply'] and 
            netconf_reply_dict['rpc-reply']['data'] is not None and
            'interfaces-state' in netconf_reply_dict['rpc-reply']['data']):
            
            interface_data = netconf_reply_dict['rpc-reply']['data']['interfaces-state']['interface']
            admin_status = interface_data['admin-status']
            oper_status = interface_data['oper-status']
            
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070030 is enabled (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070030 is disabled (checked by Netconf)"
        
        return "No Interface loopback 66070030 (checked by Netconf)"
    except Exception as e:
        print(f"Error: {str(e)}")
