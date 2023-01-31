#!/usr/share/python3

import requests
import time
import optparse
from colorama import Fore, Back, Style

# This is a Website Subdomain and Directory Enumeration Tool
# Author : PythonHacker
# Python Version Tested on : 3.10.7
# Usage : Python3 [arguements]
#         Arguements:
#                    -h, --help : To show help 
#                    -u, --url : To specify the Target URL
#                    -w, --wordlist : To specify the wordlist containing subdomain or directories as per requirements
#                    -m, --mode : To specify the mode of enumeration [sub (subdomain), dir (directory)]
#                    -v, --verbose : Verbose mode True/true. false/False if not specified

def get_arguements():

    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", help="To specify the target URL. Provide the URL like target.com", dest="target_url")
    parser.add_option("-w", "--wordlist", help="To specify wordlist containing subdomains or directories as per requirements", dest="wordlist_path")
    parser.add_option("-m", "--mode", help="To specify mode of enumeration (sub, dir)", dest="mode")
    parser.add_option("-v", "--verbose", help="Verbose mode on (to print more information) (true or false)", dest="verbose")

    (options, arguements) = parser.parse_args()

    if not options.target_url:
        parser.error("[-] Please provide the Target URL!")
    if not options.wordlist_path:
        parser.error("[-] Please provide the wordlist path!")
    if not options.mode:
        parser.error("[-] Please provide the mode of enumeration!")

    return options

def sub_enum_get_request(subdomain, url):

    get_request = requests.get("http://" + subdomain + "." + url)
    return str(get_request.status_code)

def dir_enum_get_request(dir, url):

    get_request = requests.get("http://" + url + "/" + dir)
    return str(get_request.status_code)

def sub_enum(subdomain, url, verbose):

    try:
        get_request = sub_enum_get_request(subdomain, url)
        if get_request == "200":
            print("[+] Subdomain exists!        >> " + " " + Back.GREEN + subdomain + "." + url + Style.RESET_ALL + " " + Back.BLUE + get_request + " OK " + Style.RESET_ALL)
    except requests.exceptions.ConnectionError:
        if verbose == "true" or verbose=="True":
            print("[-] Subdomain doesn't exist! >> " + " " + Back.RED + subdomain + "." + url + " " + Style.RESET_ALL)
            pass
        else:
            pass

def dir_enum(dir, url, verbose):

    try:
        get_request = dir_enum_get_request(dir, url)
        if get_request == "200":
            print("[+] Directory found!         >> " + Back.GREEN + "/" + dir + Style.RESET_ALL + " " + Back.Blue + get_request + " OK " + Style.RESET_ALL)
        else:
            if verbose == "true" or verbose=="True":
                print("[-] Directory doesn't exist! >> " + Back.RED + dir + Style.RESET_ALL + " " + Back.BLUE + get_request + " " + http_response(get_request) +  " " + Style.RESET_ALL)
                pass
            else:
                pass

    except requests.exceptions.ConnectionError:
        if verbose == "true" or verbose=="True":
            print("[-] Directory doesn't exist! >> " + Back.RED + dir + Style.RESET_ALL + " " + Back.BLUE + get_request + Style.RESET_ALL)
            pass
        else:
            pass

def http_response(code):

    response = ""
    if code == "200":
        response = "OK"
    elif code == "301":
        response = "Move Permenantly"
    elif code == "400":
        response = "Bad Request"
    elif code == "404":
        response = "Not Found"
    elif code == "500":
        response = "Internal Server Error"
    else:
        pass
    return response

def line_count(path):
    
    with open(str(path), "r") as file:
        count = 0
        for line in file:
            if line != "\n":
                count = count + 1 
    return count

print(Fore.GREEN + "\033[1m" + "\033[4m" + "\nDomain Buster - Website Enumeration Tool\n" + "\033[0m" + Style.RESET_ALL)
print(Fore.WHITE + "  -----> By PythonHacker <-----\n" + Style.RESET_ALL)
print(Fore.RED + "\033[4m" + "[!] Do not use this program for any illegal purposes. Author is not responsible for any misuse.\n" + Style.RESET_ALL)

options = get_arguements()
url = options.target_url
file = options.wordlist_path
user_mode = options.mode
verbose = options.verbose

line_count = line_count(file)
print(Fore.WHITE + "Wordlist length : " + str(line_count) + "\n" + Style.RESET_ALL)

try:
    with open(str(file), "r") as list:
        read_file = list.read()
        for word in read_file.split():
            if user_mode == "sub" or user_mode == "subdomain":
                sub_enum(word, url, verbose)

            if user_mode == "dir" or user_mode == "directory":
                dir_enum(word, url, verbose)

except KeyboardInterrupt:
    print("\033[93m" + "\n[!] CTRL + C detected, quiting ...." + "\033[0m")

print(Fore.WHITE + "\n[+] Website Enumeration completed! " + Style.RESET_ALL)
