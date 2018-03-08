#coding=utf-8
__author__ = 'shifx'

from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误
from research_report.models import ReportUser
from django.shortcuts import render_to_response
from research_report.thread import ThreadControl

#主页面
def report_main(request):
    # ProbTotals.objects.all().delete()
    # thread_list =  ProbUser.objects.get(thread_name=th_name)
    report_user_list =  ReportUser.objects.all()
    for prob_user in report_user_list:
        c  = ThreadControl()
        try:
            #查看是否处于活跃状态
            status = c.is_alive(prob_user.report_name)
            if status:
                #设置状态为1
                prob_user.report_status = 1
                prob_user.save()
            else:
                #设置状态为0
                prob_user.report_status = 0
                prob_user.save()
        except:
            print prob_user.report_name, " not start"
            prob_user.report_status = 0
            prob_user.save()
    return render_to_response('report_main.html',{"report_user_list":report_user_list})


@csrf_exempt   #处理Post请求出错的情况
def control_report_thread(request):
    report_name = request.POST['user_name']
    control = request.POST['control']
    info_dict = {}

    #显示活跃状态
    report_user = ReportUser.objects.get(report_name=report_name)
    if control == 'start':
        driver = 3
        info_dict["driver"] = driver
        #状态信息
        c  = ThreadControl()
        #出现错误，则线程不存在，因此启动线程
        try:
            status = c.is_alive(report_name)
            print "thread is alive? ",status
            if status:
                print "thread is alive,caonot start twice!"
            else:
                print "start ..........thread1"
                c.start(report_name, info_dict)
        except:
            print "thread is not alive start!!!"
            c.start(report_name, info_dict)
        report_user.report_status = 1
        report_user.save()
    if control == 'stop':
        c  = ThreadControl()
        try :
            c.stop(report_name)
            report_user.report_status = 0
            report_user.save()
        except:
            print "not thread alive"
    report_user_list =  ReportUser.objects.all()
    return render_to_response('report_main.html',{"report_user_list":report_user_list})

def set_user(request):
    try:
        # user_name = request.POST['in_user']
        # user_password = request.POST['in_pwd']
        # control = request.POST['control']

        report_name = 'research_report_1'
        report_desc = '研究报告'
        control = 'add'
        report_id = len(ReportUser.objects.all()) + 1
        report_status = False
        if(control == 'add'):
            obj_pro = ReportUser(report_id=report_id, report_name=report_name, report_desc=report_desc, report_status=report_status)
            obj_pro.save()
        if(control == 'delete'):
            ReportUser.objects.filter(report_name=report_name).delete()
        obj_pro = ReportUser.objects.all()
    except:
        obj_pro = ReportUser.objects.all()
        return render_to_response('report_main.html', {"report_user_list":obj_pro})

    return render_to_response('report_main.html', {"report_user_list":obj_pro})