# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import twobuntu.utils


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationKey',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('key', models.CharField(default=twobuntu.utils.uuid, max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthday', models.DateField(help_text=b'Birthday in YYYY-MM-DD format [used for displaying age].', null=True, blank=True)),
                ('location', models.CharField(help_text=b'Geographic location.', max_length=40, blank=True)),
                ('website', models.URLField(help_text=b'A personal blog or website.', blank=True)),
                ('bio', models.TextField(help_text=b'A brief biography.', blank=True)),
            ],
            options={
                'ordering': ('-user__last_login',),
            },
            bases=(models.Model,),
        ),
    ]
