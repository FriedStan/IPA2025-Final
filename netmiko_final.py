from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.64"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
    "ssh_config_file": "cisco_ssh_config",
}


def gigabit_status():
    ans = ""
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
