import sys
import wikipedia
import json
import os
import threading
from colorama import init, Fore
import warnings
import requests
import webbrowser
from utils import loading_animation, _vars

warnings.catch_warnings()
warnings.simplefilter("ignore")

init(autoreset=True)

HISTORY_FILE = _vars['wiki_history_file']

def summary(query):
    global loading
    try:
        thread = threading.Thread(target=loading_animation)
        thread.start()
        search_results = wikipedia.search(query, results=1)
        if not search_results:
            _vars['loading'] = False
            thread.join()
            print(Fore.RED + "[-] No results found on Wikipedia.")
            return
        page_title = search_results[0]
        result_summary = wikipedia.summary(page_title, sentences=3)
        _vars['loading'] = False
        thread.join()  # Ensure that the loading thread is joined before printing the result
        print(Fore.GREEN + f"[+] {page_title} ")
        print(Fore.CYAN + result_summary)
        log_query(query)
    except wikipedia.exceptions.DisambiguationError as e:
        _vars['loading'] = False
        thread.join()
        print(Fore.YELLOW + "[?] The query is ambiguous.")
        print(Fore.YELLOW + "[*] Suggestions:")
        for i, option in enumerate(e.options[:5], start=1):
            print(f"  {i}. {option}")
    except wikipedia.exceptions.PageError:
        _vars['loading'] = False
        thread.join()
        print(Fore.RED + "[-] No matching page found.")
    except requests.exceptions.RequestException:
        _vars['loading'] = False
        thread.join()
        print(Fore.RED + "[-] No internet connection.")
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
