# search wikipedia
# wiki <search-term>

import sys
import wikipedia
import json
import os
import threading
import time
from colorama import init, Fore
import warnings
import requests
import webbrowser

warnings.catch_warnings()
warnings.simplefilter("ignore")

init(autoreset=True)

HISTORY_FILE = "dotfiles/wikihistory.json"
loading = True

def loading_animation():
    while loading:
        for char in "\\|/~":
            sys.stdout.write(f"\r{Fore.YELLOW}[{char}]")
            sys.stdout.flush()
            time.sleep(0.2)
    sys.stdout.write("\r")  # Clear the loading animation line


def summary(query):
    global loading
    try:
        thread = threading.Thread(target=loading_animation)
        thread.start()
        search_results = wikipedia.search(query, results=1)
        if not search_results:
            loading = False
            thread.join()
            print(Fore.RED + "[-] No results found on Wikipedia.")
            return
        page_title = search_results[0]
        result_summary = wikipedia.summary(page_title, sentences=3)
        loading = False
        thread.join()  # Ensure that the loading thread is joined before printing the result
        print(Fore.GREEN + f"[+] {page_title} ")
        print(Fore.CYAN + result_summary)
        log_query(query)
    except wikipedia.exceptions.DisambiguationError as e:
        loading = False
        thread.join()
        print(Fore.YELLOW + "[?] The query is ambiguous.")
        print(Fore.YELLOW + "[*] Suggestions:")
        for i, option in enumerate(e.options[:5], start=1):
            print(f"  {i}. {option}")
    except wikipedia.exceptions.PageError:
        loading = False
        thread.join()
        print(Fore.RED + "[-] No matching page found.")
    except requests.exceptions.RequestException:
        loading = False
        thread.join()
        print(Fore.RED + "[-] No internet connection.")
    except Exception as e:
        loading = False
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
                for i, q in enumerate(history, start=1):
                    print(f"{i}. {q}")
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
                webbrowser.open(f"https://en.wikipedia.org/wiki/{history[-1:][0]}")
            else:
                print(Fore.RED + "[-] No queries logged yet.")
    except Exception as e:
        print(Fore.RED + f"[-] Error reading query history: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Fore.BLUE + "[*] Usage:")
        print(f"  {sys.argv[0]} {Fore.LIGHTYELLOW_EX} <your-question>")
        print(f"  {sys.argv[0]} {Fore.LIGHTYELLOW_EX}--history / -h | see search history")
        print(f"  {sys.argv[0]} {Fore.LIGHTYELLOW_EX}--browser / -b | open the last search query in wikipedia")
    elif sys.argv[1] in ["--history", "-h"]:
        history()
    elif sys.argv[1] in ["--browser", "-b"]:
        browser()
    else:
        query = " ".join(sys.argv[1:])
        summary(query)
