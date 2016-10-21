# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0010_auto_20160717_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationmark',
            name='city',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='locationmark',
            name='country',
            field=models.TextField(null=True, blank=True),
        ),
    ]
