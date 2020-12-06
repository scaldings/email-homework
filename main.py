import imaplib
import email
import os
import creds
import json
from datetime import datetime, date


def get_teacher_names():
	names = []
	with open('/home/lukas/Documents/Python/homework/names.txt', 'r') as file:
		names = file.read().split('\n')
	return names


def check_mails():
	mails = []
	imap = imaplib.IMAP4_SSL('imap.gmail.com')
	imap.login(creds.email, creds.password)
	status, messages = imap.select('INBOX')

	messages = int(messages[0])

	for x in range(messages, messages -15, -1):
		mail_info = []
		res, msg = imap.fetch(str(x), '(RFC822)')
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				subject = email.header.decode_header(msg['Subject'])[0][0]
				if isinstance(subject, bytes):
					subject = subject.decode()
				From, encoding = email.header.decode_header(msg.get('From'))[0]
				if isinstance(From, bytes):
					From = From.decode(encoding)
				date = msg['Date']
				mail_info.append(subject)
				mail_info.append(From)
				mail_info.append(date)
				if msg.is_multipart():
					for part in msg.walk():
						content_type = part.get_content_type()
						content_disposition = str(part.get('Content-Disposition'))
						try:
							body = part.get_payload(decode=True).decode()
						except:
							pass
						if content_type == 'text/plain':
							mail_info.append(body)
				else:
					content_type = msg.get_content_type()
					body = msg.get_payload(decode=True).decode()
					if content_type == 'text/plain':
						mail_info.append(body)
		mails.append(mail_info)
	imap.close()
	imap.logout()
	return mails


def filter_mails(mails: list):
	valid_mails = []
	for mail in mails:
		valid_mail_info = []
		subject = mail[0]
		From = mail[1]
		date = mail[2]
		body = mail[3]

		if '<' in From:
			From = From.split(' <')[0]

		if 'Re:' not in subject:
			if 'Fwd:' not in subject:
				if From in get_teacher_names():
					if 'zoom' not in body:
						valid_mail_info.append(subject)
						valid_mail_info.append(From)
						valid_mail_info.append(date)
						valid_mail_info.append(body)
						valid_mails.append(valid_mail_info)
	return valid_mails


def format_mails(mails: list):
	formatted_mails = []
	for mail in mails:
		formatted_mail = []
		formatted_mail.append(f'Subject: {mail[0]}')
		formatted_mail.append(f'From: {mail[1]}')
		formatted_mail.append(f'Date: {format_mail_date(mail[2])}')
		formatted_mail.append(f'Body: {mail[3]}')
		formatted_mails.append(formatted_mail)
	return formatted_mails


def format_mail_date(date: str):
	date_temp = date.split(', ')[1]
	date_temp = date.split(' ')
	return f'{date_temp[0]} {date_temp[1]} {date_temp[2]}'


if __name__ == '__main__':
	mails = format_mails(filter_mails(check_mails()))
	print('*'*100)
	if len(mails) != 0:
		for mail in mails:
			for x in mail:
				print(x)
			print('*'*100)
	else:
		print('No assignments!')