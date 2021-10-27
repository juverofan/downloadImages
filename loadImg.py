#Author: Juverofan

from os import listdir
from os.path import isfile, join
import os
import sys
import platform
import subprocess
import requests
import time
from bs4 import BeautifulSoup as BS
import array as arr
import random
import base64
import string

import argparse
parser = argparse.ArgumentParser() 

parser.add_argument("-u", "--url", help="URL")
parser.add_argument("-o", "--output", help="output")
args = parser.parse_args()


output = "output"
if args.output:
	output = args.output
if(not os.path.isdir(output)):
	os.system("mkdir "+output)
	


url = args.url 
if url.count("/") == 2:
	url = url + "/"
if not url.lower().startswith("http"):
	print("URL not correct.")
else:
	path = url.split("/")[len(url.split("/"))-1]
	path = url.replace(path,"")
	domains = url.split("/")
	domain = "" 
	i = 0
	while i < 3:
		domain += domains[i]+"/"
		i += 1 
	print("Domain: " + domain+"\n")
	print("Path: "+path)
	r = requests.get(url)
	soup = BS(r.text, "html.parser")
	imglink = []
	for imgtag in soup.find_all('img'):
		if imgtag['src'] not in imglink:
			imglink.append(imgtag['src'])
	for imgtag in soup.find_all('a',href=True):
		#print(imgtag)
		if imgtag['href'] not in imglink and imgtag['href'].split(".")[len(imgtag['href'].split("."))-1].upper() in ["PNG","JPG","GIF","JPEG","BMP"]:
			imglink.append(imgtag['href'])

	#print(imglink)
	
	for img in imglink:
		print("Getting file: "+img)
		wl = 0
		if(img.split(".")[len(img.split("."))-1].upper() not in ["PNG","JPG","GIF","JPEG","BMP"]):
			wl = 1
			if(img.split(".")[len(img.split("."))-1].upper().startswith(("PNG","JPG","GIF","JPEG","BMP")) ):
				ext = "JPG"
				print("Modifying the link to: ")
				if img.split(".")[len(img.split("."))-1].upper().startswith("PNG"):
					ext = "PNG"
				elif img.split(".")[len(img.split("."))-1].upper().startswith("JPG"):
					ext = "JPG"
				elif img.split(".")[len(img.split("."))-1].upper().startswith("GIF"):
					ext = "GIF"
				elif img.split(".")[len(img.split("."))-1].upper().startswith("JPEG"):
					ext = "JPEG"
				elif img.split(".")[len(img.split("."))-1].upper().startswith("BMG"):
					ext = "BMP"
				img = img.replace(img.split(".")[len(img.split("."))-1],"")
				img = img + ext
				print(img)
				wl = 0

		if "base64," in img:
			imgdata = base64.b64decode(img.split("base64,")[1])
			letters = string.ascii_lowercase
			filename = output+"/"+''.join(random.choice(letters) for i in range(10))+".jpg"
			print("base64 image save to "+filename)
			#filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
			with open(filename, 'wb') as f:
				f.write(imgdata)
		elif wl == 1:
			print("cannot download file")
		elif(img.startswith("/")):
			filename = img.split("/")[len(img.split("/"))-1]
			r = requests.get(domain.strip("/")+img, allow_redirects=True)
			open(output+"/"+filename, 'wb').write(r.content)
		elif img.lower().startswith("http"):
			filename = img.split("/")[len(img.split("/"))-1]
			r = requests.get(img, allow_redirects=True)
			open(output+"/"+filename, 'wb').write(r.content)
		else:
			filename = img.split("/")[len(img.split("/"))-1]
			r = requests.get(path.strip("/")+"/"+img, allow_redirects=True)
			open(output+"/"+filename, 'wb').write(r.content)
