from utils.rclonetools import *
import json


def get_full_queue(src, dst):
    srcFiles = json.loads(executeCommand(f'rclone lsjson --files-only --max-depth 999 {src} --exclude "*.strm"')["out"])
    dstFiles = json.loads(executeCommand(f'rclone lsjson  --checkers=1 --files-only --max-depth 999 {dst} --exclude "*.strm"')["out"])
    dstFiles = list(filter(lambda x: not x["MimeType"].startswith("video"), dstFiles))  # 过滤视频
    deleteQueue = setDifference(dstFiles, srcFiles, lambda a, b: a["Path"] == b["Path"])  # 只比对路径
    uploadQueue = setDifference(srcFiles, dstFiles, lambda a, b: a["Path"] == b["Path"] and a["Size"] == b["Size"])  # 比对路径与大小
    return backendPathJoin(dst, deleteQueue), list(zip(backendPathJoin(src, uploadQueue), backendPathJoin(dst, uploadQueue)))


syncList = [
    ("/mnt/storage/Media/EmbyMedia/123pan/电视剧", "123readonly:电视剧"),
    ("/mnt/storage/Media/EmbyMedia/123pan/电影", "123readonly:电影"),
    ("/mnt/storage/Media/EmbyMedia/123pan/番剧", "123readonly:番剧"),
]

result = [get_full_queue(src, dst) for src, dst in syncList]
for deleteList, _ in result:
    rcloneDelete(deleteList, True, 8)
for _, copyList in result:
    rcloneCopy(copyList, True, 8)
if input("输入 y 来继续") == "y":
    for deleteList, _ in result:
        rcloneDelete(deleteList, False, 8)
    for _, copyList in result:
        rcloneCopy(copyList, False, 8)
