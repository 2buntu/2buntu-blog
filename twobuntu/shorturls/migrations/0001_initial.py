# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import twobuntu.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('key', models.CharField(primary_key=True, max_length=6, serialize=False, default=twobuntu.utils.uuid6)),
                ('url', models.URLField(help_text='URL to redirect the client to.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
