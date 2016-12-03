# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hopespace', '0011_locationmark_city_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationmark',
            name='hidden',
            field=models.ForeignKey(related_name='censored_posts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
