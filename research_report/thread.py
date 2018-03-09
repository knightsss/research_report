#coding=utf-8
__author__ = 'shifeixiang'
import time
import math
import threading
import datetime
from research_report.spider_report import spider_report_control,get_page_count,get_article_url_list,get_report_message
from research_report.base_data_message import get_base_report_type_url
from report_pdf import download_pdf,reload_pdf
from db_connect.db_mysql import mysql_connect,insert_mysql_t_finance_report,get_mysql_record
class Spider(threading.Thread):
    # __metaclass__ = Singleton
    thread_stop = False
    thread_num = 0
    interval = {}
    behavior = None
    def run(self):
        self.behavior(self,self.thread_num,self.interval)
    def stop(self):
        self.thread_stop = True

class ThreadControl():
    thread_stop = False
    current_thread = {}
    def start(self,thread_num,interval):
        spider = Spider()
        spider.behavior = loaddata
        spider.thread_num = thread_num
        spider.interval = interval
        spider.start()
        self.current_thread[str(thread_num)] = spider
    #判断进程是否活跃
    def is_alive(self,thread_num):
        tt = self.current_thread[str(thread_num)]
        return tt.isAlive()
    #获取当前线程名称
    # def get_name(self):
    def stop(self,thread_num):
        print "stop"
        spider = self.current_thread[str(thread_num)]
        spider.stop()

def loaddata(c_thread,thread_num,interval):
    base_date = time.strftime("%Y%m%d", time.localtime())
    count = 0
    #初次启动开始购买---可以通过购买记录来初始化last_minute
    last_minute = -1
    while not c_thread.thread_stop:
        current_minute = (datetime.datetime.now()).minute
        #predict.main.spider_save_predict(interval)
        # print "current_minute ",current_minute
        current_date = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        print current_date
        # time.sleep(interval['driver'])
        # spider_report_control(interval,c_thread.thread_stop)

        #获取所有类别
        base_report_type_url_list = get_base_report_type_url()
        report_class_len = len(base_report_type_url_list)
        report_class_index = 0

        #连接mysql
        mysql_conn = mysql_connect()

        while ((report_class_index < report_class_len) and (not c_thread.thread_stop)):
            # print "test..."
            # current_date = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
            # print current_date
            time.sleep(interval['driver'])

            #获取page_count
            base_report_type_url = base_report_type_url_list[report_class_index]['report_url']
            page_count = get_page_count(base_report_type_url)

            #如果网络异常，则出现为0的情况
            if page_count>0:
                #查询mysql
                #访问mysql  获取mysql总记录数,条件 报告类型：券商晨会 report_type 或者id
                mysql_count,last_publish_date = get_mysql_record(mysql_conn,base_report_type_url_list[report_class_index]['report_type_id'])
                print "mysql_count:",mysql_count
                #构造起始页码
                start_page_number = int(page_count - math.floor((mysql_count)/50))
                print "start_page_number:",start_page_number
                #构造page_url,总共需要访问多少页
                page_url_list = []
                for i in range(start_page_number):
                    page_number = start_page_number - i
                    report_type_url = base_report_type_url.replace('.html','_p' + str(page_number) + '.html')
                    page_url_list.append(report_type_url)

                #通过page url获取当页所有报告地址
                page_url_list_len = len(page_url_list)
                page_url_index = 0
                while ((page_url_index<page_url_list_len) and (not c_thread.thread_stop)):
                    page_url = page_url_list[page_url_index]
                    print "page_url:",page_url
                    # #测试
                    # page_url = 'http://istock.jrj.com.cn/yanbao_1_p648.html'
                    report_element_list = get_article_url_list(page_url)
                    #网络异常的时候 report_url_list为空
                    if len(report_element_list) == 0:
                        print "request http error..."
                        break
                    else:
                        print "========================================="
                        print "report_element_list len:",len(report_element_list)
                        for report_element in report_element_list:
                            if(not c_thread.thread_stop):
                                #判断时间是否已经采集过
                                print "last_publish_date: ",last_publish_date, "time: ",datetime.datetime.strptime(report_element['time'], "%Y-%m-%d %H:%M:%S")
                                if last_publish_date > datetime.datetime.strptime(report_element['time'], "%Y-%m-%d %H:%M:%S"):
                                    print report_element['url']," exists"
                                else:
                                    print "report_url:", report_element['url']
                                    #通过report 地址获取详细信息
                                    pdf_url,pdf_name,contents = get_report_message(report_element['url'])
                                    # pdf_url,pdf_name,contents = get_report_message('http://istock.jrj.com.cn/article,yanbao,24587410.html')
                                    #出现异常,pdf_url为空
                                    if pdf_url != '':
                                        #判断下载pdf是否异常，异常跳过
                                        file_name = report_element['file_name'] + '.'+ (pdf_url.split('.')[-1]).encode('utf-8')

                                        # print "file_name:",file_name
                                        # print "file_name:",type(file_name)
                                        download_result = download_pdf(pdf_url,file_name)
                                        if download_result:
                                            page_count,file_size = reload_pdf(file_name)
                                            #判断打开文件是否异常
                                            if page_count == 0 and file_size == 0:
                                                print "file load error!"
                                            else:
                                                print "insert into mysql"

                                                #判断mysql连接是否异常
                                                if mysql_conn == 0:
                                                    print "mysql connect error, exit!"
                                                    c_thread.thread_stop = True
                                                else:
                                                    report_id = report_element['report_id']
                                                    publish_date = report_element['time']
                                                    report_type_id = base_report_type_url_list[report_class_index]['report_type_id']
                                                    report_type = base_report_type_url_list[report_class_index]['report_type']
                                                    report_title = report_element['report_title']
                                                    report_organization = report_element['report_organization']
                                                    file_size = file_size
                                                    page_count = page_count
                                                    file_url = report_element['url']
                                                    report_content = contents
                                                    file_local_path = file_name
                                                    insert_mysql_t_finance_report(mysql_conn,report_id, publish_date, report_type_id, report_type, report_title,report_organization, file_size, page_count, file_url, report_content, file_local_path)
                                                    print "insert sucess!"
                                                #存储mysql数据库
                                        else:
                                            print "download error"
                                    else:
                                        print "get content error"
                            else:
                                print "spider stop ...."
                                break
                            # time.sleep(1)

                    page_url_index = page_url_index + 1
                    time.sleep(3)
                # print len(page_url_list)
                # print page_url_list[0],page_url_list[-1]
            else:
                print base_report_type_url," get page count error"

            report_class_index = report_class_index + 1

    print "exit!"
