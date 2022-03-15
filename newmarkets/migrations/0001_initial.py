# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso2code', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('iso3code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=200)),
                ('capital', models.CharField(max_length=200)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6)),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HSProduct',
            fields=[
                ('hs_number', models.CharField(max_length=10, serialize=False, primary_key=True, blank=True)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='IntracenImportData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imported_value', models.DecimalField(default=0.0, null=True, max_digits=12, decimal_places=2)),
                ('imported_time', models.PositiveSmallIntegerField()),
                ('country', models.ForeignKey(to='newmarkets.Country')),
                ('hs_number', models.ForeignKey(to='newmarkets.HSProduct')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='country',
            field=models.ManyToManyField(to='newmarkets.HSProduct', through='newmarkets.IntracenImportData'),
        ),
    ]
