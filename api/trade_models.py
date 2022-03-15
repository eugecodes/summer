import os
import sqlite3
import urllib
import urllib2
import json
import time
import requests
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
from StringIO import StringIO
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship, backref, scoped_session, sessionmaker
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime)
	
import flask.ext.sqlalchemy
import flask.ext.restless

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/tmp/app.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://argentina:mountains@twisted-dragon.cu3ugwf8wzsx.us-west-2.rds.amazonaws.com:5432/twisted'
db = flask.ext.sqlalchemy.SQLAlchemy(app)
#db = SQLAlchemy(app)

Base = declarative_base()
#Base.metadata.bind = engine

	
class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))

    @hybrid_property
    def _id(self):
        """
        Eve backward compatibility
        """
        return self.id

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=False)
	email = db.Column(db.String(120), unique=False)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

class Countries(db.Model):
	__tablename__ = 'countries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, unique=False)
	doc_count = db.Column(db.String(50), unique=False)
	
	def __init__(self, code, result_id, doc_count):
		self.code = code
		self.result_id = result_id
		self.doc_count = doc_count

	def __repr__(self):
		return '<Countries %s>' % self.code

class Industries(db.Model):
	__tablename__ = 'industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<Industries %s>' % self.code

class ItaIndustries(CommonColumns):
	__tablename__ = 'ita_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<ItaIndustries %s>' % self.code

class MarketResearchLibraryIndustries(CommonColumns):
	__tablename__ = 'market_research_library_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("market_research_library_results.id", use_alter=True, name='fk_marketresearchlibrary_ind_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<MarketResearchLibraryIndustries %s>' % self.code

class MarketResearchLibraryItaIndustries(CommonColumns):
	__tablename__ = 'market_research_library_ita_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("market_research_library_results.id", use_alter=True, name='fk_marketresearchlibrary_ita_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<MarketResearchLibraryItaIndustries %s>' % self.code
		
class MarketResearchLibraryAddress(CommonColumns):
	__tablename__ = 'market_research_library_address'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("market_research_library_results.id", use_alter=True, name='fk_marketresearchlibrary_address_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<MarketResearchLibraryAddress %s>' % self.code
		
class MarketResearchLibraryCountries(CommonColumns):
	__tablename__ = 'market_research_library_countries'
	id = db.Column(db.Integer, primary_key=True)
	country = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("market_research_library_results.id", use_alter=True, name='fk_marketresearchlibrary_country_resultid'), unique=False)
	
	def __init__(self, country, result_id):
		self.country = country
		self.result_id = result_id

	def __repr__(self):
		return '<MarketResearchLibraryCountries %s>' % self.country
		
class MarketResearchLibraryResults(CommonColumns):
	__tablename__ = 'market_research_library_results'
	id = db.Column(db.Integer, primary_key=True)
	search_performed_at = db.Column(db.String(255), unique=False)
	description = db.Column(db.Text, unique=False)
	title = db.Column(db.String(160), unique=False)
	url = db.Column(db.String(120), unique=False)
	report_type = db.Column(db.String(120), unique=False)
	expiration_date = db.Column(db.String(255), unique=False)
	
	industries = db.relationship(MarketResearchLibraryIndustries, backref=db.backref('market_research_library_industries'))
	itaindustries = db.relationship(MarketResearchLibraryItaIndustries, backref=db.backref('market_research_library_ita_industries'))
	addresses = db.relationship(MarketResearchLibraryAddress, backref=db.backref('market_research_library_address'))
	countries = db.relationship(MarketResearchLibraryCountries, backref=db.backref('market_research_library_countries'))
	
	def __init__(self, id, search_performed_at, description,title,url,report_type,expiration_date):
		self.id = id
		self.search_performed_at = search_performed_at
		self.description = description
		self.title = title
		self.url = url
		self.report_type = report_type
		self.expiration_date = expiration_date

	def __repr__(self):
		return '<MarketResearchLibraryResults %s>' % self.id

class Sources(CommonColumns):
	__tablename__ = 'sources'
	id = db.Column(db.Integer, primary_key=True)
	source = db.Column(db.String(255), unique=False)
	source_last_updated = db.Column(db.String(255), unique=False)
	last_imported = db.Column(db.String(255), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)
	
	def __init__(self, source, source_last_updated,last_imported,search_performed_at):
		self.source = source
		self.source_last_updated = source_last_updated
		self.last_imported = last_imported
		self.search_performed_at = search_performed_at

	def __repr__(self):
		return '<Sources %s>' % self.id
	
