import os

def list_files(directory, extensions=None):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extensions is None or filename.lower().endswith(tuple(extensions)):
                files.append(os.path.join(root, filename))
    return files