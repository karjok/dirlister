#!/bin/python3

# DIRLISTer - Directory Listing Downloader
# September 13th, 2024 01:42 AM WIB

import os
import re
from datetime import datetime
from urllib.parse import urlparse, urlunparse, unquote
import requests
import bs4

reset = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
grey = "\033[90m"

# add new or remove the file extension if necessary
file_extensions = ["txt", "doc", "docx", "pdf", "csv", "xls", "xlsx", "ppt", "pptx", "html", "htm", "json", "xml", "jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg", "mp3", "wav", "mp4", "mov", "avi", "mkv", "zip", "tar", "gz", "rar", "7z", "py", "js", "css", "php", "cpp", "c", "java", "go", "rb", "sh", "exe", "bat", "dll", "iso", "sql", "db", "sqlite", "mdb", "accdb","flv", "swf", "webp"]
has_been_processed_urls = []

local_dl_path = os.getcwd() + "/dirlister_result_files/"

stop = False
index = 1

def banner():
	os.system("clear")
	banner_text = f"""

         {green}█▀▄  █  █▀█  █░░  █  █▀  ▀█▀{reset}  █▀▀  █▀█
         {green}█▄▀  █  █▀▄  █▄▄  █  ▄█  ░█░{reset}  ██▄  █▀▄
         {green}|
         {green}├───{reset} Directory
         {green}│        └────── {reset}Listing
         {green}└──────────────────────────{reset} Downloader


{green}Current Download Path:{reset} {local_dl_path}
"""
	print(banner_text)
def create_folder_for(target_url):
	path = target_url
	paths = local_dl_path.split("/") +[p for p in path.split("/")[:-1] if p]
	full_path = "/".join(local_dl_path.split("/")+[p for p in path.split("/") if p])
	final_path = "/".join(paths)
	for i in range(0,len(paths)+1):
		if path[:i]: 
			try:
				os.mkdir('/'.join(paths[:i]))
			except:
				pass
	return final_path, full_path

def download_file(remote_file_path, indent=8, use_ssl=True):
	global index
	file_name = remote_file_path.split("/")[-1]
	target_path = create_folder_for(remote_file_path[remote_file_path.find(":")+1:])
	timestamps = datetime.now().strftime("%H:%M:%S")
	indent = indent if len(str(index)) <= indent else 10
	indent = " " * (indent - len(str(index)) )


	if file_name not in os.listdir(target_path[0]):
		try:
			downloaded_size = 0
			file = requests.get(remote_file_path, verify=use_ssl, stream=True)
			content_length = int(file.headers.get('content-length',0))
			if file.status_code == 200 and content_length > 0:
				with open(os.path.join(target_path[0], file_name), 'wb') as saved_file:
					for content_chunk in file.iter_content(chunk_size=1024):
						if content_chunk:
							print(f"\r{indent} {grey}{index}{reset}[{green}{timestamps}{reset}] ({file.headers.get('content-type', '-')}) {file_name} {round(content_length/1024)}/{round(downloaded_size/1024)} KB", end="", flush=True)
							saved_file.write(content_chunk)
							downloaded_size += len(content_chunk)
				dl_message = f" {green}OK{reset}"
				index += 1
			else:
				dl_message = f" {red}Error {file.status_code}{reset}"
			
		except Exception as e:
			dl_message = e
	
	else:
		dl_message = f"{indent} {grey}{index}{reset}[{yellow}{timestamps}{reset}] File {yellow}{file_name}{reset} already exist on download folder {local_dl_path}. {yellow}SKIP{reset}"
		index += 1
	return dl_message


def get_remote_file_path(dir_list_url, use_ssl=True):
	response = requests.get(dir_list_url, verify=use_ssl)
	host_url = urlparse(response.url)
	dir_list_base_url = host_url.scheme+"://"+host_url.netloc

	all_urls = []
	all_urls_json = []

	if response.status_code == 200 and "index of" in response.text.lower():
		html = bs4.BeautifulSoup(response.text, 'html.parser')
		a_tags = html.findAll('a')

		for a in a_tags:
			href = a.get('href') if a.text.lower() not in ["parent directory", "name", "last modified", "size", "description"] else ""
			if href:
				if host_url.path not in href:
					href = "/".join([i for i in host_url.path.split("/") if i] + [i for i in href.split("/") if i])
				is_file = any([href.lower().endswith("."+ext) for ext in file_extensions])
				is_absolute = False if href.startswith(dir_list_base_url) else True
				full_href = urlunparse((host_url.scheme, host_url.netloc, href, '', '', '')) if is_absolute else href
				path = urlparse(full_href).path
				if full_href.startswith(dir_list_base_url) and path != "/":
					if full_href not in all_urls:
						all_urls_json.append({'is_file': is_file, 'url': unquote(full_href)})
						all_urls.append(full_href)
	return all_urls_json

def perform_process(url, use_ssl=True):
	global stop, index
	path = urlparse(url)
	indent = 8
	if not stop:
		print(f"[{green}INF{reset}] 📂 Remote folder found: {green}{path.path}{reset}, Scanning file(s)..")
		urls = get_remote_file_path(url)
		for item in urls:
			try:
				if item['is_file']:
					download_message = download_file(item['url'], indent=indent)
					print(download_message)
				else:
					if item['url'] not in has_been_processed_urls:
						has_been_processed_urls.append(item['url'])
						perform_process(item['url'])
			except:
				stop = True
				break
	else:
		exit(0)

def main(url):
	use_ssl = True
	print(f"[{green}INF{reset}] Checking connection to {green}{url}{reset}..")
	try:
		def ask_q(question):
			answer = input(question+f" {yellow}y{reset}/{yellow}N{reset}: ")
			if answer.lower() == "y":
				return True
			return False
		check = requests.get(url, verify=use_ssl)
		code = check.status_code
		is_directory_listing = "index of" in check.text.lower()
		if code == 200:
			print(f"[{green}INF{reset}] Connection estabilished !")
			continue_ = True
		else:
			continue_ = ask_q(f"[{yellow}WRN{reset}] The server responded with code {code}, are you sure to continue ?")
		if not is_directory_listing:
			continue_ = ask_q(f"[{yellow}WRN{reset}] Your given URL looks like not containing 'Index Of' string that indicate the directory listing. Are you sure want to continue ?")
	except Exception as err:
		if "SSLError" in str(err):
			print(f"[{yellow}WRN{reset}] SSL Error occured. Automating perform request with no SSL..")
			continue_ = True
			use_ssl = False
		else:
			continue_ = ask_q(f"[{yellow}WRN{reset}] Failed connecting to the server with error {green}{err}{reset} . Are you sure want to continue ?")
	if continue_:
		perform_process(url, use_ssl=use_ssl)

def dirlister():
	banner()
	try:
		url = input(f"[{green}INP{reset}] Input your directory listig URL: ")
		while not url:
			url = input(f"[{yellow}WRN{reset}] Please input the target directory URL ex {green}https://youtargetsite.com/uploads{reset}, CTRL + C to exit: ")
		main(url)
	except:
		exit(0)


if __name__=="__main__":
	dirlister()
