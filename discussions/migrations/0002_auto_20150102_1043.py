# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='parent_post',
            field=models.ForeignKey(related_name='replies', blank=True, to='discussions.Post', null=True),
            preserve_default=True,
        ),
    ]
