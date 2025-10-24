import subprocess

def showrun(ip_address):
    # Convert IP address to host name (R1-R5)
    host_map = {
        "10.0.15.61": "R1",
        "10.0.15.62": "R2", 
        "10.0.15.63": "R3",
        "10.0.15.64": "R4",
        "10.0.15.65": "R5"
    }
    
    host = host_map.get(ip_address)
    if not host:
        return "Error: Invalid IP address"

    # Run ansible-playbook with specific host
    command = ['ansible-playbook', 'backup_cisco_router_playbook.yaml', '--limit', host]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    print(result)    
    if 'ok=2' in result:
        return "ok"
    else:
        return "Error: Ansible"
