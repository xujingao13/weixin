# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=30)),
                ('user_ord', models.IntegerField()),
                ('startTime', models.IntegerField()),
                ('endTime', models.IntegerField()),
                ('type', models.IntegerField()),
                ('distance', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('steps', models.IntegerField()),
                ('subType', models.IntegerField()),
                ('actTime', models.IntegerField()),
                ('nonActTime', models.IntegerField()),
                ('dsNum', models.IntegerField()),
                ('lsNum', models.IntegerField()),
                ('wakeNum', models.IntegerField()),
                ('wakeTimes', models.IntegerField()),
                ('score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RingUser',
            fields=[
                ('user_id', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('user_ord', models.IntegerField()),
                ('sex', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('target', models.IntegerField()),
                ('last_record', models.IntegerField()),
            ],
        ),
    ]
