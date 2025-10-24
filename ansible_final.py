import subprocess

# host map from IP address to host name
host_map = {
        "10.0.15.61": "R1",
        "10.0.15.62": "R2", 
        "10.0.15.63": "R3",
        "10.0.15.64": "R4",
        "10.0.15.65": "R5"
    }

def showrun(ip_address):
    # Convert IP address to host name (R1-R5)
    
    host = host_map.get(ip_address)
    if not host:
        return "Error: IP address not found in hardcoded list lmao"

    # Run ansible-playbook with specific host
    command = ['ansible-playbook', 'backup_cisco_router_playbook.yaml', '--limit', host]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    print(result)    
    if 'ok=2' in result:
        return "ok"
    else:
        return "Error: Ansible"
    
def motd(ip_address, motd_text):
    
    host = host_map.get(ip_address)
    if not host:
        return "Error: IP address not found in hardcoded list lmao"

    command = ['ansible-playbook', 'set_cisco_router_motd_playbook.yaml', '--limit', host]
    
    if motd_text:
        # Pass custom MOTD text as extra variable
        command.extend(['--extra-vars', f'custom_motd="{motd_text}"'])
    
    # Run ansible-playbook
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    print(output)
    
    # Check for successful execution
    if 'failed=0' in output and ('changed=' in output or 'ok=' in output):
        return "Ok: success"
    else:
        return "Error: Ansible"
