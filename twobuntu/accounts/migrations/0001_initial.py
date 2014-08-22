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
                ('key', models.CharField(max_length=32, default=twobuntu.utils.uuid)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthday', models.DateField(help_text='Birthday in YYYY-MM-DD format [used for displaying age].', blank=True, null=True)),
                ('location', models.CharField(help_text='Geographic location.', blank=True, max_length=40)),
                ('website', models.URLField(help_text='A personal blog or website.', blank=True)),
                ('bio', models.TextField(help_text='A brief biography.', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
