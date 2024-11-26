import requests
from lxml import html
import random
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

default = r"""
                 ᶻ ᶻ    
                z                                            
                 Zᶻ   AS IN ₂₂₂₂₂₂zzzzzzZZZZZZZZZZZᶻᶻᶻᶻᶻᶻᶻᶻ
       .--.  Z Z      A SOCIAL MENACE!                                       
      / _(c\   .-.     __                                    
     | / /  '-;   \'-'`  `\______                             
     \_\/'/ __/ )  /  )   |      \--,                        
     | \`""`__-/ .'--/   /--------\  \                       
      \\`  ///-\/   /   /---;-.    '-'                       
                   (________\  \                             
                             '-'                             
"""

with open(r"dotfiles/ids.txt", "r") as f:
    ids = str(f.read()).split("\n")
    _id = random.choice(ids)

url = f'http://www.asciiartfarts.com/{_id}.html'
try:
    response = requests.get(url)
except:
    print(Fore.RED + default)  # Print default in red color
    quit()

tree = html.fromstring(response.content)
data = tree.xpath('//pre/text()')[1]

colors = ['BLUE', 'CYAN', 'GREEN', 'LIGHTBLUE_EX', 'LIGHTGREEN_EX', 'LIGHTMAGENTA_EX', 'LIGHTRED_EX', 'LIGHTYELLOW_EX', 'MAGENTA', 'RED', 'YELLOW']

color = eval(f'Fore.{random.choice(colors)}')

# Example of using different colors for text:
print(color + data)  # Print the data in green
