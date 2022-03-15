# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myusers', '0003_auto_20160121_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='title',
        ),
    ]
