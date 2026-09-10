Markdown
# 🚀 Atomic Wallet Dogecoin Seed Recovery

A high-performance, interactive, and offline recovery tool designed to restore lost Dogecoin funds from Atomic Wallet using 11 known words of a 12-word BIP-39 mnemonic seed.

## ⚠️ The Problem: Atomic Wallet Derivation Bug

Older versions of Atomic Wallet had a known derivation path issue. Instead of generating Dogecoin addresses on the standard BIP-44 Dogecoin path (`m/44'/3'/0'/0`), it mistakenly used the Bitcoin derivation path (`m/44'/0'/0'/0`). 

Standard recovery wallets (like Trust Wallet or Exodus) only scan the standard `3'` path, causing imported seeds from Atomic Wallet to show a `0.0 DOGE` balance. This tool brute-forces the missing 12th word and scans **both** legacy and standard paths in milliseconds directly in RAM to find the exact matching target address.

## ✨ Features

- **100% Offline & Secure:** Makes zero network requests. Validates checksums and target addresses entirely locally.
- **In-Memory Execution:** Seed phrases are never written to disk, ensuring maximum security for your private keys.
- **Interactive CLI:** Prompts the user step-by-step for the 11 words and the target Dogecoin address.
- **Dual-Path Scanning:** Checks both standard BIP-44 Dogecoin paths and legacy Atomic Wallet bugged paths.
- **Ultra-Fast:** Validates 1,536 BIP-39 checksum combinations against a target address in milliseconds.
- **Multi-Language:** Fully implemented in both **TypeScript** (Node.js) and **Python**.

---

## 🛠️ Installation & Usage (TypeScript / Node.js)

The TypeScript implementation is built with robust cryptographic standards using `bitcoinjs-lib`, `bip39`, and `bip32`.

### Prerequisites
- Node.js (v16 or higher)
- npm

### Run
```bash
cd typescript
npm install
npm start
```
The script will interactively prompt you for your 11 words and the target Dogecoin address.

🐍 Installation & Usage (Python)
The Python implementation is lightweight and utilizes foundational ecdsa and mnemonic algorithms.

Prerequisites
Python 3.8+

pip

### Run
```Bash
cd python
pip install -r requirements.txt
python recovery.py
```

The script will interactively prompt you for your 11 words and the target Dogecoin address.

🔒 Security Warning
NEVER commit or upload your actual seed phrase to GitHub or any cloud storage. Always run this tool on a secure, offline machine if possible. Ensure you have added node_modules/ and __pycache__/ to your .gitignore file before pushing any code to a public repository.

⚖️ Disclaimer
This tool is provided "as is" for educational and recovery purposes. Use it at your own risk. The author is not responsible for any lost funds, compromised keys, or unintended consequences resulting from the use of this software.