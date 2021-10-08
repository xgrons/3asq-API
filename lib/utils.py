from os import replace
import requests
import re
from bs4 import BeautifulSoup
from htmlparsing import Element, HTMLParsing, Text, Attr, Parse, HTML, Markdown

def get_anime(ids):
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


#def get_episode(ids):
#    #ids = ids.replace(' ','+')
#    url = f'https://ww.anime4up.com/anime/{ids}'
#    r = requests.get(url)
#    article_list = HTMLParsing(r.text).list('.hover.ehover6', {'title': Attr('img.img-responsive', 'alt'), # css selector
#                                                    'link': Attr('a.overlay', 'href')})
#    return article_list
#
#
#def get_link(url):
#    r = requests.get(url)
#    e = Element(text=r.text)
#    lnko = e.links
#    prog = re.compile('https://uptobox.com/([a-zA-Z0-9.-]*)')
#    data = prog.findall(str(lnko))
#    all_link = []
#    Quality = ['FHD','HD','SD']
#    for i in data:
#        dl = f'https://uptobox.com/{i}'
#        all_link.append(dl)
#    dictionary = dict(zip(Quality, all_link))
#    return dictionary

#print(get_anime('boku no'))