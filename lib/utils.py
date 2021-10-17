from os import replace
import requests
import re
from bs4 import BeautifulSoup
from htmlparsing import Element, HTMLParsing, Text, Attr, Parse, HTML, Markdown

def get_manga(ids):
    ids = ids.replace(' ','+')
    url = "https://3asq.org/wp-admin/admin-ajax.php"
    data = f"action=wp-manga-search-manga&title={ids}"
    r = requests.post(url,data,headers={
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://3asq.org',
        'referer': 'https://3asq.org/?s=Hero&post_type=wp-manga',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    })
    return r.json()['data']


def get_chapter(url):
    r = requests.post(url+'ajax/chapters/')
    article_list = HTMLParsing(r.text).list('.wp-manga-chapter    ', {'link': Attr('a', 'href')})
    return article_list
