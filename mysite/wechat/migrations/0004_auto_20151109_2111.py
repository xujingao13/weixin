# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_record_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
