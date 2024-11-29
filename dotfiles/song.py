import sys
import os
import requests
from pydub import AudioSegment
from pydub.playback import play
from colorama import init, Fore
from tempfile import NamedTemporaryFile

# Initialize colorama for colored text output
init(autoreset=True)
api_url = os.getenv('SONGAPI')

# Function to get the song URL using a sample API
def get_song_url(song_name):
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
            print(Fore.RED + "[-] No song name provided.")
            sys.exit(1)

        song_name = " ".join(sys.argv[1:])  # Get the song name from the command line

        print(Fore.MAGENTA + f"[*] Searching for: {song_name}...")
        song_url, resolved_name = get_song_url(song_name)

        if song_url:
            print(Fore.MAGENTA + f"[*] Downloading {resolved_name}...")
            song_path = download_song(song_url)
            if song_path:
                print(Fore.GREEN + f"[+] Now playing: {resolved_name}")
                play_song(song_path)
            else:
                print(Fore.RED + f"[-] Failed to download {resolved_name}.")
        else:
            print(Fore.RED + f"[-] Could not find song {song_name}.")
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\n[!] Exiting")
        sys.exit(0)
