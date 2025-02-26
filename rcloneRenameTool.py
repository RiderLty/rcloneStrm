"""
输入rclone路径
对depth=1的文件
列出，并生成一个txt文件
修改该txt文件
按照index对应，进行重命名

"""

from utils.rclonetools import *
import os

renameFiles = os.path.join(os.path.dirname(__file__), "renameFiles.txt")

path = input("输入rclone可识别的完整文件夹路径\n$")
files = json.loads(executeCommand(f'rclone lsjson --files-only --max-depth 1 "{ path }"')["out"])
names = [x["Name"] for x in files]
with open(renameFiles, "w", encoding="UTF-8") as f:
    f.write("\n".join(names))
os.system(f"code {renameFiles}")
input(f"已保存到{renameFiles}\n编辑完成后任意键继续...")
with open(renameFiles, "r", encoding="UTF-8") as f:
    newNames = f.read().splitlines()

assert len(newNames) == len(names), f"文件数量不匹配 : {len(newNames)}!={len(names)}"

moves = []

for i in range(len(names)):
    if names[i] != newNames[i]:
        print(f"SRC:{names[i]}\nDST:{newNames[i]}\n")
        src = rcloneJoin(path , names[i])
        dst = rcloneJoin(path , newNames[i])
        moves.append((src,dst))   
        
        
if input("输入y来继续") == "y":
    for (src,dst) in moves:
        cmd = f'rclone moveto "{src}" "{dst}"'
        print(cmd)
        os.system(f'rclone moveto "{src}" "{dst}"')