# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20160222_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestedLead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pending', models.BooleanField(default=True)),
                ('rejected', models.BooleanField(default=False)),
                ('lead_company', models.CharField(max_length=300, null=True, blank=True)),
                ('first_name', models.CharField(max_length=300, null=True, blank=True)),
                ('last_name', models.CharField(max_length=300, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('title', models.CharField(max_length=300, blank=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=model_utils.fields.StatusField(default='Manufacturing', max_length=100, no_check_for_status=True, choices=[(0, 'dummy')]),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(related_name='contacts', to='company.Company'),
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(related_name='products', to='company.Company'),
        ),
        migrations.AddField(
            model_name='requestedlead',
            name='company',
            field=models.ForeignKey(related_name='requestedleads', to='company.Company'),
        ),
    ]
