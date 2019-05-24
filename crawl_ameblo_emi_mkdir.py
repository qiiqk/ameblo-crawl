import codecs
import os
import time
import re
import string

import requests
from bs4 import BeautifulSoup

URL = 'https://ameblo.jp/kurita--emi/'
Page_Num=13
start_num=47

def get_url():
	links = {}
    
	for i in range(Page_Num):
		# print(line.split(',')[0])
		url=URL + 'page-'+str(i+start_num) + '.html'
		title = 'page-'+str(i+start_num)
		links[url] = title

	return links




def download_page(url):
    return requests.get(url).content



def crawl(url,page_index):
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')

    # create dir with the date of passage
    time = re.split('\s',soup.find('span', attrs={'class': 'date'}).getText())[0]
    time_1=re.split('\s',soup.find('span', attrs={'class': 'date'}).getText())[1]
    time=time+'_'+re.split(':',time_1)[0]+'_'+re.split(':',time_1)[1]+'_'+re.split(':',time_1)[2]
    print('time = ' + time)
    if not os.path.exists(time):
        os.mkdir(time)
	
    #47-59页面用以下语句
    if page_index>=47 and page_index<=59:
        all_a = soup.find_all('div', attrs={'style': 'text-align:left'})
    else:
        all_a = soup.find_all('a')
    index = 0
    for each_a in all_a:
        img = each_a.find('img')
        if img is not None:
            img_link = img['src']
            if img_link[-3:] == '800':
                index += 1
                img_path = './' + time + '/'  + index.__str__() + '.jpg'
                print('img_name = ' + img_path)
                print('img_link = ' + img_link)
                img_r = requests.get(img_link, stream=True)
                if img_r.status_code == 200:
                    with open(img_path, 'wb') as f:
                        for chunk in img_r.iter_content(1024):
                            f.write(chunk)


if __name__ == '__main__':

    s_time = time.time()
    page_index=start_num-1
    all_blog_link = get_url()
    for ame_link in all_blog_link:
        print(ame_link + ', ' + all_blog_link[ame_link])
        page_index+=1
        crawl(ame_link,page_index)

    e_time = time.time()
    cost = e_time - s_time
    print('cost = ' + time.strftime('%M:%S', time.gmtime(cost)))








