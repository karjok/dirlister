#!/bin/python3

# DIRLISTer - Directory Listing Downloader
# September 13th, 2024 01:42 AM WIB

import os
import re
import signal
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse, urlunparse, unquote
import requests
import bs4

reset = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
grey = "\033[90m"

has_been_processed_urls = []
local_dl_path = os.getcwd() + "/dirlister_result_files/"

stop = False
all_scraped_urls = set()

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

def keyboard_interrupt_handler(signal,frame):
	import sys
	print(f"\n[{yellow}WRN{reset}] KeyboardInterrupt detected, stoping process")
	sys.exit(0)

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

def download_file(remote_file_path, use_ssl=True):
	file_name = remote_file_path.split("/")[-1]
	target_path = create_folder_for(remote_file_path[remote_file_path.find(":")+1:])
	timestamps = datetime.now().strftime("%H:%M:%S")

	if file_name not in os.listdir(target_path[0]):
		try:
			file = requests.get(remote_file_path, verify=use_ssl, stream=True)
			content_length = round(int(file.headers.get('content-length',0)) / 1024, 2) # in KB
			if file.status_code == 200 and content_length > 0:
				with open(os.path.join(target_path[0], file_name), 'wb') as saved_file:
					for content_chunk in file.iter_content(chunk_size=1024):
						if content_chunk:
							saved_file.write(content_chunk)
					dl_message = f"[{green}{timestamps}{reset}] Download file {green}{file_name}{reset} ({file.headers.get('content-type', '-')}) {round(content_length/1024, 2)} MB {green}OK{reset}"
			else:
				dl_message = f"[{red}{timestamps}{reset}] Download file {red}{remote_file_path}{reset} failed. Perhaps no content file ? 🧐"
			
		except Exception as e:
			dl_message = f"[{red}{timestamps}{reset}] Download file {red}{remote_file_path}{reset} failed with error: {red}{e}{reset}"
	
	else:
		dl_message = f"[{yellow}{timestamps}{reset}] File {yellow}{file_name}{reset} already exist on download folder {grey}{local_dl_path}{reset}. {yellow}SKIP{reset}"
	return dl_message


def get_all_url_from(url, file_extensions=[], use_ssl=True):
	all_urls = []
	all_urls_json = []

	# check if url is not 'file'
	check_header = requests.head(url, verify=use_ssl)
	if 'text/html' not in check_header.headers.get('Content-Type'):
		is_file_url = True
		all_urls_json.append({"is_file": is_file_url, "url":url})
		all_urls.append(url)
	else:
		response = requests.get(url, verify=use_ssl)
		host_url = urlparse(response.url)
		dir_list_base_url = host_url.scheme+"://"+host_url.netloc
		if response.status_code == 200 and "index of" in str(response.content.decode('utf-8')).lower():
			html = bs4.BeautifulSoup(response.text, 'html.parser')
			a_tags = html.findAll('a')
			for a in a_tags:
				href = a.get('href') if a.text.lower() not in ["parent directory", "name", "last modified", "size", "description","../"] else ""
				if href:
					if host_url.path not in href:
						href = "/".join([i for i in host_url.path.split("/") if i] + [i for i in href.split("/") if i])
					is_file = True if os.path.splitext(href.lower())[1].replace(".","") else False # any([href.lower().endswith("."+ext) for ext in file_extensions])
					is_absolute = False if href.startswith(dir_list_base_url) else True
					full_href = urlunparse((host_url.scheme, host_url.netloc, href, '', '', '')) if is_absolute else href
					path = urlparse(full_href).path
					if full_href.startswith(dir_list_base_url) and path != "/":
						if full_href not in all_urls:
							all_urls_json.append({'is_file': is_file, 'url': unquote(full_href)})
							all_urls.append(full_href)
	return all_urls_json

def perform_scrape_url(url, file_extensions=[], use_ssl=True):
	global stop, index
	path = urlparse(url)
	if not stop:
		print(f"[{green}INF{reset}] 📂 Remote folder found: {green}{path.path}{reset}, Scanning..")
		urls = get_all_url_from(url, file_extensions=file_extensions)
		if urls:
			print(f"      🌐 Found {len(urls)} folder/file urls from {green}{path.path}{reset}")
			for item in urls:
				try:
					if item['is_file']:
						all_scraped_urls.add(item['url'])
					else:
						if item['url'] not in has_been_processed_urls:
							has_been_processed_urls.append(item['url'])
							perform_scrape_url(item['url'])
				except:
					stop = True
					break

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
			exclude_file_extensions = input(f"[{green}INP{reset}] Input exclude file extension sparated by comma, leave blank to include all extensions. {green}example:{reset} zip,jpg,mp4: ")
			exclude_file_extensions = [ext.lower() for ext in exclude_file_extensions.split(",")]
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
		perform_scrape_url(url, use_ssl=use_ssl)
		urls_without_excluded_ext = [i for i in all_scraped_urls if os.path.splitext(i)[1].replace(".","") not in exclude_file_extensions]
		print(f"[{green}INF{reset}] ℹ️  Scraping URL process done with {green}{len(all_scraped_urls)}{reset} urls")
		if exclude_file_extensions:
			print(f"         {yellow}{len(urls_without_excluded_ext)}{reset} urls without exclude extensions.")
		print(f"[{green}INF{reset}] 📥 Download process starting..")

		max_threads = 10
		download_worker = None
		# for handling ctrl + c when using concurrent
		signal.signal(signal.SIGINT, keyboard_interrupt_handler)
		try:
			download_worker = concurrent.futures.ThreadPoolExecutor(max_workers=max_threads)
			download_process = [download_worker.submit(download_file, url ,use_ssl) for url in urls_without_excluded_ext]
			indent = 8
			n = 1
			for finished_download_process in concurrent.futures.as_completed(download_process):
				spaces = " " * (indent - len(str(n)))
				print(f"{spaces}{grey}{n}{reset} {finished_download_process.result()}")
				n += 1
		except KeyboardInterrupt:
			download_worker.shutdown(wait=True)
		finally:
			download_worker.shutdown(wait=True)
		print(f"[{green}INF{reset}] ✅ Process has been finished at {green}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{reset} !")

def dirlister():
	banner()
	try:
		url = input(f"[{green}INP{reset}] Input your directory listig URL: ")
		while not url:
			url = input(f"[{yellow}WRN{reset}] Please input the target directory URL ex {green}https://youtargetsite.com/uploads{reset}, CTRL + C to exit: ")
		main(url.strip())
	except:
		exit(0)


if __name__=="__main__":
	dirlister()
