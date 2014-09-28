# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('icon_url', models.ImageField(upload_to=b'apps/icons')),
                ('title', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('license', models.CharField(max_length=40)),
                ('website', models.URLField()),
                ('download_url', models.URLField()),
                ('download_size', models.PositiveIntegerField()),
                ('rating', models.PositiveSmallIntegerField()),
                ('last_updated', models.DateTimeField()),
                ('date_published', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'apps/screenshots')),
                ('application', models.ForeignKey(to='touch.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='department',
            field=models.ForeignKey(to='touch.Department'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='keywords',
            field=models.ManyToManyField(to='touch.Keyword'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='publisher',
            field=models.ForeignKey(to='touch.Publisher'),
            preserve_default=True,
        ),
    ]
