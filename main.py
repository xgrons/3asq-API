from fastapi import FastAPI
from typing import Optional
import requests
import logging
from lib.utils import *
from lib.uptobox import *
#############################
app = FastAPI()

logging.basicConfig(level=logging.INFO)
@app.get("/")
def read_root():
    r = requests.get('http://ip-api.com/json')
    data = r.json()
    return data

@app.get("/api/search")
def read_item(id: str):
    resutls = get_anime(id)
    return {"results":resutls}

@app.get("/api/fetch")
def read_item(id: str):
    resutls = get_episode(id)
    return {"results":resutls}

@app.get("/api/dl")
def read_item(link: str):
    resutls = get_link(link)
    return resutls
