# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_id', models.IntegerField()),
                ('report_name', models.CharField(max_length=30)),
                ('report_desc', models.CharField(max_length=30)),
                ('report_status', models.BooleanField()),
            ],
        ),
    ]