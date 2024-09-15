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
### Running as System Tool (Linux)
1. Make the script executable:
   ```bash
   mv dirlister.py dirlister
   chmod +x dirlister
   ```
2. Move the executable to a directory in your system path:
   ```bash
   mv dirlister /home/bin/
   ```
You can also create a symlink to the `dirlister.py` script in `/usr/bin/` to make DIRLISTer accessible from anywhere on your system. This allows you to run the tool without needing to navigate to its directory each time.

#### Steps:
1. **Make the script executable** by running:
    ```bash
    chmod +x dirlister.py
    ```

2. **Create a symlink** in `/usr/bin/` to allow system-wide access:
    ```bash
    sudo ln -s /path/to/dirlister/dirlister.py /usr/bin/dirlister
    ```

    Replace `/path/to/dirlister/dirlister.py` with the actual path to the `dirlister.py` file.

3. Now you can run DIRLISTer from anywhere on your system by simply typing:
    ```bash
    dirlister
    ```

This method gives you convenient access to DIRLISTer from any directory in your terminal.
   
**The downloaded files will be saved in the `dirlister_result_path` folder located in the same directory from where you run the script.**

## Features
- **User-friendly:** Simple to use.
- **Excluding:** Exclude extensions capaility
- **Concurrent:** Use concurrent when downloading the files
- **Efficiency:** Skips files that have already been downloaded.
- **Open Source:** Contribute and improve the project!

## Demo
Check out the demo video: 
[![asciicast](https://asciinema.org/a/9vRVUe25HRO4ajN8AtanqtOQH.svg)](https://asciinema.org/a/9vRVUe25HRO4ajN8AtanqtOQH)


## Tested Environment

DIRLISTer has been tested and confirmed to work on the following environments:
- **PC**: Ubuntu-based systems and Kali Linux.
- **Android**: Termux environment.

If you encounter issues while using this tool on other operating systems, devices, or environments, please provide details in the [Issues](https://github.com/karjok/dirlister/issues) section of this repository. Your feedback is valuable and will help improve compatibility with other platforms.


## Contributing
Feel free to contribute to the project by submitting pull requests or reporting issues. Your input is greatly appreciated!