import os

PATH = r"/mnt/storage/Media/EmbyMedia"
TARGET = "emby.router.local"
REPLACEMENT = "emby.nas.local"
DRY_RUN = True

def list_files(path):
    file_paths = []
    items = os.listdir(path)
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            file_paths.append(item_path)
        elif os.path.isdir(item_path):
            file_paths.extend(list_files(item_path))
    return file_paths


def handel(path, content):
    return content.replace(TARGET, REPLACEMENT)


file_paths = list_files(PATH)
for file in file_paths:
    if os.path.splitext(file)[1].lower() == ".strm":
        print(file)
        content = open(file, "r", encoding="UTF-8").read()
        new = handel(file, content)
        print(file, "\n", content, "\n", new, "\n")
        if DRY_RUN:
            with open(file, "w", encoding="UTF-8") as f:
                f.write(new)