class ConsolidatedScreenListAddresses(CommonColumns):
	__tablename__ = 'consolidated_screen_list_address'
	id = db.Column(db.Integer, primary_key=True)
	address = db.Column(db.String(255), unique=False)
	city = db.Column(db.String(40), unique=False)
	state = db.Column(db.String(40), unique=False)
	postal_code = db.Column(db.String(40), unique=False)
	country = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("consolidated_screen_list_results.id", use_alter=True, name='fk_consolidated_address_resultid'), unique=False)
	
	def __init__(self,address,city,state,postal_code,country,result_id):
		self.address = address
		self.city = city
		self.state = state
		self.postal_code = postal_code
		self.country = country
		self.result_id = result_id

	def __repr__(self):
		return '<ConsolidatedScreenListAddresses %s>' % self.id
	
class ConsolidatedScreenListResults(CommonColumns):
	__tablename__ = 'consolidated_screen_list_results'
	id = db.Column(db.Integer, primary_key=True)
	end_date = db.Column(db.String(255), unique=False)
	federal_register_notice = db.Column(db.String(255), unique=False)
	name = db.Column(db.String(1255), unique=False)
	remarks = db.Column(db.String(255), unique=False)
	source = db.Column(db.String(255), unique=False)
	source_information_url = db.Column(db.String(255), unique=False)
	source_list_url = db.Column(db.String(255), unique=False)
	standard_order = db.Column(db.String(255), unique=False)
	start_date = db.Column(db.String(255), unique=False)
	
	addresses = db.relationship(ConsolidatedScreenListAddresses, backref=db.backref('consolidated_screen_list_address'))
	
	def __init__(self,end_date,federal_register_notice,name,remarks,source,source_information_url,source_list_url,standard_order,start_date):
		self.end_date = end_date
		self.federal_register_notice = federal_register_notice
		self.name = name
		self.remarks = remarks
		self.source = source
		self.source_information_url = source_information_url
		self.source_list_url = source_list_url
		self.standard_order = standard_order
		self.start_date = start_date

	def __repr__(self):
		return '<ConsolidatedScreenListResults %s>' % self.id

class TradeEventVenues(CommonColumns):
	__tablename__ = 'trade_event_venues'
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(255), unique=False)
	country = db.Column(db.String(255), unique=False)
	state = db.Column(db.String(255), unique=False)
	venue = db.Column(db.Text, unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_event_results.id", use_alter=True, name='fk_tradeevent_venues_resultid'), unique=False)
	address = db.Column(db.String(255), unique=False)
	
	def __init__(self,city,country,state,venue,result_id,address):
	#def __init__(self,city):
		self.city = city
		self.country = country
		self.state = state
		self.venue = venue
		self.result_id = result_id
		self.address = address

	def __repr__(self):
		return '<TradeEventVenues %s>' % self.id

class TradeEventContacts(CommonColumns):
	__tablename__ = 'trade_event_contacts'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=False)
	first_name = db.Column(db.String(255), unique=False)
	last_name = db.Column(db.String(255), unique=False)
	person_title = db.Column(db.String(255), unique=False)
	phone = db.Column(db.String(255), unique=False)
	post = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_event_results.id", use_alter=True, name='fk_tradeevent_contacts_resultid'), unique=False)
	
	def __init__(self,email,first_name,last_name,person_title,phone,post,result_id):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.person_title = person_title
		self.phone = phone
		self.post = post
		self.result_id = result_id

	def __repr__(self):
		return '<TradeEventContacts %s>' % self.id

class TradeEventAggregations(CommonColumns):
	__tablename__ = 'trade_event_aggregations'
	id = db.Column(db.Integer, primary_key=True)
	doc_count = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_event_results.id", use_alter=True, name='fk_tradeevent_aggr_resultid'), unique=False)
	key = db.Column(db.String(255), unique=False)
	
	def __init__(self,doc_count,result_id,key):
		self.doc_count = doc_count
		self.result_id = result_id
		self.key = key

	def __repr__(self):
		return '<TradeEventAggregations %s>' % self.id

