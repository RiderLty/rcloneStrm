import shlex
import sys
from urllib.parse import urljoin
from utils.rclonetools import executeCommand, backendPathJoin, rcloneJoin, rcloneCopy, setDifference
from utils.webdavInterface import webdav
from utils.logger import debug, info, warn, error
import json
import os
import shutil
import subprocess
import threading
import time
from queue import Queue

syncList = [
    ("/mnt/storage/Media/EmbyMedia/123pan/电视剧", "123raw:电视剧"),
    ("/mnt/storage/Media/EmbyMedia/123pan/电影", "123raw:电影"),
    ("/mnt/storage/Media/EmbyMedia/123pan/番剧", "123raw:番剧"),
]

for src, dst in syncList:
    cmd = f'rclone lsjson --files-only --max-depth 999 {src} --exclude "*.strm"  --exclude "*.ass"  --max-age 25h'#--exclude "*.ass" 
    files = json.loads(executeCommand(cmd)["out"])
    copyList = list(zip(backendPathJoin(src, files), backendPathJoin(dst, files)))
    rcloneCopy(copyList, False, 8)
