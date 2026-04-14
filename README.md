

***


# ReconOrchestrator
**Controlled Concurrency Engine for Web Application Fuzzing**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Security](https://img.shields.io/badge/Security-VAPT%20%7C%20Bug%20Bounty-red.svg)
![Environment](https://img.shields.io/badge/Environment-Linux%20%7C%20Kali-green.svg)


<img width="1916" height="572" alt="Untitled design" src="https://github.com/user-attachments/assets/b7bd020b-cfab-4494-978a-9edf28ee1552" />


## 📌 Overview
**ReconOrchestrator** is a lightweight, Python-based concurrency wrapper engineered to automate multi-target web security assessments safely. 

Modern cloud infrastructure utilizes aggressive Web Application Firewalls (WAFs) and rate-limiting algorithms that immediately block brute-force directory discovery tools. Furthermore, running high-speed multi-target scans can rapidly exhaust local system resources and cause local network port exhaustion.

This tool solves both problems. It acts as an intelligent governor for high-speed fuzzing tools (specifically `ffuf`), enforcing strict thread limits, adaptive backoff strategies, and pre-scan heuristics to safely scan hundreds of targets simultaneously without crashing local hardware or triggering remote IP bans.

---


## 🎯 Features

  * ⚡ **Strict Concurrency** - Multi-threaded processing with hard-capped workers to prevent local hardware exhaustion.
  * 🛡️ **Adaptive Rate-Limiting** - Exponential backoff automatically triggers upon detecting `429` or `403` WAF mitigation responses.
  * 🔍 **Smart Pre-Probing** - Lightweight liveness checks drop dead infrastructure before heavy fuzzing begins.
  * 🎯 **Intelligent Noise Reduction** - Dynamic auto-calibration filters out generic wildcard `301` and `200` responses.
  * 🥷 **Advanced IDS Evasion** - Implements execution jitter, target shuffling, and dynamic User-Agent cycling.

## 🚀 Installation

**From Source**

```bash
git clone https://github.com/Akhter313/ReconOrchestrator.git
cd ReconOrchestrator

# Initialize virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests urllib3
```

*Note: Ensure you have `ffuf` installed and accessible in your system's PATH.*

## 📖 Usage

**Basic Usage**

```bash
# Ensure targets.txt and wordlist.txt are populated, then run:
python3 recon_orchestrator.py
```

## 📊 Core Architecture

ReconOrchestrator bridges the gap between raw speed and connection stability:

| Mechanism | Description | Benefit |
| :--- | :--- | :--- |
| **ThreadPoolExecutor** | Hard-caps concurrent background processes. | Prevents local router packet drops. |
| **Requests Timeout** | 5-second lightweight pre-scan check. | Saves time on unresolvable DNS/dead IPs. |
| **Subprocess Regex** | Monitors stdout for 429/403 blocks. | Evades Cloudflare/Akamai bot detection. |
| **Auto-Calibration** | Analyzes baseline WAF responses. | Eliminates false-positive logs. |

## 🎯 Bug Bounty Workflow

```bash
# Step 1: Subdomain enumeration
subfinder -d target.com -o subdomains.txt

# Step 2: Resolve alive hosts (Optional, though ReconOrchestrator handles this)
cat subdomains.txt | httpx -mc 200 -o targets.txt

# Step 3: Run the Orchestrator
python3 recon_orchestrator.py

# Step 4: Pass valid findings directly to vulnerability scanners
cat results.txt | nuclei -t vulnerabilities/
```

## 📁 Example Output (Terminal UI)

```text
 █▀█ █▀▀ █▀▀ █▀█ █▄ █ █▀█ █▀█ █▀▀ █ █ █▀▀ █▀ ▀█▀ █▀█ ▄▀█ ▀█▀ █▀█ █▀█
 █▀▄ ██▄ █▄▄ █▄█ █ ▀█ █▄█ █▀▄ █▄▄ █▀█ ██▄ ▄█  █  █▀▄ █▀█  █  █▄█ █▀▄

  > SYSTEM   : Target Acquisition & Concurrency Engine
  > PROTOCOL : Automated Web Reconnaissance / Rate-Limit Evasion
  > DEV      : Kamal Akhter | VERSION: 1.0

[*] Processing 4 domain(s)
[*] Initiating 5 concurrent workers...

[-] Worker 4 | Host Dead/Timeout | Skipping: https://api.zerodha.com
[+] Worker 1 | Liveness Passed | Fuzzing: https://kite.zerodha.com
[+] Worker 2 | Liveness Passed | Fuzzing: https://coin.zerodha.com
[!] Worker 1 | WAF Block (429/403) on https://kite.zerodha.com. Sleeping for 15s...
[$$$] Worker 2 | Hits found on https://coin.zerodha.com! Saved to results.txt
```

## 📝 Input File Formats

**targets.txt**

```text
https://example.com
https://api.example.com
https://dev.example.com
```

**wordlist.txt**

```text
admin
login
api
dashboard
v1
```

## 🎓 How It Works

1.  📥 **Input Processing** - Reads targets and wordlists, shuffling the array to distribute load.
2.  🌐 **Liveness Probing** - Pings the host with randomized User-Agents to verify uptime.
3.  ⚙️ **Thread Assignment** - Spawns a dedicated worker using the ThreadPool limits.
4.  🔎 **Fuzzing Execution** - Invokes `ffuf` with auto-calibration and silent flags.
5.  🔄 **Telemetry Analysis** - Intercepts the WAF response; pauses the thread if rate-limited.
6.  📤 **Output Generation** - Appends only 100% valid, verified hits to `results.txt`.

## 🤝 Contributing

Contributions are welcome\! Please feel free to submit a Pull Request.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 👨‍💻 Author

**Kamal Akhter** \#\# ⭐ Support

If you found this tool helpful for your research, please consider giving it a star ⭐

## ⚠️ Disclaimer

This tool is intended for security research and authorized testing only. Users are responsible for complying with applicable laws and regulations. Executing automated reconnaissance against systems you do not own or do not have explicit, written permission to test is illegal. The author assumes no liability for misuse.
