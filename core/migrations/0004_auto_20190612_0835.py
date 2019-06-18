# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190612_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelist',
            name='project',
            field=models.ForeignKey(related_name='member_list', to='lessons.Project', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='whitelist',
            name='site_account',
            field=models.ForeignKey(related_name='membership', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
