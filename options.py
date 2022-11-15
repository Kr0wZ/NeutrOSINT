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

		self.parser.add_argument("-u", "--username", metavar="USERNAME", required=True, type=str, help="Username to connect to your ProtonMail account")
		self.parser.add_argument("-p", "--password", metavar="PASSWORD", required=True, type=str, help="Password to connect to your ProtonMail account")

		exclusive_group_actions.add_argument("-f", "--file", metavar="FILE", type=str, help="Specify containing list of emails to check")
		exclusive_group_actions.add_argument("-e", "--email", metavar="EMAIL", type=str, help="Check existence of this email")

		self.parser.add_argument("-o", "--output", metavar="FILE", type=str, help="File where results are stored")
		self.parser.add_argument("-P", "--proxy", metavar="IP:PORT", type=str, help="IP:PORT of proxy to make requests. To use Tor, you must have installed it and specify '127.0.0.1:9050' as proxy")


		self.args = self.parser.parse_args()

		if(not "file" in self.args and not "email" in self.args):
			self.parser.error("Error! You must specify one of the two options: -f/--file or -e/--email")


	def get_args(self):
		return self.args

	def run(self):

		self.neutrosint.set_username(self.args.username)
		self.neutrosint.set_password(self.args.password)

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

		self.neutrosint.run()

if (__name__ == "__main__"):
	options = Options()
	options.build_arg_parser()