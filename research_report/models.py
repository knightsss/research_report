# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#用户表
class ReportUser(models.Model):
    report_id =  models.IntegerField()
    report_name = models.CharField(max_length=30)    #主键
    report_desc =  models.CharField(max_length=30)
    report_status = models.BooleanField()