class TradeEventAggregationsCountries(CommonColumns):
	__tablename__ = 'trade_event_aggregations_countries'
	id = db.Column(db.Integer, primary_key=True)
	country = db.Column(db.String(50), unique=False)
	doc_count =  db.Column(db.Integer, unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_event_results.id", use_alter=True, name='fk_tradeevent_country_resultid'), unique=False)
	
	def __init__(self, country, doc_count, result_id):
		self.country = country
		self.doc_count = doc_count
		self.result_id = result_id

	def __repr__(self):
		return '<TradeEventAggregationsCountries %s>' % self.country

class TradeEventIndustries(CommonColumns):
	__tablename__ = 'trade_event_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_event_results.id", use_alter=True, name='fk_tradeevent_industries_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<TradeEventIndustries %s>' % self.code
		
class TradeEventsResults(CommonColumns):
	__tablename__ = 'trade_event_results'
	id = db.Column(db.Integer, primary_key=True)
	cost = db.Column(db.String(255), unique=False)
	event_name = db.Column(db.Text, unique=False)
	event_type = db.Column(db.String(255), unique=False)
	start_date = db.Column(db.String(255), unique=False)
	start_time = db.Column(db.String(255), unique=False)
	end_date = db.Column(db.String(255), unique=False)
	end_time = db.Column(db.String(255), unique=False)
	time_zone = db.Column(db.String(255), unique=False)
	registration_link = db.Column(db.Text, unique=False)
	registration_title = db.Column(db.Text, unique=False)
	description = db.Column(db.Text, unique=False)
	url = db.Column(db.Text, unique=False)
	
	vanues = db.relationship(TradeEventVenues, backref=db.backref('trade_event_venues'))
	contacts = db.relationship(TradeEventContacts, backref=db.backref('trade_event_contacts'))
	aggregations = db.relationship(TradeEventAggregations, backref=db.backref('trade_event_aggregations'))
	countries = db.relationship(TradeEventAggregationsCountries, backref=db.backref('trade_event_aggregations_countries'))
	industries = db.relationship(TradeEventIndustries, backref=db.backref('trade_event_industries'))
	
	def __init__(self,cost,event_name,event_type,start_date,start_time,end_date,end_time,time_zone,registration_link,registration_title,description,url):
		self.cost = cost
		self.event_name = event_name
		self.event_type = event_type
		self.start_date = start_date
		self.start_time = start_time
		self.end_date = end_date
		self.end_time = end_time
		self.time_zone = time_zone
		self.registration_link = registration_link
		self.registration_title = registration_title
		self.description = description
		self.url = url

	def __repr__(self):
		return '<TradeEventsResults %s>' % self.id
		
class TradeLeadCategories(CommonColumns):
	__tablename__ = 'trade_lead_categories'
	id = db.Column(db.Integer, primary_key=True)
	result_id = db.Column(db.Integer, ForeignKey("trade_lead_results.id", use_alter=True, name='fk_tradelead_category_resultid'), unique=False)
	code = db.Column(db.String(255), unique=False)
	
	def __init__(self,result_id,code):
		self.result_id = result_id
		self.code = code

	def __repr__(self):
		return '<TradeLeadCategories %s>' % self.id

class TradeLeadAggregations(CommonColumns):
	__tablename__ = 'trade_lead_aggregations'
	id = db.Column(db.Integer, primary_key=True)
	doc_count = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_lead_results.id", use_alter=True, name='fk_tradelead_aggr_resultid'), unique=False)
	key = db.Column(db.String(255), unique=False)
	
	def __init__(self,doc_count,result_id,key):
		self.doc_count = doc_count
		self.result_id = result_id
		self.key = key

	def __repr__(self):
		return '<TradeLeadAggregations %s>' % self.id

class TradeLeadIndustries(CommonColumns):
	__tablename__ = 'trade_lead_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_lead_results.id", use_alter=True, name='fk_tradelead_industries_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<TradeLeadIndustries %s>' % self.code

class TradeLeadAggregationsCountries(CommonColumns):
	__tablename__ = 'trade_lead_aggregations_countries'
	id = db.Column(db.Integer, primary_key=True)
	country = db.Column(db.String(50), unique=False)
	doc_count =  db.Column(db.Integer, unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_lead_results.id", use_alter=True, name='fk_tradelead_country_resultid'), unique=False)
	
	def __init__(self, country, doc_count, result_id):
		self.country = country
		self.doc_count = doc_count
		self.result_id = result_id

	def __repr__(self):
		return '<TradeLeadAggregationsCountries %s>' % self.country
		
class TradeLeadResults(CommonColumns):
	__tablename__ = 'trade_lead_results'
	id = db.Column(db.Integer, primary_key=True)
	id_text = db.Column(db.String(255), unique=False)
	country = db.Column(db.String(255), unique=False)
	specific_location = db.Column(db.String(255), unique=False)
	title = db.Column(db.String(255), unique=False)
	project_number = db.Column(db.String(255), unique=False)
	industry = db.Column(db.String(255), unique=False)
	project_size = db.Column(db.String(255), unique=False)
	description = db.Column(db.Text, unique=False)
	tags = db.Column(db.String(255), unique=False)
	publish_date = db.Column(db.String(255), unique=False)
	end_date = db.Column(db.String(255), unique=False)
	funding_source = db.Column(db.String(255), unique=False)
	borrowing_entity = db.Column(db.String(255), unique=False)
	procurement_organization = db.Column(db.String(255), unique=False)
	contact = db.Column(db.Text, unique=False)
	comments = db.Column(db.Text, unique=False)
	submitting_officer = db.Column(db.String(255), unique=False)
	submitting_officer_contact = db.Column(db.String(255), unique=False)
	url = db.Column(db.String(255), unique=False)
	status = db.Column(db.String(255), unique=False)
	source = db.Column(db.Text, unique=False)
	notice_type = db.Column(db.String(255), unique=False)
	procurement_office = db.Column(db.String(255), unique=False)
	procurement_organization_address = db.Column(db.String(255), unique=False)
	classification_code = db.Column(db.String(255), unique=False)
	procurement_office_address = db.Column(db.String(255), unique=False)
	contract_number = db.Column(db.String(255), unique=False)
	competitive_procurement_strategy = db.Column(db.String(255), unique=False)
	specific_address = db.Column(db.String(255), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)
	lead_source = db.Column(db.Text, unique=False)
	
	categories = db.relationship(TradeLeadCategories, backref=db.backref('trade_lead_categories'))
	aggregations = db.relationship(TradeLeadAggregations, backref=db.backref('trade_lead_aggregations'))
	industries = db.relationship(TradeLeadIndustries, backref=db.backref('trade_lead_industries'))
	countries = db.relationship(TradeLeadAggregationsCountries, backref=db.backref('trade_lead_aggregations_countries'))
	
	def __init__(self,id_text,lead_source,country,specific_location,title,project_number,industry,project_size,description,tags,publish_date,end_date,funding_source,borrowing_entity,procurement_organization,contact,comments,submitting_officer,submitting_officer_contact,url,status,source,notice_type,procurement_office,procurement_organization_address,classification_code,procurement_office_address,contract_number,competitive_procurement_strategy,specific_address,search_performed_at):
		self.id_text = id_text
		self.lead_source = lead_source
		self.country = country
		self.specific_location = specific_location
		self.title = title
		self.project_number = project_number
		self.industry = industry
		self.project_size = project_size
		self.description = description
		self.tags = tags
		self.publish_date = publish_date
		self.end_date = end_date
		self.funding_source = funding_source
		self.borrowing_entity = borrowing_entity
		self.procurement_organization = procurement_organization
		self.contact = contact
		self.comments = comments
		self.submitting_officer = submitting_officer
		self.submitting_officer_contact = submitting_officer_contact
		self.url = url
		self.status = status
		self.source = source
		self.notice_type = notice_type
		self.procurement_office = procurement_office
		self.procurement_organization_address = procurement_organization_address
		self.classification_code = classification_code
		self.procurement_office_address = procurement_office_address
		self.contract_number = contract_number
		self.competitive_procurement_strategy = competitive_procurement_strategy
		self.specific_address = specific_address
		self.search_performed_at = search_performed_at
		

	def __repr__(self):
		return '<TradeLeadResults %s>' % self.id

class TrafficRatesAnnualRate(CommonColumns):
	__tablename__ = 'traffic_annual_rate'
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.String(255), unique=False)
	rate = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("traffic_rate_results.id", use_alter=True, name='fk_trafficrates_annualrate_resultid'), unique=False)
	
	def __init__(self,year,rate,result_id):
		self.year = year
		self.rate = rate
		self.result_id = result_id
	
	def __repr__(self):
		return '<TrafficRatesAnnualRate %s>' % self.id

