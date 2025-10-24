from netmiko import ConnectHandler
from pprint import pprint
import re

username = "admin"
password = "cisco"

def set_device_params(device_ip):
    device_params = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
        "ssh_config_file": "cisco_ssh_config",
    }
    return device_params


def gigabit_status(ip_address):
    ans = ""
    device_params = set_device_params(ip_address)
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        entries = []
        for status in result:
            name = status.get("intf", status.get("interface", ""))
            if name.startswith("GigabitEthernet"):
                state = status.get("status", "").lower()
                entries.append(f"{name} {state}")
                if state == "up":
                    up += 1
                elif state == "down":
                    down += 1
                elif state == "administratively down":
                    admin_down += 1
        ans = f"{', '.join(entries)} -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans

def get_motd(ip_address):
    device_params = set_device_params(ip_address)
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command("show running-config", use_textfsm=True)
        
        # Extract the banner content between ^C markers
        motd_pattern = r'banner motd \^C(.*?)\^C'
        match = re.search(motd_pattern, result, re.DOTALL)
        
        if match:
            text = match.group(1).strip()
            pprint(text)
            return text
        else:
            return "Error: No MOTD Configured"
