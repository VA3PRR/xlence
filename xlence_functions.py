from os import walk
import xlence_app as xlence
from xlence_classes import Template
from bs4 import BeautifulSoup as bs

def parse_digest():
	digest_data = xlence.digest_data
	digest = {}
	messages = digest_data.find_all("mime")
	for message in messages:
		message = message.text
		if "=0A" in message:
			#	WoAD replaces EOL character with = and LF with =0A
			message = message.replace("=\n","").replace("=0A","\n")
		message = message.split("\n")
		message_date = message[0].replace("Date: ","").replace(" +0000","")
		message_sender = find_callsign(message[1])
		message_subject = message[2]
		start_index = 0
		end_index = 0
		i = 0
		for line in message:
			if start_index == 0 and line.startswith("--boundary"):
				start_index = i+3
				continue
			elif i > start_index and line.startswith("--boundary"):
				end_index = i
				break
			i+=1
		message_text = message[start_index:end_index:]
		message_text = "\n".join([i for i in message_text if i])	#	remove empty keys and join
		if message_sender not in digest:
			digest[message_sender] = [
					{
						"date":		message_date,
						"subject":	message_subject,
						"message":	message_text,
					}
				]
		else:
			entrynum = len(digest[message_sender])+1
			digest[message_sender].append(
				{
					"date":		message_date,
					"subject":	message_subject,
					"message":	message_text,
				}
			)
	xlence.digest = digest

def find_callsign(address):
	address = address.replace("From: ","").replace("@winlink.org","").upper()
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	extras = ""
	for character in address[5:-1:-1]:
		if character not in chars:
			continue
		extras += character
	return address.replace(extras,"")

def buildTemplates():
	#	Scan Templates Directory for text and html files
	templates_directory = "static/templates/"
	text_files = []
	html_files = []
	for root,dirs,files in walk(templates_directory):
		for file in files:
			ext = file.split(".")[-1].lower()
			file_path = str(root+"/"+file)
			if ext in ("htm","html"):
				html_files.append(file_path)
			elif ext == "txt":
				text_files.append(file_path)
	#	Build templates based on text files
	templates = {}
	success = 0
	fail = 0
	for txt in text_files:
		if "Changelog.txt" not in txt and "Standard_Forms_Version.dat" not in txt:
			name = txt.replace(".txt","").split("/")
			root = name[-2]
			name = name[-1]
			try:
				 templates[name] = [root,Template(name,txt)]
				 success+=1
			except Exception as e:
				fail+=1
				continue
	print("\nTemplates built:",success,"\n\rFailed to build:",fail)
	return templates