class TrafficAltAnnualRate(CommonColumns):
	__tablename__ = 'traffic_alt_annual_rate'
	id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.String(255), unique=False)
	rate = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("traffic_rate_results.id", use_alter=True, name='fk_trafficrates_alt_annualrate_resultid'), unique=False)
	
	def __init__(self,year,rate,result_id):
		self.year = year
		self.rate = rate
		self.result_id = result_id
	
	def __repr__(self):
		return '<TrafficAltAnnualRate %s>' % self.id
		
class TrafficRateResults(CommonColumns):
	__tablename__ = 'traffic_rate_results'
	id = db.Column(db.Integer, primary_key=True)
	source_id = db.Column(db.Integer, unique=False)
	tariff_line = db.Column(db.String(255), unique=False)
	subheading_description = db.Column(db.Text, unique=False)
	hs_6 = db.Column(db.String(255), unique=False)
	base_rate = db.Column(db.String(255), unique=False)
	base_rate_alt = db.Column(db.String(255), unique=False)
	final_year = db.Column(db.String(255), unique=False)
	tariff_rate_quota = db.Column(db.String(255), unique=False)
	tariff_rate_quota_note = db.Column(db.String(255), unique=False)
	tariff_eliminated = db.Column(db.String(255), unique=False)
	ag_id = db.Column(db.Integer, unique=False)
	partner_name = db.Column(db.String(255), unique=False)
	reporter_name = db.Column(db.String(255), unique=False)
	staging_basket = db.Column(db.String(255), unique=False)
	partner_start_year = db.Column(db.String(255), unique=False)
	reporter_start_year = db.Column(db.String(255), unique=False)
	partner_agreement_name = db.Column(db.String(255), unique=False)
	reporter_agreement_name = db.Column(db.String(255), unique=False)
	partner_agreement_approved = db.Column(db.String(255), unique=False)
	reporter_agreement_approved = db.Column(db.String(255), unique=False)
	quota_name = db.Column(db.String(255), unique=False)
	rule_text = db.Column(db.String(255), unique=False)
	link_text = db.Column(db.String(255), unique=False)
	link_url = db.Column(db.String(255), unique=False)
	source = db.Column(db.String(255), unique=False)
	search_performed_at =  db.Column(db.String(255), unique=False)
	
	annualrate = db.relationship(TrafficRatesAnnualRate, backref=db.backref('traffic_annual_rate'))
	altannualrate = db.relationship(TrafficAltAnnualRate, backref=db.backref('traffic_alt_annual_rate'))
	
	def __init__(self,source_id, tariff_line, subheading_description, hs_6, base_rate, base_rate_alt, final_year, tariff_rate_quota, tariff_rate_quota_note, tariff_eliminated, ag_id, partner_name, reporter_name, staging_basket, partner_start_year, reporter_start_year, partner_agreement_name, reporter_agreement_name,partner_agreement_approved,reporter_agreement_approved, quota_name, rule_text, link_text, link_url, source, search_performed_at):
		self.source_id = source_id
		self.tariff_line = tariff_line
		self.subheading_description = subheading_description
		self.hs_6 = hs_6
		self.base_rate = base_rate
		self.base_rate_alt = base_rate_alt
		self.final_year = final_year
		self.tariff_rate_quota = tariff_rate_quota
		self.tariff_rate_quota_note = tariff_rate_quota_note
		self.tariff_eliminated = tariff_eliminated
		self.ag_id = ag_id
		self.partner_name = partner_name
		self.reporter_name = reporter_name
		self.staging_basket = staging_basket
		self.partner_start_year = partner_start_year
		self.reporter_start_year = reporter_start_year
		self.partner_agreement_name = partner_agreement_name
		self.reporter_agreement_name = reporter_agreement_name
		self.partner_agreement_approved = partner_agreement_approved
		self.reporter_agreement_approved = reporter_agreement_approved
		self.quota_name = quota_name
		self.rule_text = rule_text
		self.link_text = link_text
		self.link_url = link_url
		self.source = source
		self.search_performed_at = search_performed_at
		
	def __repr__(self):
		return '<TrafficRateResults %s>' % self.id

