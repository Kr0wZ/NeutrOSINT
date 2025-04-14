# NeutrOSINT
Determine if an email address exists or not on ProtonMail with NeutrOSINT without alerting the target.
NeutrOSINT is now able to determine if a username is used as a Protonmail address (first part of the email address).

Alternative to [ProtOSINT](https://github.com/pixelbubble/ProtOSINT) since the validation using the API doesn't work anymore.

This tool uses selenium to connect to ProtonMail and checks if email addresses are valid or not.
The "light" mode is faster and only uses the API to determine the validity of a Protonmail email address. No need to have a Protonmail account.

---
### What's new?

##### 14/04/2025
  - Thanks to [f0rked](https://github.com/yetanotherf0rked) you can now install NeutrOSINT in an easy way and use it across your system -> pip install -e .
  - [f0rked](https://github.com/yetanotherf0rked) also implemented the search username functionality that allow you to specify a username to be checked across multiple domains used by Protonmail to verify if it is used as an email address.
  - Fixed the selenium module which now works correctly.
  - Added details about the keys generation (algorithm and date).
  - No need to specify the flag `-l / --light` anymore to use the "light" mode. Not specifying options `-u` and `-p` automatically switches to the light mode.
  - Added `-k / --key` support to print the key pair used to encrypt emails (public key).

##### 08/06/2023:
  - "x-pm-uid" is in fact valid for 24 hours. It must be generated again to perform requests. This is now fixed and every requests generate a new AUTH cookie to perform searches.
  - @OSINT_Tactical found that it was possible to determine the source address of a protonmail business domain if the catch-all functionality is enabled for this domain. I implemented that in the code.

##### 06/06/2023:
  - Protonmail added a new field and a cookie for API requests: "x-pm-uid" and "AUTH-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX". With the tests I've done, these values must be generated one and then can be reused over time.
  - Added regex to check emails syntax
  - Business email addresses are now detected both in light mode and with selenium. In light mode it only gives an idea if a domain is a business domain used with protonmail but can't determine if email exists. You must you the selenium version to be sure of that (with username and password).
  - Changed print format to be more python3 friendly


This 2.0 version introduces a new 'mode': Light mode.

Thanks to @Nenaff_ (Twitter account banned), I knew it was possible to request the verification of an email without the use of selenium.<br/>
This is way faster but if you have a lot of email addresses to verify you'll be blocked after 100 requests (don't know precisely how much time but at least more than an hour).<br/>
The solution is either to use a proxy to bypass this limitation or use the other mode of NeutrOSINT which uses username and password (but you need to have a valid account - you can create one for free).


---
# Notes

- API limit with light mode: 100 requests per hour.
- Free protonmail accounts are limited to 100 entries for 'To' field. But the tool handles this. It just takes a bit more time.
- If the string 'None' appears in the creation date for valid accounts then it means the API limit is probably reached. Since this is not the same API as for the light mode, here we have only 16 requests per hour.
- For some obscure reasons, sometimes selenium isn't able to get access to the 'New Email' button. In this case it is recommended to run the script again.
- The date related to a Protonmail account is not always its creation date. It is related to the PGP keys. When an account is created, a key pair is generated and so the creation date is the same as these. But if the account owner regenerates the key, the date will match the new ones.
- If you are using the selenium mode with an account and that account has MFA enabled, you cannot connect to it using selenium (might be implemented in the future -> PR are open :p).
- PGP keys are not always related to the account creation date. It is possible to generate new key pairs. In that case, the date of creation will be these new keys! The date corresponds to the key pair in the Protonmail account set as `primary`.

---
# How to use?

### Installation

You must have Chrome Browser installed on your machine:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```
Tested on Ubuntu 20.04.4 LTS x64 and Kali Linux 2021.1 x64

If you haven't used the tool for a long time, I recommend to double check if you have the latest version of Chrome installed on your machine. Otherwise, you may encounter errors.

### Prerequisites

Clone this repository:
```bash
git clone https://github.com/Kr0wZ/NeutrOSINT
cd NeutrOSINT
```

[+] RECOMMENDED: Easy install to use NeutrOSINT anywhere on your system:
```bash
pip install -e .
```

Or classic install:
```bash
pip install -r requirements.txt
```

You must have a valid Protonmail account to use the selenium mode.
But you can also you the light mode (-l) which uses the Protonmail API without the need to create a Protonmail account.


### Usage:
Show help message:
```bash
python3 main.py -h
neutrosint -h
```

Run the light mode using the protonmail API:
```bash
python3 main.py -l -e 'EMAIL_TO_VERIFY' 
neutrosint -l -e 'EMAIL_TO_VERIFY'
```

Or:
```bash
python3 main.py -e 'EMAIL_TO_VERIFY'
neutrosint -e 'EMAIL_TO_VERIFY'
```

Or:
```bash
python3 main.py -e 'USERNAME_TO_TEST'
neutrosint -e 'USERNAME_TO_TEST'
```

Example for username search:
```bash
neutrosint -e "test"
```

It will search for:
- `test@proton.me`
- `test@protonmail.com`
- `test@pm.me`
- `test@protonmail.ch`
- `test@passmail.net`

Print the public key used by a specific existing email:
```bash
python3 main.py -e 'EMAIL_TO_VERIFY' -k
neutrosint -e 'EMAIL_TO_VERIFY' -k
```

Run with selenium by specifying username and password (useful if you are rate limited by the API with the light mode):
```bash
python3 main.py -u 'USERNAME' -p 'PASSWORD' -f 'FILE_CONTAING_EMAILS.txt'
neutrosint -u 'USERNAME' -p 'PASSWORD' -f 'FILE_CONTAING_EMAILS.txt' 
```

---
# How does it work?

The light mode calls the Protonmail API at this endpoint: https://account.proton.me/api/users/available <br/>
Depending on the status code, we can determine if an email address already exists or not.

But since May, 2023 it now needs a valid AUTH token to perform requests to the API. <br>
This token is generated in the `generate_auth_cookie` function. <br>
First, request an API access token to https://account.proton.me/api/auth/v4/sessions <br>
Then, get a valid AUTH cookie through https://account.proton.me/api/core/v4/auth/cookies <br>

The selenium mode uses selenium with the given credentials to connect to protonmail, go to 'New Email', then fills in the 'To' field with all the email addresses to check.

---

# Support

Do you want to support me?

You can buy me a coffee here:
<a href="https://www.buymeacoffee.com/krowz" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50" ></a> 


Thanks in advance to anyone donating ❤️

---

# Special thanks

S/O to [f0rked](https://github.com/yetanotherf0rked) for his contribution to this project!