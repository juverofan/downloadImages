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
	soup = BS(r.text)
	imglink = []
	for imgtag in soup.find_all('img'):
		if imgtag['src'] not in imglink:
			imglink.append(imgtag['src'])
	for imgtag in soup.find_all('a'):
		if imgtag['href'] not in imglink and imgtag['href'].split(".")[len(imgtag['href'].split("."))-1].upper() in ["PNG","JPG","GIF","JPEG","BMP"]:
			imglink.append(imgtag['href'])

	#print(imglink)
	for img in imglink:
		print("Getting file: "+img)
		if(img.startswith("/")):
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
		#print(imgtag['src'])
	#print(r.text)
