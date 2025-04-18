# WindowManager

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue)]()
[![My page](https://img.shields.io/badge/My_Page-000000?style=flat&logo=bento&logoColor=white)](https://bento.me/fanaticexplorer)


A lightweight Windows utility to manage application windows from the command line.

## Download

Pre-built executable available in [Releases](https://github.com/FanaticExplorer/windowmanager/releases).

## Installation

### Option 1: Using the executable
1. Download the latest `windowmanager.exe` from Releases
2. Place it in a directory included in your system PATH or add its location to PATH

### Option 2: From source (optional)

```bash
git clone https://github.com/FanaticExplorer/WindowManager.git
cd WindowManager
pip install -r requirements.txt
```

## Usage

Run the program with `--help` for complete usage instructions:

```bash
windowmanager --help
```

## Examples

```bash
# List all open windows
windowmanager -l

# Check if Notepad is running
windowmanager -e -t "Notepad"

# Minimize Calculator window
windowmanager -m -t "Calculator"

# Focus Chrome browser window
windowmanager -f -p "chrome"

# Check if window with PID 1234 is minimized
windowmanager -z --pid 1234
```

## 💖 Support the Developer

If you find this tool useful, consider supporting my work:

[![Buy me a coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/FanaticExplorer)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/FanaticExplorer)
[![Monobank Card](https://img.shields.io/badge/Monobank_Card-000000?style=flat&logo=visa&logoColor=white)](https://send.monobank.ua/3KAPtPvd4a)

You can also support me with cryptocurrency:

**Binance Pay ID:** `780389392`

[![Binance Pay QR code](https://img.shields.io/badge/Binance_Pay_QR_code-F0B90B?style=flat&logo=binance&logoColor=black)](https://i.imgur.com/WEYYdTn.png)

**Direct Wallet Addresses:**
- **BTC:** `1ksLDnSTekh9kdQcgeqtbdZtxKuLtDobC`
- **ETH (ERC20):** `0xef174683a9ca0cc6065bb8de433188bb1767b631`
- **USDT (TRC20):** `TC3SSLB1cyD1PEugufHF5zUv3sVpFhCi7z`
- **SOL (Solana):** `4ZZhbfJMevkg3x9W8KQiBsdFLz5NAkKMm7takXi2Lz8i`

Every donation helps me create and maintain more useful tools!

## License

MIT © [FanaticExplorer](https://github.com/FanaticExplorer)
