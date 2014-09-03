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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(help_text='The name of the category.', max_length=40)),
                ('image', models.ImageField(help_text='A representative image.', blank=True, null=True, upload_to='categories')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
    ]
