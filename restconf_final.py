import json
import requests
requests.packages.urllib3.disable_warnings()

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")

# Router IP Address is 10.0.15.61-65 / choose one
def api_url(ip_address):
    return f"https://{ip_address}/restconf/data/"


def create(ip_address):
    # Create a loopback interface named Loopback66070030
    yangConfig = {
        "ietf-interfaces:interface": [
            {
                "name": "Loopback66070030",
                "description": "Created by IPA script",
                "type": "iana-if-type:softwareLoopback",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": "172.0.30.1",
                            "netmask": "255.255.255.0"
                        }
                    ]
                }
            }
        ]
    }

    resp = requests.post(
        api_url(ip_address) + "ietf-interfaces:interfaces",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070030 is created successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070030"


def delete(ip_address):
    resp = requests.delete(
        api_url(ip_address) + "ietf-interfaces:interfaces/interface=Loopback66070030",
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070030 is deleted successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070030"


def enable(ip_address):
    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": True
        }
    }

    resp = requests.patch(
        api_url(ip_address) + "ietf-interfaces:interfaces/interface=Loopback66070030",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070030 is enabled successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070030"


def disable(ip_address):
    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url(ip_address) + "ietf-interfaces:interfaces/interface=Loopback66070030",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if 200 <= resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070030 is shutdowned successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 66070030"


def status(ip_address):
    api_url_status = api_url(ip_address) + "ietf-interfaces:interfaces-state/interface=Loopback66070030"

    resp = requests.get(
        api_url_status,
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        print(f"Admin Status: {admin_status}, Oper Status: {oper_status}")
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070030 is enabled (checked by Restconf)"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070030 is disabled (checked by Restconf)"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070030 (checked by Restconf)"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))