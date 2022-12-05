import sys
sys.path.append('E:\python_progams\web_crawler')
from collections import OrderedDict

from bs4 import BeautifulSoup
import urllib.request
from web_sup.manhwa18 import *
from web_sup.crawler_lib import *
import os
import requests


class Crawler():
    def __init__(self):
        self.url = None
        self.headers = None 
        self.page_name = None # current web site name e.g.manhwa_18 or silent war
        self.click_link = OrderedDict() # next level link
        self.image_list = OrderedDict() # usful images on page
        self.video_list = OrderedDict() # usful videos on page
        self.content_list = OrderedDict() # usful string on page
        self.request_method = 'get' # trigger get method for request
        self.download_path = None # storage path in local
        self.trigger_download = True
        self.web_content = None # request content from web
        self.parsed_content = None # parsed content from bs4
        
    def init_crawler_obj(self,**kwargs):
        for key, value in kwargs.items():
            if key in vars(self).keys():
                vars(self)[key] = value
        self.create_connect()
    
    def create_connect(self, url=None):
        if url:
            self.url = url
        if self.request_method == 'get':
            self.web_content = requests.get(url=self.url, headers=self.headers)
            self.web_content.encoding = self.web_content.apparent_encoding
            self.parsed_content = BeautifulSoup(self.web_content.text, 'html.parser')
        else:
            print('NOT READY FOR OTHER METHOD')

if __name__ == '__main__':
    pass
    