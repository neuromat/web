# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-13 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('link', models.CharField(max_length=255, verbose_name='Link')),
                ('icon_class', models.CharField(max_length=255, verbose_name='Font Awesome class')),
            ],
            options={
                'verbose_name': 'Social link',
                'verbose_name_plural': 'Social links',
                'ordering': ('title',),
            },
        ),
    ]
