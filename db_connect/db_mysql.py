#coding=utf-8
__author__ = 'shifx'
import MySQLdb

def mysql_connect():
    try:
        mysql_conn = MySQLdb.connect("127.0.0.1","root","123456","db_finance")
    except:
        print "connect mysql error"
        return None
    return mysql_conn

#写入mysql mysql数据库需要将unnicode转换成str
def insert_mysql_t_finance_report(mysql_conn,*args):
    # print args
    if len(args) == 11:
        report_id = args[0]
        publish_date = args[1]
        report_type_id = args[2]
        report_type = args[3]
        report_title = args[4]
        report_organization = args[5]
        file_size = args[6]
        page_count = args[7]
        file_url = args[8]
        report_content = args[9]
        file_local_path = args[10]

        # abstract_author = abstract_author.replace("'","''")
        # print article_id, article_url, publication_title
        # print "type abstract_author:::::::",type(abstract_author)
        # print "abstract_author:::::::",abstract_author
    # time.sleep(3)
    if 1:
        mysql_cursor = mysql_conn.cursor()
        # sql = '''insert into db_finance.t_finance_report (report_id, publish_date, report_type_id, report_type, report_title,
        #           report_organization, file_size, page_count, file_url, report_content, file_local_path) values('%s', '%s', '%d', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s')''' \
        #             %(report_id, publish_date, report_type_id, report_type, report_title,report_organization, file_size, page_count, file_url, report_content, file_local_path)

        sql = '''insert into db_finance.t_finance_report (report_id, publish_date, report_type_id, report_type, report_title,
                  report_organization, file_size, page_count, file_url, report_content, file_local_path) values(report_id, publish_date, report_type_id, report_type, report_title,report_organization, file_size, page_count, file_url, report_content, file_local_path)'''
        print "sql:",sql
        mysql_cursor.execute(sql)
        mysql_conn.commit()
    else:
        print "insert article into faild!"
    # time.sleep(3)
    return 0