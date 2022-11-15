import options


def main():
	#Setup parser
	opt = options.Options()
	opt.build_arg_parser()
	opt.run()

if(__name__ == "__main__"):
	main()