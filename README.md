## Music File Duplicate Remover

This Python script helps you find and remove duplicate music files in your directories.

## Description

The script works by traversing the directories you specify, identifying all music files (currently only .mp3 files are supported), and checking for duplicates. Duplicates are identified by their xxhash3 hash. If duplicates are found, you will be prompted to confirm their deletion.

## Usage

To use this script, simply run it from the command line with the directories you want to check as arguments. For example:

```bash
python3 duplicate_remover.py /path/to/directory1 /path/to/directory2
```

If no directories are specified, the script will check the current directory.

## Functions

- `is_music(file)`: Checks if a file is a music file.
- `get_all_music_files(paths)`: Gets all music files in the given paths.
- `get_files_state(paths)`: Gets the state of the files in the given paths.
- `delete_duplicates(files_state)`: Deletes duplicate files.

