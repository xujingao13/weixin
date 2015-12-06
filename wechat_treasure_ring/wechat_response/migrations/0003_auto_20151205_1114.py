# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_response', '0002_remove_ringuser_user_ord'),
    ]

    operations = [
        migrations.AddField(
            model_name='ringuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ringuser',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
    ]
