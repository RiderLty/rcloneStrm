import os
import json
import requests

os.makedirs("字幕下载",exist_ok=True)
url = f"https://api.github.com/repos/foxofice/sub_share/contents/{input('path:')}"
keyword = input("关键字(可为空):")
response = requests.get(url)
if response.status_code == 200:
    # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    for file in response.json():
        if file["type"] == "file" and keyword in file["name"]:
            resp = requests.get(file["download_url"])
            if resp.ok:
                with open(os.path.join("字幕下载",file["name"]) , 'wb') as f:
                    f.write(resp.content)
                print(f'{file["name"]} 已下载')
            else:
                print(f'{file["name"]} 下载失败')
else:
    print(response.text)   

print("完成")