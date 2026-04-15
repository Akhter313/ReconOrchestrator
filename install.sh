#!/bin/bash
echo "========================================"
echo " ReconOrchestrator Setup Script"
echo "========================================"

echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[*] Checking system for ffuf..."
if ! command -v ffuf &> /dev/null
then
    echo "[-] ffuf is not installed! Please install it to use this engine."
    echo "    Try: sudo apt install ffuf"
    exit 1
else
    echo "[+] ffuf detected!"
fi

echo "[*] Downloading default SecLists wordlist..."
mkdir -p wordlists
wget -q -O wordlists/default.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/raft-small-directories.txt
echo "[+] Wordlist downloaded successfully."

echo "[+] Setup Complete. You are ready to run: python3 recon_orchestrator.py"
