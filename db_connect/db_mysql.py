#coding=utf-8
__author__ = 'shifx'
import MySQLdb
import datetime
def mysql_connect():
    try:
        mysql_conn = MySQLdb.connect("127.0.0.1","root","123456","db_finance",charset="utf8")
    except:
        print "connect mysql error"
        return 0
    return mysql_conn

#写入mysql mysql数据库需要将unnicode转换成str
def insert_mysql_t_finance_report(mysql_conn,*args):
    # print args
    # print len(args)
    if len(args) == 11:
        report_id = args[0]
        publish_date = args[1]
        report_type_id = int(args[2])
        report_type = args[3]
        report_title = args[4]
        report_organization = args[5]
        file_size = int(args[6])
        page_count = int(args[7])
        file_url = args[8]
        report_content = args[9].replace("'","''")
        file_local_path = args[10]

        # print type(report_id)
        # print type(publish_date)
        # print "report_type_id type:",type(report_type_id)
        # print "content type ",type(report_content)
        # print "file ",type(file_size)
        # print "count ",type(page_count)

        # abstract_author = abstract_author.replace("'","''")
        # print article_id, article_url, publication_title
        # print "type abstract_author:::::::",type(abstract_author)
        # print "abstract_author:::::::",abstract_author
    # time.sleep(3)
    if 1:
        mysql_cursor = mysql_conn.cursor()
        sql = '''insert into db_finance.t_finance_report (report_id, publish_date, report_type_id, report_type, report_title, \
                  report_organization, file_size, page_count, file_url, report_content, file_local_path) values('%s', '%s', '%d', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s')''' \
                    %(report_id, publish_date, report_type_id, report_type, report_title,report_organization, file_size, page_count, file_url, report_content, file_local_path)

        write_file(sql)
        # sql = '''insert into db_finance.t_finance_report (report_id, publish_date, report_type_id, report_type, report_title,
        #           report_organization, file_size, page_count, file_url, report_content, file_local_path) values(report_id, publish_date,
        #           report_type_id, report_type, report_title,report_organization, file_size, page_count, file_url, report_content, file_local_path)'''

        mysql_cursor.execute(sql)
        mysql_conn.commit()
    else:
        print "insert article into faild!"
    # time.sleep(3)
    return 0


def get_mysql_record(mysql_conn,report_type_id):
    mysql_cursor = mysql_conn.cursor()
    sql1 = "SELECT publish_date FROM db_finance.t_finance_report WHERE report_type_id = '%d' order by publish_date desc limit 1;" % (report_type_id)
    mysql_cursor.execute(sql1)
    data = mysql_cursor.fetchone()
    try:
        last_publish_date = data[0]
    except:
        last_publish_date = datetime.datetime.strptime("2010-06-07 9:34:45", "%Y-%m-%d %H:%M:%S")

    sql2 = "SELECT count(*) FROM db_finance.t_finance_report WHERE report_type_id = '%d'" % (report_type_id)
    mysql_cursor.execute(sql2)
    result = mysql_cursor.fetchone()
    try:
        record_count = result[0]
    except:
        record_count = 1
    return record_count,last_publish_date

def write_file(sql):
    f = open("sql.sql",'w')
    f.write(sql)
    f.close()