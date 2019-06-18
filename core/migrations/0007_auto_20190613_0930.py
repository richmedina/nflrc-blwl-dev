# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190613_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmembership',
            name='user',
            field=models.ForeignKey(related_name='member_projects', to='core.Whitelist'),
            preserve_default=True,
        ),
    ]
