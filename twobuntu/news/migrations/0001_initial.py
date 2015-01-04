# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title of the news item.', max_length=100)),
                ('body', models.TextField(help_text=b'The body of the news item [in Markdown].')),
                ('url', models.URLField(help_text=b'URL with more details about the news item.')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reporter', models.ForeignKey(help_text=b'The user reporting the news item.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
    ]
