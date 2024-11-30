import os
import sys
import requests
from pydub import AudioSegment
from pydub.playback import play
from colorama import init, Fore
from tempfile import NamedTemporaryFile

# Initialize colorama for colored text output
init(autoreset=True)
vars = {'current_song_path':''}


def list_mp3():
    temp_path = os.environ.get("TEMP")
    if not temp_path:
        print(Fore.RED + "[-] Could not find the TEMP directory.")
        return

    print(Fore.YELLOW + f"[*] Searching for .mp3 files in: {temp_path}\n")
    
    # List all .mp3 files in the %TEMP% directory
    mp3_files = [f for f in os.listdir(temp_path) if f.endswith(".mp3")]
    i=1
    if mp3_files:
        print(Fore.GREEN + f"[+] Found {len(mp3_files)} MP3 files:")
        for file in mp3_files:
            print(f"{Fore.LIGHTBLACK_EX}{i}. {Fore.LIGHTRED_EX}{file}")
            i+=1
        return mp3_files
    else:
        print(Fore.RED + "[-] No MP3 files found.")


def delete_mp3():
    mp3_files = list_mp3()
    temp_path = os.environ.get("TEMP")
    if not mp3_files:
        print(Fore.RED + "[-] No MP3 files to delete.")
        return

    print(Fore.YELLOW + f"[*] Deleting {len(mp3_files)} MP3 files...")
    done = []
    _not = []
    for file in mp3_files:
        try:
            os.remove(os.path.join(temp_path, file))
            done.append(file)
        except Exception as e:
            _not.append(file)
            print(Fore.RED + f"[-] Failed to delete {file}: {e}")
    print(Fore.GREEN + f"[+] Deleted {len(done)} files.")
    if _not!=[]:
        print(Fore.RED + f"[-] Could not delete {len(_not)} file(s) | {', '.join(_not)}")



# Function to get the song URL using a sample API
def get_song_url(song_name):
    api_url = "https://jiosaavn-api-privatecvc2.vercel.app/search/songs"
    try:
        response = requests.get(f"{api_url}?query={song_name}")
        response.raise_for_status()
        data = response.json()
        try:
            url = data["data"]["results"][0]["downloadUrl"][-1]["link"]
            name = data["data"]["results"][0]["name"]
            return url, name
        except (KeyError, IndexError):
            print(Fore.RED + f"[-] Could not find song details for: {song_name}")
            return None, None
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error fetching song URL: {e}")
        return None, None

# Function to download the song from the URL
def download_song(song_url):
    try:
        response = requests.get(song_url, stream=True)
        response.raise_for_status()
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        with open(temp_file.name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return temp_file.name
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error downloading song: {e}")
        return None

# Function to play the song
def play_song(song_path):
    try:
        song = AudioSegment.from_file(song_path)
        play(song)
        print(Fore.GREEN + f"[+] Finished playing: {song_path}")
    except Exception as e:
        print(Fore.RED + f"[-] Error playing song: {e}")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(Fore.RED + f"[-] No song name provided.\n{Fore.YELLOW}[*] \"song -d\" to open download destination.\n{Fore.YELLOW}[*] \"song -del\" to delete mp3 files downloaded in %TEMP%.")
            sys.exit(1)

        song_name = " ".join(sys.argv[1:])  # Get the song name from the command line
        if sys.argv[1].lower() == "-d":
            list_mp3()
            os.startfile(os.environ['TEMP'])
            sys.exit(0)
        elif sys.argv[1].lower() == "-del":
            delete_mp3()
            sys.exit(0)
        print(Fore.MAGENTA + f"[*] Searching for: {song_name}...")
        song_url, resolved_name = get_song_url(song_name)

        if song_url:
            print(Fore.MAGENTA + f"[*] Downloading {resolved_name}...")
            song_path = download_song(song_url)
            if song_path:
                vars['current_song_path'] = song_path
                print(Fore.GREEN + f"[+] Now playing: {resolved_name}")
                play_song(song_path)
            else:
                print(Fore.RED + f"[-] Failed to download {resolved_name}.")
        else:
            print(Fore.RED + f"[-] Could not find song {song_name}.")
    except KeyboardInterrupt:
        if vars.get('current_song_path'):
            print(Fore.LIGHTYELLOW_EX + f"[*] Downloaded in: {vars['current_song_path']}")
        print(Fore.MAGENTA + "\n[!] Exiting")
        sys.exit(0)
