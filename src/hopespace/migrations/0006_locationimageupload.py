# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0005_auto_20160223_0615'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationImageUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(editable=False, blank=True)),
                ('modified', models.DateTimeField(editable=False, blank=True)),
                ('url', models.URLField(max_length=100, null=True, blank=True)),
                ('mark', models.ForeignKey(related_name='images', to='hopespace.LocationMark')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
