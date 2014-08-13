# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ticker', '0002_auto_20140804_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticker',
            options={'ordering': [b'-timestamp']},
        ),
        migrations.AddField(
            model_name='exchange',
            name='priceJsonLoc',
            field=models.CharField(default='ticker,last', max_length=200,
                                   verbose_name=b"Comma seperated list of location to price in the response eg. 'ticker, last'"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(max_length=4, verbose_name=b'Symbol: Case sensitive'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='url',
            field=models.URLField(verbose_name=b"URL: API endpoint. Replace currencies with *'s."),
        ),
    ]
