# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0003_auto_20160211_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethnicity',
            options={'ordering': ['name'], 'verbose_name_plural': 'ethnicities'},
        ),
    ]
