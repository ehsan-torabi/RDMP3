import hashlib
import os
import sys
from pathlib import Path
from time import time
from colorama import Fore,Style
import stat
def is_music(file):
    return file.endswith(".mp3") or file.endswith(".MP3")


def get_all_music_files(paths: list, output_list):
    if len(paths) == 0:
        paths.append(os.curdir)
    for file_path in paths:
        path = Path(file_path).resolve()
        for child in path.iterdir():
            try:
                if child.is_dir():
                    get_all_music_files([child], output_list)
                elif is_music(str(child)):
                    output_list.append(str(child))
            except Exception as err:
                print(err)
                continue
                


def get_files_state(path):
    files_state = {}
    music_files = []
    get_all_music_files(path, music_files)
    for file in music_files:
        with open(file, "rb") as music:
            file_hash = hashlib.sha1(music.read()).hexdigest()
            if file_hash not in files_state:
                files_state[file_hash] = [file]
            else:
                files_state[file_hash].append(file)
    return files_state


def delete_duplicates(files_state):
    duplicate_files = []
    counter = 0
    for file_list in files_state.values():
        if len(file_list) > 1:
            print("\n")
            for file in file_list[1:]:
                duplicate_files.append(file)
                print(Style.BRIGHT+f"Will removed file: {file}".center(100))
    if len(duplicate_files) > 0:
        dialogue =Fore.RED + str(len(duplicate_files)) + Fore.WHITE + " file is duplicate"
        print(dialogue.center(100))
        choose = input(Fore.GREEN +"Are you sure delete this files? (y or n) \n")
        if choose == "y":
            print(Fore.YELLOW +"-------------------------Removed files:-------------------------".center(100)) 
            for file in duplicate_files:
                os.chmod(file, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
                os.remove(file)
                print(Fore.RED+f"{file}".center(100))
            print(Fore.YELLOW +"-------------------------Removed files-------------------------".center(100)+Fore.RESET )
        else:
            print("See you later👋")
            
    else:
        print("File is clean😁".center(100))
    print(Style.RESET_ALL)


if __name__ == "__main__":
    target_dir = sys.argv[1:]
    file_states = get_files_state(target_dir)
    delete_duplicates(file_states)
