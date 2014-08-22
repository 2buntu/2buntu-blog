# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('caption', models.CharField(help_text='A brief description of the image.', max_length=100)),
                ('image', models.ImageField(help_text='The image file.', upload_to='images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