class TradeItaFaqsIndustries(CommonColumns):
	__tablename__ = 'trade_ita_faq_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_faqs.id", use_alter=True, name='fk_trade_itafaq_industries_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<TradeItaFaqsIndustries %s>' % self.code

class TradeItaFaqsCountries(CommonColumns):
	__tablename__ = 'trade_ita_faq_countries'
	id = db.Column(db.Integer, primary_key=True)
	country = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_faqs.id", use_alter=True, name='fk_trade_itafaq_country_resultid'), unique=False)
	
	def __init__(self, country, result_id):
		self.country = country
		self.result_id = result_id

	def __repr__(self):
		return '<TradeItaFaqsCountries %s>' % self.country

class TradeItaFaqsTopic(CommonColumns):
	__tablename__ = 'trade_ita_zipcode_topic'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_faqs.id", use_alter=True, name='fk_trade_itafaqs_topic_resultid'), unique=False)

	def __init__(self,code, result_id):
		self.code = code
		self.result_id = result_id
	def __repr__(self):
		return '<TradeItaFaqsTopic %s>' % self.id
		
class TradeItaFaqs(CommonColumns):
	__tablename__ = 'trade_ita_faqs'
	id = db.Column(db.Integer, primary_key=True)
	text_id = db.Column(db.String(255), unique=False)
	question = db.Column(db.Text, unique=False)
	answer = db.Column(db.Text, unique=False)
	update_date = db.Column(db.String(255), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)
	
	topics = db.relationship(TradeItaFaqsTopic, backref=db.backref('trade_ita_zipcode_topic'))
	countries = db.relationship(TradeItaFaqsCountries, backref=db.backref('trade_ita_faq_countries'))
	industries = db.relationship(TradeItaFaqsIndustries, backref=db.backref('trade_ita_faq_industries'))

	def __init__(self,text_id, question, answer, update_date, search_performed_at):
		self.text_id = text_id
		self.question = question
		self.answer = answer
		self.update_date = update_date
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaFaqs %s>' % self.id
		
class TradeZipcodeAddress(CommonColumns):
	__tablename__ = 'trade_ita_zipcode_address'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_zipcode_to_post.id", use_alter=True, name='fk_tradezipcode_address_resultid'), unique=False)

	def __init__(self,code, result_id):
		self.code = code
		self.result_id = result_id
	def __repr__(self):
		return '<TradeZipcodeAddress %s>' % self.id
		
