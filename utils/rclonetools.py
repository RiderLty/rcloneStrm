import shlex
import sys
from urllib.parse import urljoin
from utils.logger import debug, info, warn, error
import json
import os
import shutil
import subprocess
import threading
import time
from queue import Queue


def executeCommand(command_with_args, dry_run=False):
    """
    执行rclone命令并获取结果

    {
        code:xx,

        out:xx,

        error:xx

    }
    """
    try:
        if dry_run:
            return {
                "code": 0,
                "out": command_with_args,
                "error": "",
            }
        else:
            proc = subprocess.Popen(
                shlex.split(command_with_args),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            stdout, stderr = proc.communicate()
            return {
                "code": proc.returncode,
                "out": stdout.replace("\\n", "\n"),
                "error": stderr,
            }
    except FileNotFoundError as not_found_e:
        return {
            "code": -20,
            "out": "",
            "error": not_found_e,
        }
    except Exception as generic_e:
        return {
            "code": -30,
            "out": "",
            "error": generic_e,
        }


def setDifference(set_a, set_b, compare_func=lambda x, y: x == y):
    """
    计算差

    传入集合A,B,比较函数

    返回存在于集合A中，且不存在集合B中的元素

    例如：

    [1,2,3,4] - [3,4,5,6] => [1,2]

    """
    return [x for x in set_a if not any(compare_func(x, y) for y in set_b)]


def rcloneJoin(a, b):
    """
    rclone的路径合并
    """
    return a + b if a.endswith("/") else a + "/" + b


def rcloneCopy(copyList, dry_run=True, worker_num=2):
    """
    处理复制 用于上传/下载

    copyList 为列表, 其中元素为长度为2的元组(src,dst)

    执行 rclone copyto {src} {dst}
    """
    sem = threading.Semaphore(worker_num)
    for src, dst in copyList:
        print(f"{src} => {dst}\n")
        sem.acquire()

        def worker():
            try:
                res = executeCommand(f'rclone copyto "{src}" "{dst}"', dry_run)
                if res["code"] != 0:
                    print(f'出错:{res["error"]} {src}')
            except Exception as e:
                print(e)
            sem.release()

        threading.Thread(target=worker).start()
    [sem.acquire() for _ in range(worker_num)]
    [sem.release() for _ in range(worker_num)]


def rcloneDelete(deleteList, dry_run=True, worker_num=2):
    """
    处理删除

    deleteList 为列表, 其中元素为需要删除的地址dst

    执行 rclone delete {dst}
    """
    sem = threading.Semaphore(worker_num)
    for dst in deleteList:
        print(f"DELETE:\n{dst}\n")
        sem.acquire()

        def worker():
            try:
                res = executeCommand(f'rclone delete "{dst}"', dry_run)
                if res["code"] != 0:
                    print(f'出错:{res["error"]} {dst}')
            except Exception as e:
                print(e)
            sem.release()

        threading.Thread(target=worker).start()
    [sem.acquire() for _ in range(worker_num)]
    [sem.release() for _ in range(worker_num)]


def backendPathJoin(backend, jsonResult):
    """
    将后端路径与lsjson的结果合并
    返回绝对路径
    """
    return [rcloneJoin(backend, x["Path"]) for x in jsonResult]
