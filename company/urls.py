#company/urls
from __future__ import absolute_import
from django.conf.urls import url
from django.views.generic import TemplateView
from company import views


urlpatterns =[
	url(r'^add_company/$', 'company.views.general_info', name='general_info'),
	url(r'^economic/$', 'company.views.economic_info', name='economic_info'),
	url(r'^add_product/$', 'company.views.product_info', name='product_info'),
	url(r'^$', TemplateView.as_view(template_name='company/customers.html'), name='customers'),
	url(r'^customer-detail/$', TemplateView.as_view(template_name='company/customer_detail.html'), name='customer_detail'),
	]