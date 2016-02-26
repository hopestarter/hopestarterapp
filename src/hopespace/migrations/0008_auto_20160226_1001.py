# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0007_auto_20160225_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationimageupload',
            name='url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
