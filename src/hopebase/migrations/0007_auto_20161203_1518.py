# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations
from django.db.models import Count


def add_missing_stats(apps, schema_editor):
    LocationMark = apps.get_model("hopespace", "LocationMark")  # noqa
    User = apps.get_model("auth", "User")
    UserStats = apps.get_model("hopebase", "UserStats")
    # we do all the users since some counts might be wrong
    for user in User.objects.annotate(post_count=Count('marks')):
        UserStats.objects.update_or_create(
            user=user, defaults={
                'post_count': user.post_count,
                'modified': datetime.utcnow()
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('hopebase', '0006_userstats'),
        ('hopespace', '0002_locationmark_user'),
    ]

    operations = [
        migrations.RunPython(add_missing_stats),
    ]
