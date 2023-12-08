import hashlib
import os
import sys
from pathlib import Path
from collections import defaultdict



def is_music(file):
    return file.endswith((".mp3", ".MP3"))


def get_all_music_files(paths):
    if not paths:
        paths = [os.curdir]

    music_files = []
    for path in paths:
        for child in Path(path).resolve().iterdir():
            if child.is_dir():
                get_all_music_files([child])
            elif is_music(child.name):
                music_files.append(child)
    return music_files


def get_files_state(paths):
    files_state = defaultdict(list)
    music_files = get_all_music_files(paths)

    for file in music_files:
        with file.open("rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        files_state[file_hash].append(file)

    return files_state


def delete_duplicates(files_state):
    duplicate_files = []

    for file_list in files_state.values():
        if len(file_list) > 1:
            for file in file_list[1:]:
                duplicate_files.append(file)

    if not duplicate_files:
        print("No duplicate files found!")
        return

    print(f"{len(duplicate_files)} duplicate files found:")
    for file in duplicate_files:
        print(f"\t{file}")

    confirm = input("Delete duplicate files? (y/n): ")
    if confirm.lower() not in ("y", "yes"):
        print("Exiting...")
        return

    for file in duplicate_files:
        os.chmod(file, 0o777)
        os.remove(file)

    print(f"Successfully deleted {len(duplicate_files)} duplicate files!")


if __name__ == "__main__":
    target_dir = sys.argv[1:]
    file_states = get_files_state(target_dir)
    delete_duplicates(file_states)
