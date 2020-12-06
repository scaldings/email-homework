import imaplib
import email
import os
import creds



def check_mails():
	imap = imaplib.IMAP4_SSL('imap.gmail.com')
	imap.login(creds.email, creds.password)
	messages = imap.select('INBOX')
	for msg in messages:
		print(msg)


if __name__ == '__main__':
	check_mails()