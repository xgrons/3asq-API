from typing import Tuple, Any
import math
import time
import json
import re
import sys
import os
import requests
if os.path.exists('.env'):
  load_dotenv('.env')

token = int(os.environ.get("TOKEN"))
regex = r"https?:\/\/uptobox\.com\/(?P<code>[a-zA-Z0-9]+)"
api_url = "https://uptobox.com/api"


def _convert_size(bytes_size: int)-> str:
    if bytes_size == 0:
        return "0B"
    name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(bytes_size, 1024)))
    p = math.pow(1024, i)
    s = round(bytes_size/p, 2)
    return f"{s} {name[i]}"

def _countdown(wait_time: int)-> str:
    while wait_time:
        minutes, seconds = divmod(wait_time, 60)
        timer = f"{minutes}:{seconds}"
        print(timer, end="\r")
        time.sleep(1)
        wait_time -= 1
    return timer

def get_file_info(code: str)-> Tuple[Any, Any]:
    if code.startswith("https://uptobox.com"):
        code = re.findall(regex, code)[0]
        request = requests.get(f"{api_url}/link/info?fileCodes={code}").text
        info = json.loads(request)
        file_name = info["data"]["list"][0]["file_name"]
        file_size = _convert_size(info["data"]["list"][0]["file_size"])
    return file_name, file_size

def get_user_status()-> int:
    request = requests.get(f"{api_url}/user/me?token={token}").text
    info = json.loads(request)
    premium_check = info["data"]["premium"]
    return premium_check

def get_download_link(code: str)-> str:
    if code.startswith("https://uptobox.com"):
        code = re.findall(regex, code)[0]
    if get_user_status() == 1:
        request = requests.get(f"{api_url}/link?token={token}&file_code={code}").text
        info = json.loads(request)
        download_link = info["data"]["dlLink"]
    else:
        request = requests.get(f"{api_url}/link?token={token}&file_code={code}").text
        info = json.loads(request)
        waiting_time = info["data"]["waiting"] + 1
        waiting_token = info["data"]["waiting_token"]
        print(f"[Uptobox] You have to wait {waiting_time} seconds to generate a new link.\n[Uptobox] Do you want to wait ?")
        answer = input("Y for yes, everything else to quit: ")
        if answer.upper() == "Y":
            _countdown(waiting_time)
            request = requests.get(f"{api_url}/link?token={token}&file_code={code}&waiting_token={waiting_token}").text
            info = json.loads(request)
            download_link = info["data"]["dlLink"]
        else:
            sys.exit(1)
    return download_link
#print(get_file_info('https://uptobox.com/plcaufp3hyqu'))
#print(get_download_link('https://uptobox.com/plcaufp3hyqu'))
