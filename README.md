# NeutrOSINT
Determine if an email address exists or not on ProtonMail with NeutrOSINT

Alternative to [ProtOSINT](https://github.com/pixelbubble/ProtOSINT) since the validation using the API doesn't work anymore.

This tool uses selenium to connect to ProtonMail and checks if email addresses are valid or not.

---
# How to use?

### Installation

You must have Chrome Browser installed on your machine:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```
Tested on Ubuntu 20.04.4 LTS x64 and Kali Linux 2021.1 x64

### Prerequisites

```bash
pip install -r requirements.txt
```
You must have a valid Protonmail account


### Usage:
```bash
python3 main.py -h
```

```bash
python3 main.py -u 'USERNAME' -p 'PASSWORD' -f 'FILE_CONTAING_EMAILS.txt' 
```

