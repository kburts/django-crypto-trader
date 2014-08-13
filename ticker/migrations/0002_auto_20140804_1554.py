# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ticker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='currency1',
            field=models.ForeignKey(default=0, to='ticker.Currency'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pair',
            name='currency2',
            field=models.ForeignKey(default=0, to='ticker.Currency'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='currency',
            name='pair',
        ),
    ]
