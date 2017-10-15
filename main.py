from multiprocessing import Pool
from list import channel_list
from page_info import get_links_from,get_item_info,url_list,iteam_info,client
import time


# 拿到前100页`的数据

def get_all_links_from(channel):
    for i in range(1,100):
        get_links_from(channel,i)

# 拿到详情页信息
def get_all_info(url_list,n):
       for i in url_list.find().limit(n):
                get_item_info(i['url'])



if __name__ == '__main__':
    poo1=Pool()
    poo1.map(get_all_links_from, channel_list.split())
    poo1.close()
    poo1.join()
    while True:
        get_all_info(url_list,1000)




