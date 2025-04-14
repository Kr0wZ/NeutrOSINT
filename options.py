import argparse
import neutrosint as nt
import sys

class Options:
	def __init__(self):
		self.parser = None
		self.args = None
		self.neutrosint = nt.NeutrOSINT()

	def build_arg_parser(self):
		epilog = "python3 main.py -u 'MY_USER' -p 'MY_PASSWORD' -f ./emails.txt"
		self.parser = argparse.ArgumentParser(description="Made by KrowZ", epilog=epilog, argument_default=argparse.SUPPRESS)

		#Group where options cannot be called together
		exclusive_group_actions = self.parser.add_mutually_exclusive_group()

		self.parser.add_argument("-l", "--light", action="store_true", help="Light mode in which we call the API instead of connecting with credentials. Useful when few emails to check")
		self.parser.add_argument("-u", "--username", metavar="USERNAME", type=str, help="Username to connect to your ProtonMail account")
		self.parser.add_argument("-p", "--password", metavar="PASSWORD", type=str, help="Password to connect to your ProtonMail account")

		exclusive_group_actions.add_argument("-f", "--file", metavar="FILE", type=str, help="Specify containing list of emails to check")
		exclusive_group_actions.add_argument("-e", "--email", metavar="EMAIL", type=str, help="Check existence of this email")

		self.parser.add_argument("-k", "--key", action="store_true", help="Print the public PGP key for that email account")
		self.parser.add_argument("-o", "--output", metavar="FILE", type=str, help="File where results are stored")
		self.parser.add_argument("-P", "--proxy", metavar="IP:PORT", type=str, help="IP:PORT of proxy to make requests. To use Tor, you must have installed it and specify '127.0.0.1:9050' as proxy")


		self.args = self.parser.parse_args()

		#If none of these arguments is used
		if("light" in self.args and ("username" in self.args or "password" in self.args)):
			self.parser.error("Error! You must specify either the light mode -l/--light or the credentials (-u/--username and -p/--password)")

        #If username is used without password or inversely
		if ("username" in self.args) ^ ("password" in self.args):
			self.parser.error("Error! You must specify both username and password.")

		if(not "file" in self.args and not "email" in self.args):
			self.parser.error("Error! You must specify one of the two options: -f/--file or -e/--email")


	def get_args(self):
		return self.args

	def run(self):

		if("username" in self.args and "password" in self.args):
			self.neutrosint.set_username(self.args.username)
			self.neutrosint.set_password(self.args.password)
		else:
			print("username and password not specified, using light mode...")
			self.neutrosint.set_light_mode(True)

		if("proxy" in self.args):
			self.neutrosint.set_proxy(self.args.proxy)

		if("email" in self.args):
			self.neutrosint.set_email(self.args.email)
			if("output" in self.args):
				self.neutrosint.set_output_file(self.args.output)

		elif("file" in self.args):
			self.neutrosint.load_emails(self.args.file)
			if("output" in self.args):
				self.neutrosint.set_output_file(self.args.output)

		if("key" in self.args):
			self.neutrosint.set_key(self.args.key)

		self.neutrosint.run()

if (__name__ == "__main__"):
	options = Options()
	options.build_arg_parser()