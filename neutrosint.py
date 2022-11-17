from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

import time
import os
import re
import requests
from datetime import datetime
from colorama import Fore, Style

#Check if the number of emails to verify is greater than 100. In the case where the user uses the light mode, print a message saying that all email addresses won't be able to be tested. Redirect the user
#to the credentials mode.
#If the user uses the credentials mode then check if more than 100 email addresses. If yes then automatically remove from the field from 'To' once we reach the limit and do it again until there
#are no more email addresses to verify

class NeutrOSINT():
	def __init__(self):
		self.driver = None
		self.username = None
		self.password = None
		self.emails = []
		self.time = 16
		self.output_file = None
		self.proxy = {}
		self.light = False
		self.max_retries = 0

	def banner(self):
		print("""

		  ██████   █████                      █████                 ███████     █████████  █████ ██████   █████ ███████████                 ████████ 
		 ░░██████ ░░███                      ░░███                ███░░░░░███  ███░░░░░███░░███ ░░██████ ░░███ ░█░░░███░░░█                ███░░░░███
		  ░███░███ ░███   ██████  █████ ████ ███████   ████████  ███     ░░███░███    ░░░  ░███  ░███░███ ░███ ░   ░███  ░     █████ █████░░░    ░███
		  ░███░░███░███  ███░░███░░███ ░███ ░░░███░   ░░███░░███░███      ░███░░█████████  ░███  ░███░░███░███     ░███       ░░███ ░░███    ███████ 
		  ░███ ░░██████ ░███████  ░███ ░███   ░███     ░███ ░░░ ░███      ░███ ░░░░░░░░███ ░███  ░███ ░░██████     ░███        ░███  ░███   ███░░░░  
		  ░███  ░░█████ ░███░░░   ░███ ░███   ░███ ███ ░███     ░░███     ███  ███    ░███ ░███  ░███  ░░█████     ░███        ░░███ ███   ███      █
		  █████  ░░█████░░██████  ░░████████  ░░█████  █████     ░░░███████░  ░░█████████  █████ █████  ░░█████    █████        ░░█████   ░██████████
		 ░░░░░    ░░░░░  ░░░░░░    ░░░░░░░░    ░░░░░  ░░░░░        ░░░░░░░     ░░░░░░░░░  ░░░░░ ░░░░░    ░░░░░    ░░░░░          ░░░░░    ░░░░░░░░░░ 

			""")

	def setup(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument('--no-sandbox')

		if(len(self.proxy) != 0):
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

	def set_light_mode(self, light):
		self.light = light

	def load_emails(self, file):
		try:
			handle = open(file, 'r')
			lines = handle.read().splitlines()
			for line in lines:
				self.emails.append(line)

			handle.close()

			#Tell the user the API limit will be exceeded
			if(len(self.emails) < 100):
				if(self.light):
					print(Fore.YELLOW + "[?] Warning! There are more than 100 email addresses to check. The API's limit is 100 requests. All the email addresses won't be tested. You can either use the credentials mode (--username and --password) or use a proxy (--proxy)")

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

	def clear_element(self, method, element_path):
		try:
			wait_element = WebDriverWait(self.driver, self.time).until(EC.presence_of_element_located((method, element_path)))
			element = self.driver.find_element(method, element_path)
			element.clear()
		except:
			print(Fore.RED + "[-] Unable to clear the element")
			exit()

	def new_email(self):
		try:
			print(Fore.YELLOW + "[?] Accessing 'New email' to check email addresses...")
			#Retrieve the "New email" button
			element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="button button-large button-solid-norm w100 no-mobile"]')))
			new_email_element = self.driver.find_element(By.XPATH, '//button[@class="button button-large button-solid-norm w100 no-mobile"]')
			new_email_element.click()

			time.sleep(self.time)

			#Retrieve the "To" field to insert emails
			element = WebDriverWait(self.driver, self.time).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input')))
			to_email_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input')

			print(Fore.YELLOW + "[?] Checking email addresses...\n" + Style.RESET_ALL)

			#Create a copy of emails to avoid the modifications
			tmp_emails_array = self.emails[:]

			while(len(tmp_emails_array) > 100):
				#Check the first 100 emails
				emails_to_check_str = ','.join(tmp_emails_array[:100])
				#Convert list to string + add "," at the end (for the last occurence to be updated)
				emails_to_check_str += ','

				#Write all emails in the "To" field and wait until protonmail detects if they exist or not
				to_email_element.send_keys(emails_to_check_str)

				self.check_emails(tmp_emails_array[:100])

				#Remove the first 100 email addresses
				tmp_emails_array = tmp_emails_array[100:]
				#Clear the 'To' field
				to_email_element.clear()

			#If we are here it means there are less than 100 email addresses
			emails_to_check_str = ','.join(tmp_emails_array)
			#Convert list to string + add "," at the end (for the last occurence to be updated)
			emails_to_check_str += ','
			

			#Write all emails in the "To" field and wait until protonmail detects if they exist or not
			to_email_element.send_keys(emails_to_check_str)
			self.check_emails(tmp_emails_array)

		except TimeoutException:
			if(self.max_retries == 1):
				print(Fore.RED + "[-] Too many retries. Try to launch the script again")
				exit()
			self.max_retries = self.max_retries + 1
			print(Fore.RED + "[-] Unable to access new email to check email addresses. Trying again...")
			self.new_email()
			


	def extract_timestamp(self, email):

		#We use requests here because selenium doesn't work???
		source_code = requests.get('https://api.protonmail.ch/pks/lookup?op=index&search=' + email)

		try:
			timestamp = re.sub(':', '', re.search(':[0-9]{10}::', source_code.text).group(0))
			creation_date = datetime.fromtimestamp(int(timestamp))

			return creation_date

		except AttributeError:
			#print(Fore.RED + "[-] Error! Impossible to retrieve the creation date. Maybe API restriction...")
			return None
		

	#Pass emails as argument to use for printing (pass tmp_emails_array)
	def check_emails(self, emails):
		try:
			#print(Fore.YELLOW + "[?] Checking email addresses...\n" + Style.RESET_ALL)
			#Retrieve the emails we inserted in the input field
			element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div/div[2]/div/div/div/div/div/div')))
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
						self.write_to_file("Invalid email: " + emails[count] + "\n")
					print(Fore.RED + "[-] Invalid email: " + Style.RESET_ALL + emails[count])
				else:
					creation_date = self.extract_timestamp(emails[count])
					if(self.output_file != None):
						self.write_to_file("Valid email: " + emails[count] + " - Creation date: " + str(creation_date) + "\n")
					print(Fore.GREEN + "[+] Valid email: " + Style.RESET_ALL + emails[count] + " - Creation date: " + str(creation_date))

				count = count + 1
		except UnexpectedAlertPresentException:
			print(Fore.RED + "[-] Unable to check emails addreses...")
			exit()
		except IndexError:
			pass

	def close(self):
		self.driver.close()

	def request_api(self):
		for email in self.emails:
			try:
				request = requests.get("https://account.proton.me/api/users/available", 
					headers={
						"x-pm-appversion":"web-account@5.0.11.11",
						"x-pm-locale":"en_US"
					},
					params={
						"Name":email,
						"ParseDomain":"1"
					},
					proxies=self.proxy)

				#Return code 429 = API limite exceeded
				if(request.status_code == 409):
					creation_date = self.extract_timestamp(email)
					if(self.output_file != None):
						self.write_to_file("Valid email: " + email + " - Creation date: " + str(creation_date) + "\n")
					print(Fore.GREEN + "[+] Valid email: " + Style.RESET_ALL + email + " - Creation date: " + str(creation_date))

				elif(request.status_code == 429):
					print(Fore.RED + "[-] API requests limit exceeded... Try with the credentials mode (--username and --password) or use a proxy (--proxy)")
				else:
					if(self.output_file != None):
						self.write_to_file("Invalid email: " + email + Style.RESET_ALL + "\n")
					print(Fore.RED + "[-] Invalid email: " + Style.RESET_ALL + email)

			except:
				print("Error when requesting the API")


	def run(self):
		try:
			self.banner()

			#Check if we are running in light mode
			if(self.light):
				self.request_api()
			else:
				self.setup()
				self.login()
				self.new_email()
				self.close()
		except KeyboardInterrupt:
			print(Fore.YELLOW + "[?] Exiting..." + Style.RESET_ALL)
			return