class TradeItaZipcodeToPost(CommonColumns):
	__tablename__ = 'trade_ita_zipcode_to_post'
	id = db.Column(db.Integer, primary_key=True)
	id_text = db.Column(db.String(255), unique=False)
	post = db.Column(db.String(255), unique=False)
	office_name = db.Column(db.String(255), unique=False)
	country = db.Column(db.String(255), unique=False)
	state = db.Column(db.String(255), unique=False)
	city = db.Column(db.String(255), unique=False)
	email = db.Column(db.String(255), unique=False)
	fax = db.Column(db.String(255), unique=False)
	mail_instructions = db.Column(db.Text, unique=False)
	phone = db.Column(db.String(255), unique=False)
	post_type = db.Column(db.String(255), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)
	
	addresses = db.relationship(TradeZipcodeAddress, backref=db.backref('trade_ita_zipcode_address'))
	
	def __init__(self,id_text, post, office_name, country, state, city, email, fax, mail_instructions, phone, post_type, search_performed_at):
		self.id_text = id_text
		self.post = post
		self.office_name = office_name
		self.country = country
		self.state = state
		self.city = city
		self.email = email
		self.fax = fax
		self.mail_instructions = mail_instructions
		self.phone = phone
		self.post_type = post_type
		self.search_performed_at = search_performed_at

	def __repr__(self):
		return '<TradeItaZipcodeToPost %s>' % self.id
		
class TradeItaOfficeLocationsAddress(CommonColumns):
	__tablename__ = 'trade_ita_office_locations_address'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_office_locations.id", use_alter=True, name='fk_tradeitaoff_locaddr_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code,result_id,search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaOfficeLocationsAddress %s>' % self.id
		
class TradeItaOfficeLocations(CommonColumns):
	__tablename__ = 'trade_ita_office_locations'
	id = db.Column(db.Integer, primary_key=True)
	id_text = db.Column(db.String(255), unique=False)
	post = db.Column(db.String(255), unique=False)
	office_name = db.Column(db.String(255), unique=False)
	country = db.Column(db.String(255), unique=False)
	state = db.Column(db.String(255), unique=False)
	city = db.Column(db.String(255), unique=False)
	email = db.Column(db.String(255), unique=False)
	fax = db.Column(db.String(255), unique=False)
	mail_instructions = db.Column(db.String(255), unique=False)
	phones = db.Column(db.String(255), unique=False)
	post_type = db.Column(db.String(255), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)
	
	addresses = db.relationship(TradeItaOfficeLocationsAddress, backref=db.backref('trade_ita_office_locations_address'))

	def __init__(self, id_text, post, office_name, country, state, city, email, fax, mail_instructions, phone, post_type, search_performed_at):
		self.id_text = id_text
		self.post = post
		self.office_name = office_name
		self.country = country
		self.state = state
		self.city = city
		self.email = email
		self.fax = fax
		self.mail_instructions = mail_instructions
		self.phone = phone
		self.post_type = post_type
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaOfficeLocations %s>' % self.id

class TradeItaArticlesTradePrograms(CommonColumns):
	__tablename__ = 'trade_ita_articles_programs'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_tradeprogram_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesTradePrograms %s>' % self.id

class TradeItaTradeArticlesAgencies(CommonColumns):
	__tablename__ = 'trade_ita_articles_agencies'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_artagen_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaTradeArticlesAgencies %s>' % self.id

class ItaTradeArticlesIndustries(CommonColumns):
	__tablename__ = 'trade_ita_articles_industries'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_trade_articles_industries_resultid'), unique=False)
	
	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<ItaTradeArticlesIndustries %s>' % self.code

