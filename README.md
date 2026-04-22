
# 🔐 Brute Force Detection & IP Blocking Lab

## 🧠 What this lab is about

Instead of just reading theory about brute-force attacks, I wanted to **see it happen, detect it, and stop it**.

So in this lab, I simulated repeated failed login attempts and then built a simple detection + response system using:

* Linux logs
* Python (regex parsing)
* Firewall rules (iptables)

End result → **detect attacker → block attacker automatically**

---

## 🎯 Goal

* Identify brute-force attempts from logs
* Extract attacker IP addresses
* Count repeated failures
* Automatically block suspicious IPs

---

## 🧱 Lab Setup

I built a small isolated lab using virtual machines.

**Environment:**

* VirtualBox
* Ubuntu Server (target machine)
* Windows machine (used to simulate attacker)
* Host-only network (so both machines can talk safely)

---

## 🌐 Network Setup

I configured the VM network like this:

* Adapter: Host-only
* Adapter Type: Intel PRO/1000 MT Desktop
* Cable: Connected

This setup ensures:

* Machines can communicate
* No external internet interference
* Safe environment for testing attacks

---

## ⚠️ Issue I Faced (Real Problem)

While setting up, I hit a network issue:

```bash
Temporary failure resolving 'archive.ubuntu.com'
```

Tried fixing it using:

```bash
sudo apt install isc-dhcp-client -y
```

But DNS was still broken.

👉 Instead of wasting time, I moved forward with the lab **without depending on internet**.

---

## 🔍 Step 1 — Log Monitoring

I started by checking authentication logs:

```bash
sudo journalctl | grep -i "failed"
```

I saw repeated entries like:

```
Failed password for invalid user
```

This clearly indicates:

* Someone is trying multiple logins
* Likely brute-force attempt

---

## 🧠 Step 2 — Build Detection Script

Instead of manually watching logs, I wrote a Python script.

### What it does:

* Reads `/var/log/auth.log`
* Searches for `"Failed password"`
* Extracts IP addresses using regex
* Counts number of attempts
* Blocks IP if attempts exceed threshold

---

### 🧾 Python Script

```python
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
```

---

## ⚔️ Step 3 — Simulate Attack

From the attacker machine, I made multiple failed SSH login attempts.

Result in logs:

```
Failed password for invalid user
Failed password for root
Failed password for admin
```

After several attempts → script triggered.

---

## 🛡️ Step 4 — Automatic Blocking

Once threshold exceeded:

```bash
iptables -A INPUT -s <attacker_ip> -j DROP
```

What happened:

* Attacker IP added to firewall
* Further connection attempts blocked

---

## 🔄 Step 5 — Testing Again

To verify:

* I flushed rules:

  ```bash
  iptables -F
  ```
* Changed attacker IP
* Re-ran attack

✔️ Detection worked again
✔️ Blocking worked again

---
## 📸 Screenshots

### 🔴 Attack (Brute Force)
![Attack](lab1.png)

### 🟡 Detection & Response
![Detection](lab2.png)

### 🟢 Blocking Result
![Blocking](lab3.png)

---

## 📊 What I Observed

* Logs give **real attack visibility**
* Even simple patterns like `"Failed password"` are powerful
* Repeated attempts = strong signal
* Automating response saves time

---

## 🧠 What I Learned

* Regex is extremely useful for log parsing
* Linux logs are a goldmine for detection
* Even a basic script can act like a mini IDS
* Firewall rules are simple but effective

---

## ⚠️ Limitations

This is a basic implementation. Some issues:

* Not real-time (reads file, not live stream)
* No whitelist (could block legit users)
* No logging of blocked IPs
* iptables rules not persistent after reboot

---

## 🚀 Improvements (Next Level)

If I extend this:

* Use `tail -f` for real-time detection
* Add whitelist for trusted IPs
* Store alerts in a file or database
* Replace with **fail2ban-style logic**
* Integrate into SIEM

---

## 🧾 Conclusion

This lab helped me understand how detection actually works in real systems:

**Logs → Pattern → Detection → Action**

Not theory — actual working flow.

---

## ▶️ How to Run

```bash
sudo python3 script.py
```

Make sure:

* `/var/log/auth.log` exists
* You have sudo privileges
* iptables is installed

---


