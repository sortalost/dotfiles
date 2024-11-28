import requests
import sys
from colorama import init, Fore
import os

init(autoreset=True)
SITE = "https://dev.saimudra.com"


def login():
    print(Fore.YELLOW + f"[*] Trying to login, with {os.getenv('SITEUSER')} and {os.getenv('SITEPASS')}.")
    con = requests.post(SITE + '/login',json={'username':os.getenv("SITEUSER"),'password':os.getenv("SITEPASS")})
    print(con.content)
    if "Invalid" in str(con.content):
        print(Fore.RED + "[-] Could not login")
        quit()
    print(Fore.GREEN + "[+] Logged in")
    


def newsletter():
    try:
        con = requests.get(SITE + "/misc/newsletter/worker").json()
        print(con)
        if con['status']=='error':
            print(Fore.RED + "[-] Not logged in.")
            login()
        con = requests.get(SITE + "/misc/newsletter/worker").json()
        print(Fore.GREEN + f"[+] Okay: {con}")
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")


if __name__=="__main__":
    if sys.argv[1]=="newsletter":
        newsletter()
    else:
        print(Fore.RED + "[-] No such command.")