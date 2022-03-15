# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import model_utils.fields
import autoslug.fields
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=250, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique_with=('id',), null=True, editable=False)),
                ('website', models.URLField(blank=True)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=50)),
                ('state_province', models.CharField(max_length=50, blank=True)),
                ('postal_code', models.CharField(max_length=50)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('industry', model_utils.fields.StatusField(default='manufacturing', max_length=100, no_check_for_status=True, choices=[('Chemical', 'Chemical'), ('Mining', 'Mining'), ('Food', 'Food'), ('Basic Materials', 'Basic Materials'), ('Services', 'Services'), ('Transportation', 'Transportation'), ('Healthcare', 'Healthcare'), ('Technology', 'Technology'), ('Communication', 'Communication'), ('manufacturing', 'manufacturing')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('title', models.CharField(max_length=300, blank=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('skype', models.CharField(max_length=50, blank=True)),
                ('whatsapp', models.CharField(max_length=50, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(to='company.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=128)),
                ('product_description', models.TextField(max_length=500, blank=True)),
                ('product_hs_code', models.CharField(max_length=15, null=True)),
                ('cost_goods_sold', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('wholesale_price', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('retail_price', models.DecimalField(default=0.0, max_digits=9, decimal_places=2)),
                ('daily_production', models.DecimalField(default=0.0, max_digits=9, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(to='company.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