class ItaTradeArticlesCountries(CommonColumns):
	__tablename__ = 'trade_ita_articles_countries'
	id = db.Column(db.Integer, primary_key=True)
	country = db.Column(db.String(50), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_trade_articles_countries_resultid'), unique=False)

	def __init__(self, country, result_id):
		self.country = country
		self.result_id = result_id
		
	def __repr__(self):
		return '<ItaTradeArticlesCountries %s>' % self.country

class TradeItaTradeArticlesSourcesBusinessUnits(CommonColumns):
	__tablename__ = 'trade_ita_articles_source_bi_units'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_artagen_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaTradeArticlesSourcesBusinessUnits %s>' % self.id

class TradeItaTradeArticlesSourceOffices(CommonColumns):
	__tablename__ = 'trade_ita_articles_source_offices'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_sourceoffice_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaTradeArticlesSourceOffices %s>' % self.id
		
class TradeItaTradeArticlesExportPhases(CommonColumns):
	__tablename__ = 'trade_ita_articles_export_phases'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_expphases_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaTradeArticlesExportPhases %s>' % self.id

class TradeItaArticlesTopics(CommonColumns):
	__tablename__ = 'trade_ita_articles_topics'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_top_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesTopics %s>' % self.id

class TradeItaArticlesSubTopics(CommonColumns):
	__tablename__ = 'trade_ita_articles_subtopics'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_subtop_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesSubTopics %s>' % self.id

class TradeItaArticlesGeoRegions(CommonColumns):
	__tablename__ = 'trade_ita_articles_georegions'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_georeg_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesGeoRegions %s>' % self.id
		
class TradeItaArticlesGeoSubRegions(CommonColumns):
	__tablename__ = 'trade_ita_articles_geosubregions'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_geosubreg_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesGeoSubRegions %s>' % self.id
		
class TradeItaArticlesTradeRegions(CommonColumns):
	__tablename__ = 'trade_ita_articles_regions'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_tradereg_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesTradeRegions %s>' % self.id
		
class TradeItaArticlesTradeInitiatives(CommonColumns):
	__tablename__ = 'trade_ita_articles_init'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_init_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesTradeInitiatives %s>' % self.id
		
class TradeItaArticlesFileUrl(CommonColumns):
	__tablename__ = 'trade_ita_articles_file_url'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_fileurl_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesFileUrl %s>' % self.id
		
class TradeItaArticlesImageUrl(CommonColumns):
	__tablename__ = 'trade_ita_articles_img_url'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_imgurl_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesImageUrl %s>' % self.id

class TradeItaArticlesUrlHtmlSource(CommonColumns):
	__tablename__ = 'trade_ita_articles_url_html_source'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_urlhtml_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesUrlHtmlSource %s>' % self.id

class TradeItaArticlesUrlXmlSource(CommonColumns):
	__tablename__ = 'trade_ita_articles_url_xml_source'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_ita_articles.id", use_alter=True, name='fk_tradeita_xmlurl_resultid'), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)

	def __init__(self, code, result_id, search_performed_at):
		self.code = code
		self.result_id = result_id
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaArticlesUrlXmlSource %s>' % self.id

		
class TradeItaTradeArticles(CommonColumns):
	__tablename__ = 'trade_ita_articles'
	id = db.Column(db.Integer, primary_key=True)
	id_text = db.Column(db.String(255), unique=False)
	title = db.Column(db.Text, unique=False)
	short_title = db.Column(db.Text, unique=False)
	summary = db.Column(db.Text, unique=False)
	creation_date = db.Column(db.String(255), unique=False)
	release_date = db.Column(db.String(255), unique=False)
	expiration_date = db.Column(db.String(255), unique=False)
	evergreen = db.Column(db.String(255), unique=False)
	content = db.Column(db.Text, unique=False)
	keyword = db.Column(db.String(255), unique=False)
	seo_metadata_title = db.Column(db.Text, unique=False)
	seo_metadata_description = db.Column(db.Text, unique=False)
	seo_metadata_keyword = db.Column(db.Text, unique=False)
	trade_url = db.Column(db.String(255), unique=False)
	search_performed_at = db.Column(db.String(255), unique=False)
	
	programs = db.relationship(TradeItaArticlesTradePrograms, backref=db.backref('trade_ita_articles_programs'))
	agencies = db.relationship(TradeItaTradeArticlesAgencies, backref=db.backref('trade_ita_articles_agencies'))
	industries = db.relationship(ItaTradeArticlesIndustries, backref=db.backref('trade_ita_articles_industries'))
	countries = db.relationship(ItaTradeArticlesCountries, backref=db.backref('trade_ita_articles_countries'))
	business = db.relationship(TradeItaTradeArticlesSourcesBusinessUnits, backref=db.backref('trade_ita_articles_source_bi_units'))
	offices = db.relationship(TradeItaTradeArticlesSourceOffices, backref=db.backref('trade_ita_articles_source_bi_units'))
	export_phases = db.relationship(TradeItaTradeArticlesExportPhases, backref=db.backref('trade_ita_articles_export_phases'))
	topics = db.relationship(TradeItaArticlesTopics, backref=db.backref('trade_ita_articles_topics'))
	subtopics = db.relationship(TradeItaArticlesSubTopics, backref=db.backref('trade_ita_articles_subtopics'))
	georegions = db.relationship(TradeItaArticlesGeoRegions, backref=db.backref('trade_ita_articles_georegions'))
	geosubregions = db.relationship(TradeItaArticlesGeoSubRegions, backref=db.backref('trade_ita_articles_geosubregions'))
	regions = db.relationship(TradeItaArticlesTradeRegions, backref=db.backref('trade_ita_articles_regions'))
	initiatives = db.relationship(TradeItaArticlesTradeInitiatives, backref=db.backref('trade_ita_articles_init'))
	fileurl = db.relationship(TradeItaArticlesFileUrl, backref=db.backref('trade_ita_articles_file_url'))
	imageurl = db.relationship(TradeItaArticlesImageUrl, backref=db.backref('trade_ita_articles_img_url'))
	urlhtmlsource = db.relationship(TradeItaArticlesUrlHtmlSource, backref=db.backref('trade_ita_articles_url_html_source'))
	urlxmlsource = db.relationship(TradeItaArticlesUrlXmlSource, backref=db.backref('trade_ita_articles_url_xml_source'))

	def __init__(self, id_text, title, short_title, summary, creation_date, release_date, expiration_date, evergreen, content, keyword, seo_metadata_title, seo_metadata_description, seo_metadata_keyword, trade_url, search_performed_at):
		self.id_text = id_text
		self.title = title
		self.short_title = short_title
		self.summary = summary
		self.creation_date = creation_date
		self.release_date = release_date
		self.expiration_date = expiration_date
		self.evergreen = evergreen
		self.content = content
		self.keyword = keyword
		self.seo_metadata_title = seo_metadata_title
		self.seo_metadata_description = seo_metadata_description
		self.seo_metadata_keyword = seo_metadata_keyword
		self.trade_url = trade_url
		self.search_performed_at = search_performed_at
	def __repr__(self):
		return '<TradeItaTradeArticles %s>' % self.id	

class TradeBusinessServiceProviders(CommonColumns):
	__tablename__ = 'trade_bi_service_providers'
	id = db.Column(db.Integer, primary_key=True)
	ita_contact_email = db.Column(db.String(255), unique=False)
	company_name = db.Column(db.String(255), unique=False)
	company_phone = db.Column(db.String(255), unique=False)
	company_address = db.Column(db.String(255), unique=False)
	company_website = db.Column(db.String(255), unique=False)
	company_description = db.Column(db.Text, unique=False)
	company_email = db.Column(db.String(255), unique=False)
	ita_office = db.Column(db.String(255), unique=False)
	contact_title = db.Column(db.String(255), unique=False)
	contact_name = db.Column(db.String(255), unique=False)
	category = db.Column(db.String(255), unique=False)
	
	def __init__(self, ita_contact_email, company_name, company_phone, company_address, company_website, company_description, company_email, ita_office, contact_title, contact_name, category):
		self.ita_contact_email = ita_contact_email
		self.company_name = company_name
		self.company_phone = company_phone
		self.company_address = company_address
		self.company_website = company_website
		self.company_description = company_description
		self.company_email = company_email
		self.ita_office = ita_office
		self.contact_title = contact_title
		self.contact_name = contact_name
		self.category = category
		
	def __repr__(self):
		return '<TradeBusinessServiceProviders %s>' % self.id

class TradeTaxonomyTaxonomies(CommonColumns):
	__tablename__ = 'trade_tax_taxonomies'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_tax_results.id", use_alter=True, name='fk_tradetax_resultid'), unique=False)

	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<TradeTaxonomyTaxonomies %s>' % self.id

class TradeTaxonomyBroaderTerms(CommonColumns):
	__tablename__ = 'trade_tax_broader_terms'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_tax_results.id", use_alter=True, name='fk_tradetax_broad_resultid'), unique=False)

	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<TradeTaxonomyBroaderTerms %s>' % self.id

class TradeTaxonomyNarrowTerms(CommonColumns):
	__tablename__ = 'trade_tax_narrow_terms'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(255), unique=False)
	result_id = db.Column(db.Integer, ForeignKey("trade_tax_results.id", use_alter=True, name='fk_tradetax_narr_resultid'), unique=False)

	def __init__(self, code, result_id):
		self.code = code
		self.result_id = result_id

	def __repr__(self):
		return '<TradeTaxonomyNarrowTerms %s>' % self.id
		
