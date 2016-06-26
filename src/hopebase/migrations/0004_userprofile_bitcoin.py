# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopebase', '0003_auto_20160226_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bitcoin',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
