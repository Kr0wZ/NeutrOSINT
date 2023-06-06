# NeutrOSINT
Determine if an email address exists or not on ProtonMail with NeutrOSINT

Alternative to [ProtOSINT](https://github.com/pixelbubble/ProtOSINT) since the validation using the API doesn't work anymore.

This tool uses selenium to connect to ProtonMail and checks if email addresses are valid or not.

---
### What's new?

##### 06/06/2023:
  - Protonmail added a new field and a cookie for API requests: "x-pm-uid" and "AUTH-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX". With the tests I've done, these values must be generated one and then can be reused over time.
  - Added regex to check emails syntax
  - Business email addresses are now detected both in light mode and with selenium. In light mode it only gives an idea if a domain is a business domain used with protonmail but can't determine if email exists. You must you the selenium version to be sure of that (with username and password).
  - Changed print format to be more python3 friendly


This 2.0 version introduces a new 'mode': Light mode.

Thanks to [@Nenaff_](https://twitter.com/Nenaff_), I knew it was possible to request the verification of an email without the use of selenium.<br/>
This is way faster but if you have a lot of email addresses to verify you'll be blocked after 100 requests (don't know precisely how much time but at least more than an hour).<br/>
The solution is either to use a proxy to bypass this limitation or use the other mode of NeutrOSINT which uses username and password (but you need to have a valid account - you can create one for free).


---
# Notes

- API limit with light mode: 100 requests per hour.
- Free protonmail accounts are limited to 100 entries for 'To' field. But the tool handles this. It just takes a bit more time.
- If the string 'None' appears in the creation date for valid accounts then it means the API limit is probably reached. Since this is not the same API as for the light mode, here we have only 16 requests per hour.
- For some obscure reasons, sometimes selenium isn't able to get access to the 'New Email' button. In this case it is recommended to run the script again.

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
Show help message:
```bash
python3 main.py -h
```

Run the light mode using the protonmail API:
```bash
python3 main.py -l -e 'EMAIL_TO_VERIFY' 
```

Run with selenium by specifying username and password.
```bash
python3 main.py -u 'USERNAME' -p 'PASSWORD' -f 'FILE_CONTAING_EMAILS.txt' 
```

---
# How does it work?

The light mode calls the Protonmail API at this endpoint: https://account.proton.me/api/users/available <br/>
Depending on the status code, we can determine if an email address already exists or not.

The selenium mode uses selenium with the given credentials to connect to protonmail, go to 'New Email', then fills in the 'To' field with all the email addresses to check.



