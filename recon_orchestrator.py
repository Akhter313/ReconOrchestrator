
import concurrent.futures
import subprocess
import random
import time
import os
import requests
import urllib3

# Suppress SSL warnings for our pre-scan liveness checks so the terminal stays clean
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Terminal UI Colors ---
class UI:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# --- Configuration & Hardware Limits ---
MAX_WORKERS = 5
WORDLIST = "wordlist.txt"
RESULTS_FILE = "results.txt"

# Dynamic User-Agent Cycling Pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

def print_banner(target_count, workers):
    # Main title in Cyan (Slant style), Subtitle in Blue for contrast
    banner = f"""{UI.CYAN}{UI.BOLD}
    ____                           ____           __               __             __            
   / __ \\___  _________  ____     / __ \\_________/ /_  ___  ____  / /__________ _/ /_____  _____
  / /_/ / _ \\/ ___/ __ \\/ __ \\   / / / / ___/ ___/ __ \\/ _ \\/ ___/ __/ ___/ __ `/ __/ __ \\/ ___/
 / _, _/  __/ /__/ /_/ / / / /  / /_/ / /  / /__/ / / /  __(__  ) /_/ /  / /_/ / /_/ /_/ / /    
/_/ |_|\\___/\\___/\\____/_/ /_/   \\____/_/   \\___/_/ /_/\\___/____/\\__/_/   \\__,_/\\__/\\____/_/     
{UI.RESET}{UI.BLUE}
  > SYSTEM   : Target Acquisition & Concurrency Engine
  > PROTOCOL : Automated Web Reconnaissance / Rate-Limit Evasion
  > DEV      : Kamal Akhter | VERSION: 1.0
{UI.RESET}"""
    
    print(banner)
    print(f"[{UI.BLUE}*{UI.RESET}] Processing {target_count} domain(s)")
    print(f"[{UI.BLUE}*{UI.RESET}] Initiating {workers} concurrent workers...\n")

def check_liveness(url):
    """
    Performs a lightweight GET request to ensure the host is alive.
    If it times out or refuses connection, we skip fuzzing to save time.
    """
    target_url = url if url.startswith("http") else f"https://{url}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        # 5-second timeout; we just want to know if a server responds at all
        requests.get(target_url, headers=headers, timeout=5, verify=False)
        return True
    except requests.RequestException:
        return False

def scan_target(url, worker_id):
    """Core fuzzing logic handling WAF evasion, rate limiting, and ffuf execution."""
    
    # 1. Pre-scan Liveness Check
    if not check_liveness(url):
        print(f"[{UI.RED}-{UI.RESET}] Worker {worker_id} | Host Dead/Timeout | Skipping: {url}")
        return

    print(f"[{UI.BLUE}+{UI.RESET}] Worker {worker_id} | Liveness Passed | Fuzzing: {url}")
    
    # 2. Randomized Jitter (IDS Evasion)
    time.sleep(random.uniform(0.5, 2.5))
    
    # 3. User-Agent Cycling
    current_ua = random.choice(USER_AGENTS)
    target_url = url if url.startswith("http") else f"https://{url}"
    
    # 4. Constructing the ffuf Subprocess Command
    command = [
        "ffuf",
        "-u", f"{target_url}/FUZZ",
        "-w", WORDLIST,
        "-t", "10",        # Internal thread limit
        "-ac",             # Auto-calibrate to kill wildcard 301s/200s
        "-s",              # Silent mode (only valid hits in stdout)
        "-H", f"User-Agent: {current_ua}"
    ]

    backoff_time = 15
    max_retries = 3
    attempts = 0

    while attempts < max_retries:
        try:
            # Execute ffuf
            result = subprocess.run(command, capture_output=True, text=True, timeout=600)
            output = result.stdout + result.stderr
            
            # 5. Adaptive Rate Control (Exponential Backoff)
            if "429" in output or "403" in output:
                print(f"[{UI.YELLOW}!{UI.RESET}] Worker {worker_id} | WAF Block (429/403) on {url}. Sleeping for {backoff_time}s...")
                time.sleep(backoff_time)
                backoff_time *= 2  # Double the backoff time for the next potential failure
                attempts += 1
                continue  # Retry the same URL
            
            # 6. Save Valid Results
            if output.strip():
                with open(RESULTS_FILE, "a") as f:
                    f.write(f"\n--- Results for {url} ---\n")
                    f.write(output)
                print(f"[{UI.GREEN}$$${UI.RESET}] Worker {worker_id} | Hits found on {url}! Saved to results.txt")
            
            break  # Success! Break the retry loop.

        except subprocess.TimeoutExpired:
            print(f"[{UI.RED}-{UI.RESET}] Worker {worker_id} | ffuf Timed Out on {url}.")
            break
        except Exception as e:
            print(f"[{UI.RED}-{UI.RESET}] Worker {worker_id} | Subprocess Error on {url}: {e}")
            break

def main():
    # File Validation
    if not os.path.exists("targets.txt"):
        print(f"[{UI.RED}-{UI.RESET}] Error: 'targets.txt' not found in current directory.")
        return
    if not os.path.exists(WORDLIST):
        print(f"[{UI.RED}-{UI.RESET}] Error: '{WORDLIST}' not found. Please provide a valid wordlist.")
        return
        
    with open("targets.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
        
    if not urls:
        print(f"[{UI.RED}-{UI.RESET}] Error: 'targets.txt' is empty.")
        return

    # Target Shuffling (Distribute the load)
    random.shuffle(urls)
    
    # Print the custom CLI Banner
    print_banner(len(urls), MAX_WORKERS)

    # Strict Concurrency Governor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for index, url in enumerate(urls):
            # Assign a worker ID (1-5) for clean UI tracking
            worker_id = (index % MAX_WORKERS) + 1
            executor.submit(scan_target, url, worker_id)
            
    print(f"\n[{UI.GREEN}*{UI.RESET}] Recon completed safely. Check 'results.txt' for valid findings.")

if __name__ == "__main__":
    main()

