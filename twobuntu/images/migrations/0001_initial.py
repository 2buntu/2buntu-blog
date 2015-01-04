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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(help_text=b'A brief description of the image.', max_length=100)),
                ('image', models.ImageField(help_text=b'The image file.', upload_to=b'images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
