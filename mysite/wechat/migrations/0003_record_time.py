# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_remove_record_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.DateField(default=datetime.datetime(2015, 11, 9, 12, 35, 4, 537633, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
