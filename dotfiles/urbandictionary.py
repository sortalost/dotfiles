import sys
import json
import os
from urllib.parse import quote_plus
import threading
from colorama import init, Fore
import warnings
import requests
import webbrowser
from utils import loading_animation, _vars

warnings.catch_warnings()
warnings.simplefilter("ignore")

init(autoreset=True)

HISTORY_FILE = _vars['ub_history_file']


def search(search_terms,pos=0):
    if pos!=0:
        pos-=1
    def encode(s):
        return quote_plus(s, encoding="utf-8", errors="replace")
    search_terms = search_terms.split(" ")
    search_terms = "+".join([encode(s) for s in search_terms])
    url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
    result = requests.get(url).json()
    if result["list"]:
        try:
            result['list'][pos]
        except KeyError:
            return False
        word = result['list'][pos]['word']
        author = result['list'][pos]['author']
        definition = result['list'][pos]['definition']
        example = result['list'][pos]['example']
        permalink = result['list'][pos]['permalink']
        return word, author, definition, example, len(result['list']), permalink
    else:
        return False



def summary(query,pos=0):
    global loading
    try:
        thread = threading.Thread(target=loading_animation)
        thread.start()
        search_results = search(query,pos=pos)
        if search_results is False:
            _vars['loading'] = False
            thread.join()
            print(Fore.RED + "[-] No results found on Urban dictionary.")
            return
        word = search_results[0]
        author = search_results[1]
        definition = search_results[2]
        example = search_results[3]
        total = search_results[4]
        _vars['loading'] = False
        thread.join()  # Ensure that the loading thread is joined before printing the result
        print(Fore.GREEN + f"[+] {word} ~ {author}  |  {pos} out of {total}th result")
        print(Fore.LIGHTYELLOW_EX + f"DEFINITION:\n{Fore.CYAN}{definition}")
        print("")
        print(Fore.LIGHTYELLOW_EX + f"EXAMPLE:\n{Fore.CYAN}{example}")
        log_query(search_results[5])
    except Exception as e:
        _vars['loading'] = False
        thread.join()
        print(Fore.RED + f"[-] An error occurred: {e}")

def log_query(query):
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []
        history.append(query)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except Exception:
        pass

def history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
            if history:
                print(Fore.GREEN + f"[+] Query History: ({len(history)})")
                for i, q in enumerate(list(set(history)), start=1):
                    def ss(s):
                        f = []
                        for ii in s[7:]:
                                if ii==".":
                                        break
                                f.append(ii)
                        f2 = "".join(f)
                        f3 = f2.replace("-"," ")
                        return f3
                    print(f"{i}. {ss(q)}")
            else:
                print(Fore.RED + "[-] No queries logged yet.")
        else:
            print(Fore.RED + "[-] No query history found.")
    except Exception as e:
        print(Fore.RED + f"[-] Error reading query history: {e}")


def browser():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
            if history:
                webbrowser.open(history[-1:][0])
            else:
                print(Fore.RED + "[-] No queries logged yet.")
    except Exception as e:
        print(Fore.RED + f"[-] Error reading query history: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Fore.BLUE + "[*] Usage:")
        print(f"  {sys.argv[0]} {Fore.LIGHTYELLOW_EX} <your-question> <definition-index>")
        print(f"  {sys.argv[0]} {Fore.LIGHTYELLOW_EX}--history / -h | see search history")
        print(f"  {sys.argv[0]} {Fore.LIGHTYELLOW_EX}--browser / -b | open the last search query in urbandictionary.com")
    elif sys.argv[1] in ["--history", "-h"]:
        history()
    elif sys.argv[1] in ["--browser", "-b"]:
        browser()
    else:
        pos=0
        try:
            if (isinstance(eval(sys.argv[-1]),int)) and (int(sys.argv[-1])<=10):
                pos = sys.argv[-1]
            if int(sys.argv[-1])>10:
                print(Fore.YELLOW + "[!] <definition-index> cannot be more than 10")
        except:
            pass
        if len(sys.argv[1:])>1:
            query = " ".join(sys.argv[1:][:-1])
        else:
            query = " ".join(sys.argv[1:])
        summary(query,pos=int(pos))
