#coding:utf-8

import urllib2,re,time,random,os,datetime
import HTMLParser
from bs4 import BeautifulSoup
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

# 自定义打印函数
def self_log(msg):
    print u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)
    
# 获取页面内容
def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url=url,headers=headers)
    try:
        html = urllib2.urlopen(req).read()
	html=HTMLParser.HTMLParser().unescape(html)
        return html  		
    except urllib2.HTTPError,e:  
        print e.code

# 得到博客页面的总数
def get_last_page(html,fd):  
    if not html:  
        self_log(u'页面错误，停止运行')   
        return  
    page = BeautifulSoup(html,'lxml')  
    try:
        last_page=page.find('div',class_ ='pagelist').find_all('a')  
        last_page= last_page[len(last_page)-1].get('href')[-1:]  
        self_log('总共有%s 页博客' % last_page)  
        fd.write('总共有%s 页博客\n' % last_page)
        return last_page  
    except Exception,e:  
        return 1  
 
      
# 获取页面列表
def get_items(url):  
    content_html=get_html(url)  
    page = BeautifulSoup(content_html,'lxml')  
    items = page.find_all('div',class_ ='list_item list_view')  
    return items  
  
# 根据每一个 items list 提取需要的元素
def handle_items(items,content_list,read_num_for_sort):  
    for item in items:  
        temp={} # 临时变量
          
        title=item.find('a')#标题  
        content_url='http://blog.csdn.net'+title.get('href')#标题对应文章的地址  
        read_times=item.find('span',class_ ='link_view').text.strip()#阅读次数  
        comments_time=item.find('span',class_ ='link_comments')#评论次数  
          
        read_number = int(filter(str.isdigit, str(read_times))) #提取出来具体阅读次数的数字，为之后的排序做准备  
        read_num_for_sort.append(read_number)  
  
        # 数据打包
        temp['indexs']=read_number  
        temp['title']=title.text.strip()  
        temp['read_times']=read_times  
        temp['comments_time']=comments_time.text.strip()  
        temp['content_url']=content_url  
        content_list.append(temp)  
  
#创建文件夹  
def mkdir_folder(path):  
    if not os.path.exists(path):    
        os.makedirs(path)   
  
#获取页面信息  
def getContent(html,dir_path):  
    page = BeautifulSoup(html,'lxml')  
    try:  
        title=page.find('div',class_='article_title').find('a').text  
        title=title.strip()  
    except Exception,e:  
        print e  
    try:  
        content=page.find('div',class_='article_content')  
        dir_path=dir_path  
        artitle_name_path=dir_path+'/'+title+'.txt'  
        with open(artitle_name_path+'.txt','w') as f:  
            f.write(content.text)  
        self_log(u'存贮文章：%s 完毕' % title)  
    except Exception,e:  
        print e  
  
#存贮每一篇文章到本地  
def run_to_get_article(content_total_list,dir_path):  
    self_log('start save every article  ')  
    for article_content in content_total_list:  
        article_url=article_content.split('|')[4]  
        self_log( '将要存贮的地址是： %s ...' % article_url)  
        artitle_html=get_html(article_url)  
        getContent(artitle_html,dir_path)  
    
#根据传进来的地址，获取博主名字，同时以博主名字命名存贮目录	
def get_blocker_name(url):
    if 'viewmode' in url:
        print url.split('.net')[1]
        print url.split('.net')[1].split('?')[0].split('/')[1]
        return url.split('.net')[1].split('?')[0].split('/')[1]
    else:
        print url.split('.net')[1]
        print url.split('.net')[1].split('/')[1]          
        return url.split('.net')[1].split('/')[1]          

# 程序运行主函数
def run(url,dir_path):  
    read_num_for_sort=[]  
    content_list=[]  
    content_total_list=[]  
      
    #定义文件夹名字并创建文件夹  
    dir_path=dir_path
    mkdir_folder(dir_path)  
      
    #定义文件名字  
    count_file_name=dir_path+'/'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.txt'  
    fd=open(count_file_name,'w')  
      
    #1.从主页进入获取页面总数  
    main_html=get_html(url)  
    last_page=get_last_page(main_html,fd)  
      
 
    if  last_page>1:
    #3.组装url，分别加载每页的页面,同时在每一个页面提取我们需要的内容  
        for i in range(1,int(last_page)+1):  
            if  'category' not in url:
                main_url=url.split('?')[0]+'/article/list/%d?viewmode=contents' % i 
            else:
                main_url=url+'/%s' % i
            self_log('即将获取第%d页的内容，地址是：%s' % (i,main_url))  
                  
            items=get_items(main_url)#获取每一页的页面内容，根据页面内容得到文章item list  
            handle_items(items,content_list,read_num_for_sort)#处理item list  
    else:
        items=get_items(url)#获取每一页的页面内容，根据页面内容得到文章item list  
        handle_items(items,content_list,read_num_for_sort)#处理item list  
    self_log('总共有%d 篇文章' % len(content_list))#根据得到的数据，统计文章总数  
    #根据 indexs（阅读次数）这个索引值进行排序  
    #非常好的一个根据列表中字典数据进行排序的方法  
    content_list = sorted(content_list,cmp=lambda x,y:cmp(x['indexs'],y['indexs']),reverse=0)  
      
    article_index = 1  
    for a in content_list:  
        #组装打印语句  
        totalcontent= '第'+str(article_index)+'篇|'+a['title']+'|'+a['read_times']+'|'+a['comments_time']+'|'+a['content_url']  
        #self_log(totalcontent)  
        print totalcontent  
        #将其存贮到本地  
        fd.write(totalcontent)  
        fd.write('\n')  
        article_index +=1  
        content_total_list.append(totalcontent)  
    fd.close()        
  
    return content_total_list  
      
if __name__ == '__main__':   
    print '''
            *****************************************  
            ** Welcome to the Spider of CSDN Blog  **  
            ** Created on 2019-06-22               **  
            ** @author: Alan_Wang                  **  
            *****************************************
		    '''
 
    url = 'http://blog.csdn.net/qiqiyingse?viewmode=contents'  
    
    # url = 'http://blog.csdn.net/qiqiyingse/article/category/6292432?viewmode=contents' 
    # 使用某分类目录的 url
    
    dir_path = get_blocker_name(url)
    content_total_list = run(url,dir_path)  
    run_to_get_article(content_total_list,dir_path)  