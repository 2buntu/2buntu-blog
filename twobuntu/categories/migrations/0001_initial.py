# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the category.', max_length=40)),
                ('image', models.ImageField(help_text=b'A representative image.', null=True, upload_to=b'categories', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
    ]
