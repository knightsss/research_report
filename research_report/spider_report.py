#coding=utf-8
__author__ = 'shifx'
import math
import time
import urllib2
import re
import os
from bs4 import BeautifulSoup

from research_report.base_data_message import get_base_report_type_url

# open the url and read
def get_html(url):
    # page = urllib2.request.urlopen(url)
    get_html_flag = True
    count = 0
    while get_html_flag:
        try:
            req = urllib2.Request(url = url)
            page = urllib2.urlopen(req)
            html = page.read()
            page.close()
            get_html_flag = False
        except:
            time.sleep(3)
            print "spider html again..."
            if count > 2:
                get_html_flag = False
                print "spider html error..."
                html = ''
        count = count + 1
    return html

#获取总页面数，需要异常处理，完成
def get_page_count(base_report_type_url):
    try:
        #base_report_type_url = base_report_type_url.replace('.html','_p' + str(1) + '.html')
        html = get_html(base_report_type_url)
        #网络异常
        if html == '':
            page_count = 0
        else:
            print "get html ok"
            time.sleep(1)
            soup = BeautifulSoup(html,"html.parser")
            page_count = int(soup.find(class_='page').find('span').string)
    except:
        page_count = 0
    return page_count

#基于每一页的url,获取当页的所有report的地址
def get_article_url_list(base_url):
    base_html = get_html(base_url)
    base_url_list = []
    if base_html == '':
        pass
    else:
        soup = BeautifulSoup(base_html,"html5lib")
        elements = soup.find(class_='yb_con').find_all('li')
        for elem in elements:
            elem_dict = {}
            a_element = elem.find('a')
            if a_element != None:
                elem_dict['title'] = unicode(a_element['title']).encode('utf-8')
                report_organization, report_title = zhongwen_cute(elem_dict['title'])
                elem_dict['report_organization'] = report_organization
                elem_dict['report_title'] = report_title
                elem_dict['url'] = a_element['href']
                elem_dict['time'] = unicode(elem.find('span').string).encode('utf-8')
                elem_dict['report_date'] = elem_dict['time'].split(' ')[0].replace('-','')
                elem_dict['file_name'] = 'qsyb' + str(elem_dict['report_date']) + '#' + elem_dict['url'][-12:-5] + '.pdf'
                elem_dict['report_id'] = str(elem_dict['report_date']) + elem_dict['url'][-12:-5]
                base_url_list.append(elem_dict)
            # print a_element['title']
    return change_list(base_url_list)

#基于report地址，获取pdf地址，pdf文件名，报告内容
def get_report_message(report_url):
    article_html = get_html(report_url)
    pdf_url = ''
    pdf_name = ''
    contents = ''
    if article_html == '':
        pass
    else:
        try:
            soup = BeautifulSoup(article_html,"html.parser")
            main_element = soup.find(class_='main')
            main_content =  main_element.find('div').strings
            contents = ''
            for content in main_content:
                contents = contents + content

            pdf_url = main_element.find('a')['href']
            pdf_name = main_element.find('a').string
        except:
            print "content not exists."
        # print "title:",soup.find(class_='tit').find(class_='fl').string
        # print "contents:",contents
        # print "pdf_url:",main_element.find('a')['href']
        # print "pdf_name:",main_element.find('a').string
    return pdf_url,pdf_name,contents

#测试使用
def spider_report_control(interval,flag):
    i = 0
    while ((i < 8) and (not flag)):
        print "test..."
        current_date = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        print current_date
        time.sleep(interval['driver'])
        i = i + 1

def change_list(array_list):
    new_array_list = []
    list_len = len(array_list)
    for i in range(list_len):
        new_array_list.append(array_list[list_len-i-1])
    return new_array_list

def zhongwen_cute(words):
    report_word = words.split('--')
    report_organization = report_word[0]
    report_title = report_word[1].split('【')[0]
    # print "report_organization:",report_organization
    # print "report_title:",report_title
    return report_organization, report_title

if __name__ == '__main__':
    #获取基础对象
    base_report_type_url_list = get_base_report_type_url()
    #遍历5大类
    # for base_report_type_url in base_report_type_url_list:
    #     print base_report_type_url['report_url']
    #     page_count = get_page_count_soup(base_report_type_url['report_url'])
    #     print "report_type:", base_report_type_url['report_type'] ," page count:",page_count

    #获取page_count
    base_report_type_url = base_report_type_url_list[2]['report_url']
    page_count = get_page_count(base_report_type_url)

    #访问mysql  获取mysql总记录数
    mysql_count = 49
    last_time = '2010-03-06 12:34:44'

    start_page_number = int(page_count - math.floor((mysql_count)/50))
    print start_page_number

    #构造page url
    page_url_list = []
    for i in range(start_page_number):
        page_number = start_page_number - i
        report_type_url = base_report_type_url.replace('.html','_p' + str(page_number) + '.html')
        page_url_list.append(report_type_url)
    print len(page_url_list)
    print page_url_list[0],page_url_list[-1]


    #通过page url获取所有报告地址
    base_url = page_url_list[0]
    report_url_list = get_article_url_list(base_url)
    for report_url in report_url_list:
        print report_url

    #通过report 地址获取详细信息
    pdf_url,pdf_name,contents = get_report_message(report_url_list[-1])



