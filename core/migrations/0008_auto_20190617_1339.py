# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190613_0930'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectmembership',
            unique_together=set([('project', 'user')]),
        ),
    ]
