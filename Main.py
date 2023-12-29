import hashlib
import os
import sys
from pathlib import Path
from collections import defaultdict

def is_music(file):
    """Check if a file is a music file."""
    return file.suffix.lower() == ".mp3"

def get_all_music_files(paths):
    """Get all music files in the given paths."""
    music_files = []
    if not paths:
        paths = [os.curdir]

    for path in paths:
        try:
            for child in Path(path).resolve().iterdir():
                if child.is_dir():
                    music_files.extend(get_all_music_files([child]))
                elif is_music(child):
                    music_files.append(child)
        except:
            continue
    return music_files

def get_files_state(paths):
    """Get the state of the files in the given paths."""
    files_state = defaultdict(list)
    music_files = get_all_music_files(paths)

    for file in music_files:
        with file.open("rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        files_state[file_hash].append(file)

    return files_state

def delete_duplicates(files_state):
    """Delete duplicate files."""
    duplicate_files = [file for file_list in files_state.values() if len(file_list) > 1 for file in file_list[1:]]

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
    print("Please wait ...")
    target_dir = sys.argv[1:]
    file_states = get_files_state(target_dir)
    delete_duplicates(file_states)
