# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0006_locationimageupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationimageupload',
            name='mark',
            field=models.ForeignKey(related_name='picture', to='hopespace.LocationMark'),
        ),
    ]
