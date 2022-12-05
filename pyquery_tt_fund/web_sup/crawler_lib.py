from bs4 import BeautifulSoup
import requests
import urllib.request

def find_all_title(page_info, title, attri):
    # 1st layer filter
    _tmp = page_info.find_all(title[0], attri[0])
    
def down_img(img_url, path):
    with open(path, 'wb') as f:
        f.write(requests.get(img_url).content)
    
if __name__=='__main__':
    url = 'https://cdn5.manhwa18.com/images/2020/10/11/020e2ed18cdc79ed647.jpg'
    path = 'D:/Manhwa18\silent_war\chapter_100_5.jpg'
    down_img(url, path)