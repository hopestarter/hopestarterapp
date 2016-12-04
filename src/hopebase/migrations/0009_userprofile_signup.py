# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopebase', '0008_auto_20161203_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='signup',
            field=models.SlugField(default=b'app', choices=[(b'app', b'app'), (b'web', b'web'), (b'ngo', b'ngo')]),
        ),
    ]
