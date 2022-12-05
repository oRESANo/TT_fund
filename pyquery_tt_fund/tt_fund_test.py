import requests
from pyquery import PyQuery as pq

url = 'http://fund.eastmoney.com/data/fundsearch.html?spm=search&key=%e6%b6%88%e8%b4%b9#key%e6%b6%88%e8%b4%b9'
r = requests.get(url)
#实例化
doc = pq(r.text)
print(doc)