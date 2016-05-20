# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(default=b'', help_text='Enter your first and last name.', max_length=64, verbose_name='Name', blank=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='name',
            field=models.CharField(default=b'', help_text='Enter your first and last name.', max_length=64, verbose_name='Name', blank=True),
        ),
    ]
