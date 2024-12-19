import sys
from colorama import Fore
import time

_vars = {
    'loading':True,
    'wiki_history_file':'dotfiles/wikihistory.json',
    'ub_history_file':'dotfiles/ubhistory.json',
    }

def loading_animation():
    while _vars['loading']:
        for char in "\\|/~":
            sys.stdout.write(f"\r{Fore.YELLOW}[{char}]")
            sys.stdout.flush()
            time.sleep(0.2)
    sys.stdout.write("\r")  # Clear the loading animation line
