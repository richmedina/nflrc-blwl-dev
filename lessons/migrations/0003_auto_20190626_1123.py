# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_20190530_0543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessonmodule',
            options={'ordering': ['order']},
        ),
    ]
