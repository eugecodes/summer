#company/admin.py
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib import admin
from . models import Contact, Company, Product, RequestedLead
# Register your models here.
admin.site.register(Contact)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(RequestedLead)