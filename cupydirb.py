# import ArgumentParser for- parsing arguments
from argparse import ArgumentParser
# import Thread class from threading library for multithreading
from threading import Thread
# get requests for checking if dir exists
from requests import get
# allows for a niiiiice clean exit
from sys import exit

# function used for brute forcing
# takes in a url and content to iterate over, returns None
def brute_force(url: str, content: list) -> None:
	# for each directory in the list given
	for directory in content:
		# if it already starts with a /, remove it
		if(directory[0] == "/"):
			directory = directory[1:len(directory)]

		# define the current url as the url given plus the current directory
		current_url = "{}/{}".format(url, directory)
		# define the status as the status code returned by the GET request on the page
		status = get(current_url).status_code

		# if it starts with 1, informational response
		if(str(status)[0] == '1'):
			print("[+] {} -> {}".format(current_url, status))

		# if it starts with 2, success response
		if(str(status)[0] == '2'):
			print("[+] {} -> {}".format(current_url, status))

# function for checking the url is valid
# returns True or False
def check_url(url: str) -> bool:
	try:
		# try to send a GET request to the url, obtaining headers
		get(url).headers
		# return True if possible
		return(True)

	# if something goes wrong
	except Exception:
		# return False
		return(False)

# function for checking the wordlist provided is valid, returns True or False
def check_wordlist(wordlist: str) -> bool:
	try:
		# try to open the file and then close it
		open(wordlist, "r").close()
		# return True if possible
		return(True)

	# if something goes wrong
	except Exception:
		# return False
		return(False)

# function for parsing the arguments passed to the program, returns a tuple
def parse_args() -> tuple:
	# define arg_parser object from ArgumentParser class, defining a couple things such as the description and epilog
	arg_parser = ArgumentParser(description="[!] Tool for brute forcing web directories! [!]", epilog="[!] Enjoy ^^ [!]")
	
	# add arguments for the wordlist (--wordlist) and target url (--url)
	arg_parser.add_argument('-w', '--wordlist', metavar='wordlist', action="store", type=str, help="File to use for directory search", required=True)
	arg_parser.add_argument('-u', '--url', metavar='url', action="store", type=str, help="URL to brute force", required=True)

	# use the parse_args() method to define the arguments passed
	args = arg_parser.parse_args()

	# return them from the function
	return(args.url, args.wordlist)

# store the values into variables
url, wordlist = parse_args()

# using our functions, check if the values passed are valid
if(not check_url(url)):
	print("[-] Unable to connect to target URL :(")
	exit()

# again, with the wordlist
if(not check_wordlist(wordlist)):
	print("[-] Unable to open wordlist file :(")
	exit()

# epic message :)
print("[!] Web directory brute forcer! [!]")
print("[#] Written by cupycake-png ^^ [#]\n\n")

# displaying information passed in
print("Target Url >> {}\nWordlist >> {}\n-----------------".format(url, wordlist))


try:
	# try to get the full content of the wordlist, reading it and splitting it
	full_content = open(wordlist, "r").read().split("\n")
	# splitting it in half
	half_1 = full_content[len(full_content) // 2:]
	half_2 = full_content[:len(full_content) // 2]

	# defining a thread for each half to run simultaneously
	thread1 = Thread(target=brute_force, args=(url, half_1))
	# start thread
	thread1.start()

	# defining another thread for the second half
	thread2 = Thread(target=brute_force, args=(url, half_2))
	# starting the thread
	thread2.start()

# if CTRL+C is pressed, display and exit
except KeyboardInterrupt:
	print("[-] Brute force ended by user")
	exit()