from os import replace
import requests
import re
from bs4 import BeautifulSoup
from htmlparsing import Element, HTMLParsing, Text, Attr, Parse, HTML, Markdown
from lib.uptobox import *


def get_anime(ids):
    ids = ids.replace(' ','+')
    url = f'https://ww.anime4up.com/?search_param=animes&s={ids}'
    r = requests.get(url)
    article_list = HTMLParsing(r.text).list('.hover.ehover6', {'url': Attr('a.overlay', 'href'),
                                                               'title': Attr('img.img-responsive', 'alt'),
                                                               'image_url': Attr('img.img-responsive', 'src')})
    return article_list


def get_episode(ids):
    #ids = ids.replace(' ','+')
    url = f'https://ww.anime4up.com/anime/{ids}'
    r = requests.get(url)
    article_list = HTMLParsing(r.text).list('.hover.ehover6', {'title': Attr('img.img-responsive', 'alt'), # css selector
                                                    'link': Attr('a.overlay', 'href')})
    return article_list


def get_link(url):
    r = requests.get(url)
    e = Element(text=r.text)
    lnko = e.links
    prog = re.compile('https://uptobox.com/([a-zA-Z0-9.-]*)')
    data = prog.findall(str(lnko))
    all_link = []
    Quality = ['FHD','HD','SD']
    for i in data:
        dl = f'https://uptobox.com/{i}'
        all_link.append(dl)
    dictionary = dict(zip(Quality, all_link))
    return dictionary

