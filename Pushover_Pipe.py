#!/usr/bin/python

"""
* Pushover Pipe
* for Python 3
* 
* http://github.com/robotmachine/Pushover_Pipe
*
* This program is free software. It comes without any warranty, to
* the extent permitted by applicable law. You can redistribute it
* and/or modify it under the terms of the Do What The Fuck You Want
* To Public License, Version 2, as published by Sam Hocevar. See
* http://sam.zoy.org/wtfpl/COPYING for more details.
"""
import os, sys, urllib, http.client, configparser, textwrap, argparse

settings = os.path.expanduser("~/.pushpipe")
config = configparser.ConfigParser()
conn = http.client.HTTPSConnection("api.pushover.net:443")

def main():
	parser = argparse.ArgumentParser(description='Pushover thing', prog='Pushover Pipe')
	parser.add_argument('-u','--user',
		action='store', dest='user', default=None,
		help='User key instead of reading from settings. Requires --token.')
	parser.add_argument('-t','--token',
		action='store', dest='token', default=None,
		help='Token key instead of reading from settings. Requires --user.')
	parser.add_argument('-m','--message',
		action='store', dest='WORDS', default="Pushover Pipe",
		help='Message to send. Default is "Pushover Pipe"')
	parser.add_argument('-d','--device',
		action='store', dest='DEV', default=None,
		help='Device name to receive message. Default sends to all devices.')
	parser.add_argument('--title',
		action='store', dest='TITLE', default='Pushover_Pipe',
		help='Title or application name. Default is Pushover_Pipe')
	parser.add_argument('--url',
		action='store', dest='URL', default=None,
		help='Optional URL to accompany your message.')
	parser.add_argument('--urltitle',
		action='store', dest='UTITLE', default='Pushover Pipe URL',
		help='Title to go with your URL.')
	args = parser.parse_args()
	read_config(token=args.token, user=args.user, WORDS=args.WORDS, DEV=args.DEV, TITLE=args.TITLE, URL=args.URL, UTITLE=args.UTITLE)

def read_config(token, user, WORDS, DEV, TITLE, URL, UTITLE):
	if token is None and user is None:
		if os.path.exists(settings):
			config.read(settings)
			token = config['PUSHPIPE']['token']
			user = config['PUSHPIPE']['user']
			message(token, user, WORDS, DEV, TITLE, URL, UTITLE)
		if not os.path.exists(settings):
			set_config()
	elif token is not None and user is not None:
		message(token, user, WORDS, DEV, TITLE, URL, UTITLE)

def message(token, user, WORDS, DEV, TITLE, URL, UTITLE):
	if DEV is None and URL is None:
		conn.request("POST", "/1/messages.json",
			urllib.parse.urlencode({
				"token": token,
				"user": user,
				"title": TITLE,
				"message": WORDS,
			}), { "Content-type": "application/x-www-form-urlencoded" })
	if DEV is not None and URL is None:
		conn.request("POST", "/1/messages.json",
			urllib.parse.urlencode({
				"token": token,
				"user": user,
				"title": TITLE,
				"message": WORDS,
				"device": DEV,
			}), { "Content-type": "application/x-www-form-urlencoded" })
	if DEV is not None and URL is not None:
		conn.request("POST", "/1/messages.json",
			urllib.parse.urlencode({
				"token": token,
				"user": user,
				"title": TITLE,
				"message": WORDS,
				"device": DEV,
				"url": URL,
				"url_title": UTITLE,
			}), { "Content-type": "application/x-www-form-urlencoded" })
	response=conn.getresponse()
	if response.status is 200:
		print("Everything went well.")
	else:
		print("Oops. You bwoke it.")
		print("Pushover sez:", response.status, response.reason)

def set_config():
	print(textwrap.dedent("""
	You will need to create an app 
	with Pushover and provide the token.
	https://pushover.net/apps
	"""))
	token = input("API Token: ")
	print(textwrap.dedent("""
	Your user key is found on your 
	Pushover.net Dashboard	
	https://pushover.net
	"""))
	user = input("User Key: ")
	config ['PUSHPIPE'] = {'token': token,
			       'user': user}		
	with open(settings, 'w') as configfile:
		config.write(configfile)
	message(token, user)

main()