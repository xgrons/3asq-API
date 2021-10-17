from os import replace
import requests
import re
from bs4 import BeautifulSoup
from htmlparsing import Element, HTMLParsing, Text, Attr, Parse, HTML, Markdown
from requests.sessions import session
##############################################################################################
def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
##############################################################################################
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
    data = [url['url'] for url in r.json()['data']]
    data_title = [url['title'] for url in r.json()['data']]
    data_link = ['https://3asq.deta.dev/api/fetch?link='+link for link in data ]
    data_anime = [{'title': a,'url': b,} for a ,b in zip(data_title,data_link)]
    return data_anime

def get_chapter(url):
    manga_name = url.split('/')[4]
    new_link = 'https://3asq.org/manga/'+manga_name+'/ajax/chapters/'
    r = requests.post(new_link,headers={
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://3asq.org',
        'referer': 'https://3asq.org/manga/'+manga_name+'/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    })
    tree = BeautifulSoup(r.text, 'html.parser')
    data_link = [child for child in tree.findAll("li", {"class":"wp-manga-chapter"})]
    data_date = [child for child in tree.findAll("span", {"class":"chapter-release-date"})]
    links_data = [link.find('a')['href'] for link in data_link]
    date_release = [link.find('i').text for link in data_date]
    links = ['https://3asq.deta.dev/api/dl?link='+link for link in links_data]
    all_link = dict(enumerate(links, start=1))
    return all_link

def get_image(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_data = [child['src'] for child in soup.findAll("img", {"class":"wp-manga-chapter-img"})]
    image_links = [link.strip() for link in image_data]
    return image_links
