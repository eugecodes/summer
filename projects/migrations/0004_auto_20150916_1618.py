# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django_countries.fields
import django.utils.timezone
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('title', models.CharField(max_length=300, null=True, blank=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('skype', models.CharField(max_length=50, null=True, blank=True)),
                ('whatsapp', models.CharField(max_length=50, null=True, blank=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=300)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'company_name', null=True, editable=False, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('address1', models.CharField(max_length=300, null=True, blank=True)),
                ('address2', models.CharField(max_length=300, null=True, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('state_province', models.CharField(max_length=300, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=10, null=True, blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('modified_at', models.DateTimeField(null=True, verbose_name='modified date', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.AddField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(to='projects.Customer'),
            preserve_default=True,
        ),
    ]
