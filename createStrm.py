from utils.rclonetools import *
import json
import os


def getDownloadQueue(src, dst, host):
    srcFiles = json.loads(executeCommand(f"rclone lsjson --dirs-only --max-depth 1 {src}")["out"])
    dstFiles = json.loads(executeCommand(f"rclone lsjson --dirs-only --max-depth 1 {dst}")["out"])
    lackDirs = setDifference(srcFiles, dstFiles, lambda a, b: a["Path"] == b["Path"])  # 只比对路径
    copyList = []
    strmList = []
    for dirItem in lackDirs:
        dirBackend = rcloneJoin(src, dirItem["Path"])
        for file in json.loads(executeCommand(f'rclone lsjson --files-only --max-depth 9999 "{ dirBackend }"')["out"]):
            if file["MimeType"].startswith("video"):
                strmUrl = rcloneJoin(rcloneJoin(host, dirItem["Path"]), file["Path"])
                fileDst = rcloneJoin(rcloneJoin(dst, dirItem["Path"]), file["Path"])
                name, _ = os.path.splitext(fileDst)
                fileDst = f"{name}.strm"
                strmList.append((strmUrl, fileDst))
            else:
                fileSrc = rcloneJoin(rcloneJoin(src, dirItem["Path"]), file["Path"])
                fileDst = rcloneJoin(rcloneJoin(dst, dirItem["Path"]), file["Path"])
                copyList.append((fileSrc, fileDst))
    return copyList, strmList


syncList = [
    ("123readonly:电视剧/", "/mnt/storage/Media/EmbyMedia/123pan/电视剧/", "http://emby.nas.local/strm/123pan/电视剧"),
    ("123readonly:电影/", "/mnt/storage/Media/EmbyMedia/123pan/电影/", "http://emby.nas.local/strm/123pan/电影"),
    ("123readonly:番剧/", "/mnt/storage/Media/EmbyMedia/123pan/番剧/", "http://emby.nas.local/strm/123pan/番剧"),
]


result = [getDownloadQueue(src, dst, host) for src, dst, host in syncList]

for copyList, _ in result:
    rcloneCopy(copyList, True, 8)
for _, strmList in result:
    [print(f"{url} > {filePath}\n") for url, filePath in strmList]

if input("输入 y 来继续") == "y":
    for copyList, _ in result:
        rcloneCopy(copyList, False, 8)
    for _, strmList in result:
        for url, filePath in strmList:
            print(f"{url} > {filePath}\n")
            directory = os.path.dirname(filePath)
            os.makedirs(directory, exist_ok=True)
            with open(filePath, "w", encoding="UTF-8") as f:
                f.write(url)

os.system("chmod 777 -R /mnt/storage/Media/EmbyMedia")
