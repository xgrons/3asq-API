from fastapi import FastAPI
from typing import Optional
import requests
import logging
from lib.utils import *
#############################
app = FastAPI()

logging.basicConfig(level=logging.INFO)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/search")
def read_item(id: str):
    resutls = get_manga(id)
    return {"results":resutls}

@app.get("/api/fetch")
def read_item(link: str):
    resutls = get_chapter(link)
    return {"results":resutls}

@app.get("/api/dl")
def read_item(link: str):
    resutls = get_image(link)
    return {"results":resutls}
