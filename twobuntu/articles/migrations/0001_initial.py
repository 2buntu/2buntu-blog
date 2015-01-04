# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title of the article.', max_length=200)),
                ('body', models.TextField(help_text=b'The body of the article [in Markdown].')),
                ('status', models.PositiveSmallIntegerField(default=0, help_text=b'The current status of the article.', choices=[(0, b'Draft'), (1, b'Unapproved'), (2, b'Published')])),
                ('cc_license', models.BooleanField(default=True, help_text=b'Whether the article is released under the CC-BY-SA 4.0 license or not.')),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ('status', '-date'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScheduledArticle',
            fields=[
                ('article', models.OneToOneField(primary_key=True, serialize=False, to='articles.Article')),
                ('date', models.DateTimeField(help_text=b'Date/time to publish article (YYYY-MM-DD HH:MM:SS).')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(help_text=b'The user writing the article.', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(help_text=b'The category of the article.', to='categories.Category'),
            preserve_default=True,
        ),
    ]
