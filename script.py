import re
import subprocess

pattern = r"\d+\.\d+\.\d+\.\d+"
count = {}

with open("/var/log/auth.log", "r") as f:
    for line in f:
        if "Failed password" in line:
            ip = re.search(pattern, line)
            if ip:
                ip = ip.group()
                count[ip] = count.get(ip, 0) + 1

for ip, attempts in count.items():
    if attempts > 5:
        print(f"[ALERT] Brute force detected from {ip}")
        
        subprocess.run([
            "sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"
        ])
        
        print(f"[BLOCKED] {ip}")