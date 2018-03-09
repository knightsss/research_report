#coding=utf-8
__author__ = 'shifx'

#获取最基础的报告类型url ---公司研究 行业研究
def get_base_report_type_url():
    base_report_type_url_list = []


    report_dict = {}
    report_dict['report_type_id'] = 3
    report_dict['report_type'] = '公司研究'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_3.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 8
    report_dict['report_type'] = '投资策略'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_8.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 9
    report_dict['report_type'] = '晨会纪要'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_9.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 1
    report_dict['report_type'] = '宏观研究'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_1.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 2
    report_dict['report_type'] = '行业研究'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_2.html'
    base_report_type_url_list.append(report_dict)

    return base_report_type_url_list