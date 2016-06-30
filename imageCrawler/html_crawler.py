from lxml import etree
import requests
from multiprocessing.dummy import Pool as ThreadPool
import os

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.10 Safari/537.36'
}

# html_breeds = requests.get('https://www.cuteness.com/popular-dog-breeds',headers=header).text
# selector_breeds = etree.HTML(html_breeds)
# dog_breeds_list = selector_breeds.xpath('//div[@class="panel-pane pane-views pane-popular-breeds"]/div/div/div[@class="view-content"]/div/div/div[@class="field-content"]/a[@class="popLink"]/text()')
# # for each in dog_breeds_list:
# #     print each
# dog_breeds_list.remove('Boxer')
# dog_breeds_list.remove('Mixed')
print '##########################'
html_breeds = requests.get('https://www.cuteness.com/popular-cat-breeds',headers=header).text
selector_breeds = etree.HTML(html_breeds)
cat_breeds_list = selector_breeds.xpath('//div[@class="panel-pane pane-views pane-popular-breeds"]/div/div/div[@class="view-content"]/div/div/div[@class="field-content"]/a[@class="popLink"]/text()')
for each in cat_breeds_list:
    print each
cat_breeds_list.remove('Calico')
cat_breeds_list.remove('Mixed')
# cat_breeds_list.remove('Tuxedo')
# cat_breeds_list.remove('Tortoiseshell')
# cat_breeds_list.remove('Persian')
# cat_breeds_list.remove('Bengal')


url_part = 'http://www.webcrawler.com/info.wbcrwl.309.17/search/images?qsi=%s&q=%s&cid=112303476&ad.segment=info.wbcrwl.309.01'
def crawler(key_word):
    n = 0
    temp = n
    dir = key_word
    try:
        os.mkdir(r'pictures/'+key_word+'/')
    except Exception,e:
        print 'Cannot create the folder '+dir
        return
    for i in range(1,542,18):
        url = url_part%(str(i),key_word)
        try:
            html = requests.get(url, headers = header, timeout = 60).text
        except Exception, e:
            print 'Failed to get the html: '+url
            continue
        selector = etree.HTML(html)
        img_urls = selector.xpath('//div[@class="searchResult imageResult"]/div/a/img/@src')
        for img_url in img_urls:
            print 'Downloading picture'+str(n)+':  '+img_url
            try:
                pic = requests.get(img_url, headers=header, timeout=60)
                if str(pic.status_code):
                    if str(pic.status_code)[0] != '2':
                        continue
                else:   continue
            except Exception as e:
                print 'Failed to download pic'+str(n)+': '+str(e)
                continue
            fp = open('pictures\\'+dir+'\\'+str(n)+'.jpg','wb')
            fp.write(pic.content)
            fp.close()
            n+=2
    fp1 = open('info.txt','w')
    fp1.write(str(temp)+'--'+str(n-2)+': '+key_word+'\n')
    return n

pool = ThreadPool(8)
# pool.map(crawler,dog_breeds_list)
pool.map(crawler,cat_breeds_list)
pool.close()
pool.join()

# n = 0
# dir = 'dog'
# for i in range(0, len(dog_breeds_list),2):
#     n = crawler(n,dog_breeds_list[i],dir)
# n = 1
# for i in range(0, len(cat_breeds_list),2):
#     n = crawler(n, cat_breeds_list[i],'cat')
#
# os.system('shutdown -s -f')
# crawler(0,'dog')
# crawler(1,'cat')