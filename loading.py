
import os
from pathlib import Path
from llama import Llama

def load_files_to_llama_index(directory, ignore_file):
    # Initialize Llama index
    index = Llama()

    # Read .granignore file
    ignore_path = Path(directory) / ignore_file
    if ignore_path.exists():
        with open(ignore_path, 'r') as f:
            ignore_files = f.read().splitlines()
    else:
        ignore_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Ignore files listed in .granignore
            if file not in ignore_files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                # Add file content to Llama index
                index.add_document(content)

    return index

# Usage
directory = 'your_directory'
ignore_file = '.granignore'
index = load_files_to_llama_index(directory, ignore_file)