class TradeTaxonomiesResults(CommonColumns):
	__tablename__ = 'trade_tax_results'
	id = db.Column(db.Integer, primary_key=True)
	text_id = db.Column(db.String(255), unique=False)
	name = db.Column(db.String(255), unique=False)
	path = db.Column(db.String(255), unique=False)
	
	taxonomies = db.relationship(TradeTaxonomyTaxonomies, backref=db.backref('trade_tax_taxonomies'))
	broaderterms = db.relationship(TradeTaxonomyBroaderTerms, backref=db.backref('trade_tax_broader_terms'))
	narrowterms = db.relationship(TradeTaxonomyNarrowTerms, backref=db.backref('trade_tax_narrow_terms'))
	
	def __init__(self, text_id, name, path):
		self.text_id = text_id
		self.name = name
		self.path = path

	def __repr__(self):
		return '<TradeTaxonomiesResults %s>' % self.id

class TradeMinimisResults(CommonColumns):
	__tablename__ = 'trade_minimis_results'
	id = db.Column(db.Integer, primary_key=True)
	country_name = db.Column(db.String(255), unique=False)
	country = db.Column(db.String(255), unique=False)
	de_minimis_value = db.Column(db.Integer, unique=False)
	de_minimis_currency = db.Column(db.String(255), unique=False)
	vat_amount = db.Column(db.Integer, unique=False)
	vat_currency = db.Column(db.String(255), unique=False)
	notes = db.Column(db.String(255), unique=False)

	def __init__(self, country_name, country, de_minimis_value, de_minimis_currency, vat_amount, vat_currency, notes):
		self.country_name = country_name
		self.country = country
		self.de_minimis_value = de_minimis_value
		self.de_minimis_currency = de_minimis_currency
		self.vat_amount = vat_amount
		self.vat_currency = vat_currency
		self.notes = notes

	def __repr__(self):
		return '<TradeMinimisResults %s>' % self.id
		
if __name__ == '__main__':
    app.run()