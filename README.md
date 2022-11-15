# NeutrOSINT
Determine if an email address exists or not on ProtonMail with NeutrOSINT

Alternative to [ProtOSINT](https://github.com/pixelbubble/ProtOSINT) since the validation using the API doesn't work anymore.

This tool uses selenium to connect to ProtonMail and checks if email addresses are valid or not.

---
### How to use

Run the main.py file with python3

Usage:
```bash
python3 main.py -u 'USERNAME' -p 'PASSWORD' -f 'FILE_CONTAING_EMAILS.txt' 
```
