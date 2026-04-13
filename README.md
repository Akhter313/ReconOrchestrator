

***

```markdown
# ReconOrchestrator
**Controlled Concurrency Engine for Web Application Fuzzing**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Security](https://img.shields.io/badge/Security-VAPT%20%7C%20Bug%20Bounty-red.svg)
![Environment](https://img.shields.io/badge/Environment-Linux%20%7C%20Kali-green.svg)

## 📌 Overview
**ReconOrchestrator** is a lightweight, Python-based concurrency wrapper engineered to automate multi-target web security assessments safely. 

Modern cloud infrastructure utilizes aggressive Web Application Firewalls (WAFs) and rate-limiting algorithms that immediately block brute-force directory discovery tools. Furthermore, running high-speed multi-target scans can rapidly exhaust local system resources and cause local network port exhaustion.

This tool solves both problems. It acts as an intelligent governor for high-speed fuzzing tools (specifically `ffuf`), enforcing strict thread limits, adaptive backoff strategies, and pre-scan heuristics to safely scan hundreds of targets simultaneously without crashing local hardware or triggering remote IP bans.

---

## ⚙️ Core Architecture & Features

### 1. Strict Thread Governance (Resource Management)
Utilizes Python's `concurrent.futures.ThreadPoolExecutor` to enforce a hard cap on active workers (Default: 5). This prevents local CPU throttling, memory spikes, and local router packet-drops during massive parallel execution.

### 2. Adaptive Rate-Limiting & Exponential Backoff
Actively monitors the `stdout` telemetry of the underlying fuzzing processes. If the engine detects WAF mitigation patterns (specifically `429 Too Many Requests` or `403 Forbidden` HTTP responses), it automatically intercepts the thread and triggers an exponential backoff `sleep()` routine, bypassing IDS bot-detection algorithms without terminating the overarching scan.

### 3. Pre-Execution Liveness Probing
Integrates a lightweight `requests`-based probing mechanism with strict timeouts. The engine verifies host viability before initiating resource-heavy fuzzing, drastically reducing overall scan time by actively dropping dead infrastructure or unresolvable DNS records.

### 4. Intelligent Noise Reduction
Leverages dynamic auto-calibration algorithms (`-ac`) to measure the exact byte-size and word-count of generic WAF wildcard responses (e.g., blanket `301 Redirects` or fake `200 OKs`), intelligently filtering out false positives and ensuring only highly actionable data is appended to the results.

### 5. Advanced IDS Evasion Tactics
* **Execution Jitter:** Implements randomized delays (`random.uniform()`) between thread launches to break predictable, automated network traffic patterns.
* **Target Array Shuffling:** Distributes the load across different physical infrastructure by randomizing the input list before execution.
* **Dynamic User-Agent Cycling:** Cycles through a curated pool of modern Desktop and Mobile User-Agents to bypass basic WAF signature rules.

---

## 🚀 Installation & Setup

It is highly recommended to run ReconOrchestrator within an isolated Python virtual environment to maintain system package integrity.

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/ReconOrchestrator.git](https://github.com/yourusername/ReconOrchestrator.git)
cd ReconOrchestrator

# 2. Initialize and activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Install required dependencies
pip install requests urllib3
```

*Note: This script requires `ffuf` to be installed and accessible in your system's PATH.*

---

## 🛠️ Usage

**1. Prepare your inputs:**
* Populate `targets.txt` with your target subdomains (one URL per line).
* Ensure you have a valid dictionary file saved as `wordlist.txt` in the root directory.

**2. Execute the Engine:**
```bash
python3 recon_orchestrator.py
```

**3. Read the Output:**
The engine runs in Silent Mode (`-s`) to keep the terminal interface clean. All valid, actionable endpoint discoveries are safely appended to `results.txt` without overwriting previous historical scan data.

---

## 💻 Terminal Interface (UI/UX)
ReconOrchestrator features a custom, color-coded CLI interface designed for rapid visual telemetry. 

* 🔵 **Blue `[+]`**: Liveness Check Passed / Fuzzing Initiated.
* 🔴 **Red `[-]`**: Host Dead / Connection Timeout / Skipped.
* 🟡 **Yellow `[!]`**: WAF Block Detected / Exponential Backoff Triggered.
* 🟢 **Green `[$$$]`**: Valid Endpoints Discovered & Logged.

---

## ⚠️ Disclaimer
**ReconOrchestrator was developed exclusively for authorized security research, penetration testing, and official Bug Bounty programs.** Executing automated reconnaissance against systems you do not own or do not have explicit, written permission to test is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---
*Engineered by Kamal Akhter*
```
