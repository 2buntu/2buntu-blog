# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.CharField(help_text=b'The name of the product being advertised.', max_length=100)),
                ('image', models.ImageField(help_text=b'An image depicting the advertised product.', upload_to=b'ads')),
                ('url', models.URLField(help_text=b'The URL that will be displayed when the image is selected.')),
                ('display_start', models.DateTimeField(help_text=b'When the ad should start being displayed.')),
                ('display_end', models.DateTimeField(help_text=b'When the ad should stop being displayed.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
