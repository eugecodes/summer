#company/serializers.py
from __future__ import unicode_literals
from rest_framework import serializers
from . models import Company, Product, Contact, RequestedLead


class ProductSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = '__all__'


class RequestedLeadSerializer(serializers.ModelSerializer):

	class Meta:
		model = RequestedLead
		fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):

	contacts = ContactSerializer(many=True)
	products = ProductSerializer(many=True)
	requestedleads = RequestedLeadSerializer(many=True)
	class Meta:
		model = Company
		fields = '__all__'