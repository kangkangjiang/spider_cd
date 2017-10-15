from bs4 import BeautifulSoup
import requests
import time
import pymongo
import re
from multiprocessing import Pool

'''
创建数据库
'''

client=pymongo.MongoClient('localhost',27017,connect=False)
data_58=client['data_58']
url_list=data_58['url_list']
iteam_info=data_58['iteam_info']

url_host='http://cd.58.com'
# spider  1

def get_links_from(channel, pages,who_sells=0 ):
    '''
    爬出所有的二手信息，分类加入到数据库
    '''
    list_view='{}{}/pn{}/'.format(channel,str(who_sells),str(pages))
    wb_datas=requests.get(list_view)
    soup=BeautifulSoup(wb_datas.text,'lxml')
    # 通过判断网页有无tr标签，判断是否还有数据
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
            # return urls
    else:
        # It's the last page !
        pass


get_links_from('http://cd.58.com/danche/',1)
# spider  2  爬取商品详情页信息

def get_item_info(url):

    # 判断是否来自转转
    no_zhuanzhuan=re.search('http://short.58.com/',url)
    if no_zhuanzhuan:
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
        if no_longer_exist:
            pass
        else:
            title = soup.title.text
            price = soup.select('span.price.c_f50')[0].text
            date = soup.select('.time')[0].text
            area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
            iteam_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
    else:
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # 判断404页面。。
        a=soup.select('div.head p.et')
        if a:
            pass
        else:

                title = soup.title.text
                if soup.find_all('price_now'):
                    price = soup.select('.price_now')[0].text
                else:
                    price='面议'
                if soup.find_all('time'):
                    date = soup.select('.time')[0].text
                else:
                    date='未知'
                # 有一些网页没有‘c_25d’属性
                if soup.find_all('palce_li'):
                    area = list(soup.select('.palce_li ')[0].stripped_strings)

                else:
                    area='未知'
                iteam_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})


