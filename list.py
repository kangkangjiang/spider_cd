from bs4 import BeautifulSoup
import requests

# 拿到58同城二手市场的列表页
start_url='http://cd.58.com/sale.shtml'
url_host='http://cd.58.com'

def get_index_url(url):
    try:
            wb_data = requests.get(url)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            links = soup.select('#ymenu-side > ul > li > span.dlb > a')
            for link in links:
                page_url = url_host + link.get('href','')
    except requests.exceptions.ConnectionError as e :
        pass

get_index_url(start_url)

channel_list='''
   

    http://cd.58.com/danche/
    http://cd.58.com/diandongche/


'''