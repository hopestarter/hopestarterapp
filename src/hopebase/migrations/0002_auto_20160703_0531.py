# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hopebase.models


class Migration(migrations.Migration):

    dependencies = [
        ('hopebase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='large_picture',
            field=models.ImageField(max_length=255, upload_to=hopebase.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='medium_picture',
            field=models.ImageField(max_length=255, upload_to=hopebase.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='small_picture',
            field=models.ImageField(max_length=255, upload_to=hopebase.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='thumbnail_picture',
            field=models.ImageField(max_length=255, upload_to=hopebase.models.upload_image_to, null=True, editable=False, blank=True),
        ),
    ]
