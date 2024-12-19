import requests
import sys
from colorama import init, Fore
import os
import json
from datetime import datetime as dt


init(autoreset=True)
SITE = "https://sortalost.vercel.app"


def newsletter():
    try:
        with open("newsletter.json","r") as f:
            data = json.load(f)
        if dt.now().strftime("%d.%m.%y") in data['dates']:
            print(Fore.YELLOW + f"[!] Already sent the newsletter today")
            quit()
        else:
            data['dates'].append(dt.now().strftime("%d.%m.%y"))
    except Exception as e:
        print(Fore.YELLOW + "[!] newsletter.json does not exist, creating...")
        data={"dates":[]}
        f = open("newsletter.json","w")
        f.write(json.dumps(data))
        f.close()
        print(Fore.YELLOW + "[*] created, sending request to server...")
    try:
        con = requests.get(SITE + "/misc/newsletter/worker",json={'username':os.getenv("SITEUSER"),'password':os.getenv("SITEPASS")}).json()
        if con['status']=='error':
            print(Fore.RED + f"[-] {con['error']}")
        else:
            print(Fore.GREEN + f"[+] {con['message']}")
            with open("newsletter.json","r+") as f:
                data = json.load(f)
            data['dates'].append(dt.now().strftime("%d.%m.%y"))
        with open("newsletter.json","w") as f:
            json.dump(data,f)
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")



def cat():
    try:
        f = open(sys.argv[2],"r")
        print(f.read())
        f.close()
    except:
        print(Fore.RED + f"[-] No such file: \"{sys.argv[2]}\"")


if __name__=="__main__":
    if len(sys.argv)<2:
        print(Fore.YELLOW + f"[*] Usage:\n{sys.argv[0]} <command>")
        quit()
    if sys.argv[1]=="newsletter":
        newsletter()
    elif sys.argv[1]=='cat':
        if len(sys.argv)<3:
            print(Fore.YELLOW + f"[*] Usage:\ncat <filename>")
            quit()
        cat()
    else:
        print(Fore.RED + "[-] No such command.")