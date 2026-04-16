# ReconOrchestrator
**Controlled Concurrency Engine for Web Application Fuzzing**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![Security](https://img.shields.io/badge/Security-VAPT%20%7C%20Bug%20Bounty-red.svg)
![Environment](https://img.shields.io/badge/Environment-Linux%20%7C%20Kali-green.svg)

<img width="1920" height="1043" alt="Untitled design(5)" src="https://github.com/user-attachments/assets/77fefe1a-db5c-45fc-ae45-682fa9a9475d" />


## Overview
**ReconOrchestrator** is a lightweight, Python-based concurrency wrapper engineered to automate multi-target web security assessments safely. 

Modern cloud infrastructure utilizes aggressive Web Application Firewalls (WAFs) and rate-limiting algorithms that immediately block brute-force directory discovery tools. Furthermore, running high-speed multi-target scans can rapidly exhaust local system resources and cause local network port exhaustion.

This tool solves both problems. It acts as an intelligent governor for high-speed fuzzing tools (specifically `ffuf`), enforcing strict thread limits, adaptive backoff strategies, and pre-scan heuristics to safely scan hundreds of targets simultaneously without crashing local hardware or triggering remote IP bans.

---

##  Features

  * **Intelligent Anomaly Detection** - Dynamically counts directory hits to identify and drop "Catch-All" (Soft 404) servers that trick standard auto-calibration, keeping your results perfectly clean.
  * **Strict Concurrency & Kill Switches** - Multi-threaded processing with hard-capped workers and a strict 2-minute execution limit per subdomain to prevent tarpitting.
  * **Adaptive Rate-Limiting** - Exponential backoff automatically triggers upon detecting `429` or `403` WAF mitigation responses.
  * **Smart Pre-Probing** - Lightweight liveness checks drop dead infrastructure before heavy fuzzing begins.

##  Installation

ReconOrchestrator is designed for Kali Linux and Debian-based systems.

```bash
git clone [https://github.com/Akhter313/ReconOrchestrator.git](https://github.com/Akhter313/ReconOrchestrator.git)
cd ReconOrchestrator

# Run the automated setup script (Installs dependencies & SecLists payload)
bash install.sh

# Activate the virtual environment
source venv/bin/activate
```

*Note: Ensure you have `ffuf` installed (`sudo apt install ffuf`) and accessible in your system's PATH.*

##  Usage

**Basic Usage**

```bash
# Ensure targets.txt is populated with URLs, then run:
python3 recon_orchestrator.py
```

##  How It Works

1.  **Input Processing** - Reads targets and wordlists, shuffling the array to distribute load.
2.  **Liveness Probing** - Pings the host with randomized User-Agents to verify uptime.
3.  **Thread Assignment** - Spawns a worker under strict ThreadPool limits and enforces a 2-minute max-execution kill switch per target.
4.  **Fuzzing Execution** - Invokes `ffuf` with auto-calibration and silent flags.
5.  **Telemetry Analysis** - Intercepts the WAF response; pauses the thread and applies exponential backoff if rate-limited.
6.  **Anomaly Detection** - Evaluates the final hit count. Instantly discards the dataset if it detects Catch-All (Soft 404) behavior.
7.  **Output Generation** - Appends only valid, verified, and non-anomalous hits to `results.txt`.

##  Core Architecture

ReconOrchestrator bridges the gap between raw speed and connection stability:

| Mechanism | Description | Benefit |
| :--- | :--- | :--- |
| **ThreadPoolExecutor** | Hard-caps concurrent background processes. | Prevents local router packet drops. |
| **Requests Timeout** | 5-second lightweight pre-scan check. | Saves time on unresolvable DNS/dead IPs. |
| **Subprocess Regex** | Monitors stdout for 429/403 blocks. | Evades Cloudflare/Akamai bot detection. |
| **Anomaly Filtering** | Drops data if hits exceed logical thresholds. | Eliminates false-positive Catch-All noise. |

##  Bug Bounty Workflow

```bash
# Step 1: Subdomain enumeration
subfinder -d target.com -o targets.txt

# Step 2: Run the Orchestrator (It handles Liveness Checking automatically)
python3 recon_orchestrator.py

# Step 3: Pass valid findings directly to vulnerability scanners
cat results.txt | nuclei -t vulnerabilities/
```

##  Input Configurations

**targets.txt**
Populate this file with your live subdomains.
```text
api.target.com
staging.target.com
uat-crm.target.com
# ... all found subdomain of the target
```

**wordlists/default.txt**
The `./install.sh` script automatically downloads the `raft-small-directories.txt` list from SecLists into this directory. You can swap this out for any custom `.txt` wordlist depending on your target.

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

##  Disclaimer

This tool is intended for security research and authorized testing only. Users are responsible for complying with applicable laws and regulations. Executing automated reconnaissance against systems you do not own or do not have explicit, written permission to test is illegal. The author assumes no liability for misuse.


