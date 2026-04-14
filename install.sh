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

echo "[+] Setup Complete. You are ready to run: python3 recon_orchestrator.py"
