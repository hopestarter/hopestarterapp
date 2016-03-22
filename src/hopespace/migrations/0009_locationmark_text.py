# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0008_auto_20160226_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationmark',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
