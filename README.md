<a href="https://github.com/karjok/dirlister/blob/main/src/dirlister_banner.png"><img src="https://github.com/karjok/dirlister/blob/main/src/dirlister_banner.png" alt="dirlister-banner" border="0" style="width:100%;"></a>

# DIRLISTer - Directory Listing Downloader

DIRLISTer is a straightforward tool for downloading or backing up all files from a directory listing host.

> Directory listing is a web page that displays the files and directories available on a web server.

With DIRLISTer, you can automate the process of downloading all files from a directory listing page, saving you the hassle of manual downloading.

## Installation
### Requirements
- Python 3
- `requests` library
- `bs4` library
  
### Setup
1. Clone this repository:
   ```bash
    git clone https://github.com/karjok/dirlister.git
   ```
2. Navigate to the project directory:
   ```bash
   cd dirlister
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
### Running the Script
To run the script, use:
```bash
python dirlister.py
```
### Running as s System Tool (Linux)
1. Make the script executable:
   ```bash
   mv dirlister.py dirlister
   chmod +x dirlister
   ```
2. Move the executable to a directory in your system path:
   ```bash
   mv dirlister /home/bin/
   ```
   
The downloaded files will be saved in the dirlister_result_path folder located in the same directory from where you run the script.


## Demo
Check out the demo video: 
[![asciicast](https://asciinema.org/a/8lelfsNAXjjv4WkebGild88ZT.svg)](https://asciinema.org/a/8lelfsNAXjjv4WkebGild88ZT)

## Features
- **User-friendly:** Simple to use.
- **Efficiency:** Skips files that have already been downloaded.
- **Open Source:** Contribute and improve the project!

## Limitations
- **Link Scraping:** Occasionally, the script may struggle with scraping links.
- **File Extensions:** Only common file extensions are listed.
- **No Filtering:** All listed extensions will be downloaded, as filtering capabilities are not yet implemented.
- **Single-threaded:** Downloads occur one at a time.
- **Tested Environment:** Currently tested only on Kali Linux. If you encounter issues, please report them in the Issues section.

## Contributing
Feel free to contribute to the project by submitting pull requests or reporting issues. Your input is greatly appreciated!
