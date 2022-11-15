from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import os
import re
import requests
from datetime import datetime
from colorama import Fore, Style

#TODO

#Add exceptions -> verify if file exists (when loading emails) + proxy server if no connection available

class NeutrOSINT():
	def __init__(self):
		self.driver = None
		self.username = None
		self.password = None
		self.emails = []
		self.time = 16
		self.output_file = None
		self.proxy = None

	def banner(self):
		print("""

		 ██████   █████                      █████                 ███████     █████████  █████ ██████   █████ ███████████
		░░██████ ░░███                      ░░███                ███░░░░░███  ███░░░░░███░░███ ░░██████ ░░███ ░█░░░███░░░█
		 ░███░███ ░███   ██████  █████ ████ ███████   ████████  ███     ░░███░███    ░░░  ░███  ░███░███ ░███ ░   ░███  ░ 
		 ░███░░███░███  ███░░███░░███ ░███ ░░░███░   ░░███░░███░███      ░███░░█████████  ░███  ░███░░███░███     ░███    
		 ░███ ░░██████ ░███████  ░███ ░███   ░███     ░███ ░░░ ░███      ░███ ░░░░░░░░███ ░███  ░███ ░░██████     ░███    
		 ░███  ░░█████ ░███░░░   ░███ ░███   ░███ ███ ░███     ░░███     ███  ███    ░███ ░███  ░███  ░░█████     ░███    
		 █████  ░░█████░░██████  ░░████████  ░░█████  █████     ░░░███████░  ░░█████████  █████ █████  ░░█████    █████   
		░░░░░    ░░░░░  ░░░░░░    ░░░░░░░░    ░░░░░  ░░░░░        ░░░░░░░     ░░░░░░░░░  ░░░░░ ░░░░░    ░░░░░    ░░░░░    

			""")

	def setup(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument('--no-sandbox')

		if(self.proxy != None):
			chrome_options.add_argument('--proxy-server=%s' % self.proxy)

		service = Service(ChromeDriverManager().install())

		try:
			self.driver = webdriver.Chrome(service=service, options=chrome_options)
		except:
			print(Fore.RED + "[-] Error setting up the driver...")
			exit()

		self.driver.get('https://account.protonmail.com/login')

	def set_email(self, email):
		self.emails = [ email ]

	def set_username(self, username):
		self.username = username

	def set_password(self, password):
		self.password = password

	def set_output_file(self, file):
		self.output_file = file

	def set_proxy(self, proxy):
		self.proxy = proxy

	def load_emails(self, file):
		try:
			handle = open(file, 'r')
			lines = handle.read().splitlines()
			for line in lines:
				self.emails.append(line)

			handle.close()
		except:
			print(Fore.RED + "[-] Unable to load emails")
			exit()
		
	def write_to_file(self, data):
		try:
			handle = open(self.output_file, "a")
			handle.write(data)
			handle.close()
		except:
			print(Fore.RED + "[-] Unable to save data to file")
			exit()

	def login(self):
		try:
			print(Fore.YELLOW + "[?] Connecting to ProtonMail with credentials...")

			#Find the username field
			element = WebDriverWait(self.driver, self.time).until(EC.presence_of_element_located((By.ID, 'username')))
			user_element = self.driver.find_element(By.ID,'username')
			user_element.send_keys(self.username)

			#Find the password field
			element = WebDriverWait(self.driver, self.time).until(EC.presence_of_element_located((By.ID, 'password')))
			password_element = self.driver.find_element(By.ID,'password') 
			password_element.send_keys(self.password)

			#Submit the form
			password_element.submit()

			#Wait to connect to our account
			time.sleep(self.time)

			print(Fore.GREEN + "[+] Connected to ProtonMail\n")
		except:
			print(Fore.RED + "[-] Error when connecting to ProtonMail...")
			exit()


	def new_email(self):
		try:
			print(Fore.YELLOW + "[?] Accessing 'New email' to check email addresses...")
			#Retrieve the "New email" button
			element = WebDriverWait(self.driver, self.time).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="button button-large button-solid-norm w100 no-mobile"]')))
			new_email_element = self.driver.find_element(By.XPATH, '//button[@class="button button-large button-solid-norm w100 no-mobile"]')
			new_email_element.click()

			time.sleep(self.time)

			#Retrieve the "To" field to insert emails
			element = WebDriverWait(self.driver, self.time).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input')))
			to_email_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input')

			#Convert list to string + add "," at the end (for the last occurence to be updated)
			emails_to_check_str = ','.join(self.emails)
			emails_to_check_str += ','

			#Write all emails in the "To" field and wait until protonmail detects if they exist or not
			to_email_element.send_keys(emails_to_check_str)

			time.sleep(self.time)
			print(Fore.GREEN + "[+] Ready to check emails\n")
		except:
			print(Fore.RED + "[-] Unable to access new email to check email addresses")
			exit()


	def extract_timestamp(self, email):

		#We use requests here because selenium doesn't work???
		source_code = requests.get('https://api.protonmail.ch/pks/lookup?op=index&search=' + email)

		try:
			timestamp = re.sub(':', '', re.search(':[0-9]{10}::', source_code.text).group(0))
			creation_date = datetime.fromtimestamp(int(timestamp))

			return creation_date

		except AttributeError:
			print(Fore.RED + "[-] Error! Impossible to retrieve the creation date")
		

	def check_emails(self):
		try:
			print(Fore.YELLOW + "[?] Checking email addresses...\n" + Style.RESET_ALL)
			#Retrieve the emails we inserted in the input field
			element = WebDriverWait(self.driver, self.time).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div')))
			elements_to_loop = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div')

			#Remove the last div (which is always null)
			elements_to_loop = elements_to_loop[:-1]

			count = 0

			#Loop over all divs
			for item in elements_to_loop:
				#foreach retrieve their classes
				class_str = item.get_attribute('class')
				if("invalid" in class_str):
					if(self.output_file != None):
						self.write_to_file("Invalid email: " + self.emails[count] + "\n")
					print(Fore.RED + "[-] Invalid email: " + self.emails[count] + Style.RESET_ALL)
				else:
					creation_date = self.extract_timestamp(self.emails[count])
					if(self.output_file != None):
						self.write_to_file("Valid email: " + self.emails[count] + " - Creation date: " + str(creation_date) + Style.RESET_ALL + "\n")
					print(Fore.GREEN + "[+] Valid email: " + self.emails[count] + " - Creation date: " + str(creation_date))

				count = count + 1
		except UnexpectedAlertPresentException:
			print(Fore.RED + "[-] Unable to check emails addreses...")
			exit()

	def close(self):
		self.driver.close()

	def run(self):
		self.banner()
		self.setup()
		self.login()
		self.new_email()
		self.check_emails()
		self.close()
