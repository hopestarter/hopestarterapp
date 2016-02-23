# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0004_auto_20160219_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethnicmember',
            name='ethnicity',
            field=models.ForeignKey(related_name='ethnicity', to='hopespace.Ethnicity'),
        ),
    ]
