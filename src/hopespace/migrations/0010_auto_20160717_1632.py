# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import hopespace.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hopespace', '0009_locationmark_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationimageupload',
            name='mark',
        ),
        migrations.AlterModelOptions(
            name='locationmark',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='locationmark',
            name='large_picture',
            field=models.ImageField(max_length=255, upload_to=hopespace.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='locationmark',
            name='medium_picture',
            field=models.ImageField(max_length=255, upload_to=hopespace.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='locationmark',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 17, 16, 32, 18, 259121, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locationmark',
            name='picture',
            field=models.ImageField(max_length=255, null=True, upload_to=hopespace.models.upload_image_to, blank=True),
        ),
        migrations.AddField(
            model_name='locationmark',
            name='small_picture',
            field=models.ImageField(max_length=255, upload_to=hopespace.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='locationmark',
            name='thumbnail_picture',
            field=models.ImageField(max_length=255, upload_to=hopespace.models.upload_image_to, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='ethnicity',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ethnicity',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ethnicmember',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ethnicmember',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='locationmark',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='LocationImageUpload',
        ),
    ]
