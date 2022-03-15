import os
import sqlite3
import urllib
import urllib2
import json
import time
import requests
import ssl
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from StringIO import StringIO
from trade_models import db, Base
from sqlalchemy import create_engine

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/tmp/app.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://twisted-dragon.cu3ugwf8wzsx.us-west-2.rds.amazonaws.com:5432/twisted'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://argentina:mountains@twisted-dragon.cu3ugwf8wzsx.us-west-2.rds.amazonaws.com:5432/twisted'

from trade_models import User, Sources, MarketResearchLibraryResults, Countries, Industries, ItaIndustries, ConsolidatedScreenListAddresses, ConsolidatedScreenListResults, TradeEventsResults, TradeEventVenues, TradeEventContacts, TradeEventAggregations, TradeLeadResults, TradeLeadCategories, TradeLeadAggregations, TrafficRateResults, TrafficRatesAnnualRate, TrafficAltAnnualRate, TradeItaFaqs, TradeItaFaqsTopic, TradeItaOfficeLocations, TradeItaOfficeLocationsAddress, TradeItaTradeArticles, TradeItaTradeArticlesAgencies, TradeItaTradeArticlesSourcesBusinessUnits, TradeItaTradeArticlesSourceOffices, TradeItaTradeArticlesExportPhases, TradeItaArticlesTopics, TradeItaArticlesSubTopics, TradeItaArticlesGeoRegions, TradeItaArticlesGeoSubRegions, TradeItaArticlesTradeRegions, TradeItaArticlesTradePrograms, TradeItaArticlesTradeInitiatives, TradeItaArticlesFileUrl, TradeItaArticlesImageUrl, TradeItaArticlesUrlHtmlSource, TradeItaArticlesUrlXmlSource, TradeBusinessServiceProviders, TradeTaxonomiesResults,TradeTaxonomyTaxonomies,TradeTaxonomyBroaderTerms,TradeTaxonomyNarrowTerms, TradeMinimisResults, TradeItaZipcodeToPost, TradeZipcodeAddress, MarketResearchLibraryIndustries, MarketResearchLibraryItaIndustries, MarketResearchLibraryCountries, TradeEventAggregationsCountries, TradeEventIndustries, TradeLeadAggregationsCountries, TradeLeadIndustries, TradeItaFaqsCountries, TradeItaFaqsIndustries, ItaTradeArticlesIndustries, ItaTradeArticlesCountries

#db.drop_all()
db.Model = Base
db.create_all()

@app.route('/market_research_li')
def add_market_research_library():
	url = 'https://api.trade.gov/market_research_library/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))
	print data
	
	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		try:
			sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
			db.session.add(sources)
			db.session.commit()
			flash('New sources_used entry was successfully posted')
		except Exception: 
			pass
	
	for item in data["results"]:
		queryString  = urllib.quote_plus(item["url"])
		try:
			results = MarketResearchLibraryResults(item["id"], search_performed_at, item["description"], item["title"], queryString, item["report_type"], item["expiration_date"])
			db.session.add(results)
			db.session.commit()
			flash('New market_research_library_results entry was successfully posted')
		except Exception: 
			pass
	
		for itemm in item["countries"]:
			try:
				countries = MarketResearchLibraryCountries(itemm,item["id"])
				db.session.add(countries)
				db.session.commit()
				flash('New countries entry was successfully posted')
			except Exception: 
				pass
			
		for item2 in item["industries"]:
			try:
				industries = MarketResearchLibraryIndustries(item2,item["id"])
				db.session.add(industries)
				db.session.commit()
				flash('New industries entry was successfully posted')
			except Exception: 
				pass
			
		for item3 in item["ita_industries"]:
			try:
				ita_industries = MarketResearchLibraryItaIndustries(item2,item["id"])
				db.session.add(ita_industries)
				db.session.commit()
				flash('New ita_industries entry was successfully posted')
			except Exception: 
				pass
			
	return "executed"

@app.route('/trade_events')
def add_trade_events():
	url = 'https://api.trade.gov/trade_events/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources_used entry was successfully posted')
		
	for item_res in data["results"]: 
		if 'event_name' in item_res.keys():
			event_name = item_res["event_name"]
		else:
			event_name = ""
			
		if 'event_type' in item_res.keys():
			event_type = item_res["event_type"]
		else:
			event_type = ""
			
		if 'start_date' in item_res.keys():
			start_date = item_res["start_date"]
		else:
			start_date = ""
			
		if  'start_time' in item_res.keys():
			start_time = item_res["start_time"]
		else:
			start_time = ""
			
		if  'end_date' in item_res.keys():   
			end_date = item_res["end_date"]
		else:
			end_date = ""
			
		if 'end_time' in item_res.keys():
			end_time = item_res["end_time"]
		else:
			end_time = ""
		
		if 'time_zone' in item_res.keys():
			time_zone = item_res["time_zone"]
		else:
			time_zone = ""
		
		if 'cost' in item_res.keys():
			cost = item_res["cost"]
		else:
			cost = ""
			
		if 'registration_link' in item_res.keys():
			registration_link = item_res["registration_link"]
			if registration_link is None:
				registration_link = ""
		else:
			registration_link = ""
			
		if 'registration_title' in item_res.keys():
			registration_title = item_res["registration_title"]
			if registration_title is None:
				registration_title = ""
		else:
			registration_title = ""
			
		if 'description' in item_res.keys():
			description = item_res["description"]
		else:
			description = ""
			
		if 'url' in item_res.keys():
			url = item_res["url"]
			if url is None:
				url = ""
		else:
			url = ""
		
		results = TradeEventsResults(event_name,event_type,start_date,start_time,end_date,end_time,time_zone,cost,registration_link,registration_title,description,url)
		db.session.add(results)
		db.session.commit()
		flash('New sources_used entry was successfully posted')
		twid = db.session.query(TradeEventsResults).order_by(TradeEventsResults.id.desc()).first()
		result_id = twid.id

		for item_venues in item_res["venues"]:
			if 'address' in item_venues.keys():
				address = item_venues["address"]
				if address is None:
					address = ""
			else:
				address = ""
				
			if 'city' in item_venues.keys():
				city = item_venues["city"]
				if city is None:
					city = ""
			else:
				city = ""
				
			if 'country' in item_venues.keys():
				country = item_venues["country"]
				if country is None:
					country = ""				
			else:
				country = ""
				
			if 'state' in item_venues.keys():
				state = item_venues["state"]
				if state is None:
					state = ""
			else:
				state = ""
				
			if 'venue' in item_venues.keys():
				venue = item_venues["venue"]
				if venue is None:
					venue = ""
			else:
				venue = ""
		
			trade_events_venues = TradeEventVenues(city,country,state,venue,result_id,address)
			db.session.add(trade_events_venues)
			db.session.commit()
			flash('New sources_used entry was successfully posted')
		
		if 'contacts' in item_res.keys():
			for item_contacts in item_res["contacts"]:
				if 'email' in item_contacts.keys():
					email = item_contacts["email"]
					if email is None:
						email = ""
				else:
					email = ""
					
				if 'first_name' in item_contacts.keys():
					first_name = item_contacts["first_name"]
					if first_name is None:
						first_name = ""
				else:
					first_name = ""
					
				if 'last_name' in item_contacts.keys(): 
					last_name = item_contacts["last_name"]
					if last_name is None:
						last_name = ""
				else:
					last_name = ""
					
				if 'person_title' in item_contacts.keys():
					person_title = item_contacts["person_title"]
					if person_title is None:
						person_title = ""
				else:
					person_title = ""
					
				if 'phone' in item_contacts.keys():
					phone = item_contacts["phone"]
					if phone is None:
						phone = ""
				else:
					phone = ""
					
				if 'post' in item_contacts.keys():
					post = item_contacts["post"]
					if post is None:
						post = ""
				else:
					post = ""
					
				result_id = twid.id
				trade_events_contacts = TradeEventContacts(email,first_name,last_name,person_title,phone,post,result_id)
				db.session.add(trade_events_contacts)
				db.session.commit()
				flash('New sources_used entry was successfully posted')
	   
		if 'industries' in item_res.keys():
			for item_industries in item_res["industries"]:
				code = item_industries
				result_id = twid.id
				industries = TradeEventIndustries(code,result_id)
				db.session.add(industries)
				db.session.commit()
				flash('New sources_used entry was successfully posted')
		
		
	for item_aggregations in data["aggregations"]["sources"]:
		itm_key = item_aggregations["key"]
		itm_doc_count= item_aggregations["doc_count"]
		result_id = twid.id
		trade_events_aggregations = TradeEventAggregations(itm_doc_count,result_id,itm_key)
		db.session.add(trade_events_aggregations)
		db.session.commit()
		flash('New sources_used entry was successfully posted')

	for item_aggregations2 in data["aggregations"]["countries"]:
		itm_key2 = item_aggregations2["key"]
		itm_doc_count2 = item_aggregations2["doc_count"]
		result_id = twid.id
		countries = TradeEventAggregationsCountries(itm_key2,itm_doc_count2,result_id)
		db.session.add(countries)
		db.session.commit()
		flash('New sources_used entry was successfully posted')
		
	return "executed"

@app.route('/trade_leads')
def add_trade_leads():
	url = 'https://api.trade.gov/trade_leads/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')

	for item_res in data["results"]: 
		if 'id' in item_res.keys():
			id_text = item_res["id"]
			if id_text is None:
				id_text = ""
		else:
			id_text = ""
			
		if 'lead_source' in item_res.keys():
			lead_source = item_res["lead_source"]
			if lead_source is None:
				lead_source = ""
		else:
			lead_source = ""
			
		if 'country' in item_res.keys():
			country = item_res["country"]
			if country is None:
				country = ""
		else:
			country = ""
			
		if 'specific_location' in item_res.keys():
			specific_location = item_res["specific_location"]
			if specific_location is None:
				specific_location = ""
		else:
			specific_location = ""
			
		if 'title' in item_res.keys():
			title = item_res["title"]
			if title is None:
				title = ""
		else:
			title = ""
			
		if 'project_number' in item_res.keys():
			project_number = item_res["project_number"]
			if project_number is None:
				project_number = ""
		else:
			project_number = ""
		
		if 'industry' is item_res.keys():
			industry = item_res["industry"]
			if industry is None:
				industry = ""
		else:
			industry = ""
			
		if 'ita_industries' in item_res.keys():
			ita_industries = item_res["ita_industries"]
			if ita_industries is None:
				ita_industries = ""
		else:
			ita_industries = ""
		
		if 'project_size' in item_res.keys():
			project_size = item_res["project_size"]
			if project_size is None:
				project_size = ""
		else:
			project_size = ""
		
		if 'description' in item_res.keys():
			description = item_res["description"]
			if description is None:
				description = ""
		else:
			description = ""
		
		if 'tags' in item_res.keys():
			tags = item_res["tags"]
			if tags is None:
				tags = ""
		else:
			tags = ""
		
		if 'publish_date' in item_res.keys():
			publish_date = item_res["publish_date"]
			if publish_date is None:
				publish_date = ""
		else:
			publish_date = ""
		
		if 'end_date' in item_res.keys():
			end_date = item_res["end_date"]
			if end_date is None:
				end_date = ""
		else:
			end_date = ""
		
		if 'funding_source' in item_res.keys():
			funding_source = item_res["funding_source"]
			if funding_source is None:
				funding_source = ""
		else:
			funding_source = ""
		
		if 'borrowing_entity' in item_res.keys():
			borrowing_entity = item_res["borrowing_entity"]
			if borrowing_entity is None:
				borrowing_entity = ""
		else:
			borrowing_entity = ""
		
		if 'procurement_organization' in item_res.keys():
			procurement_organization = item_res["procurement_organization"]
			if procurement_organization is None:
				procurement_organization = ""
		else:
			procurement_organization = ""
		
		if 'contact' in item_res.keys():
			contact = item_res["contact"]
			if contact is None:
				contact = ""
		else:
			contact = ""
		
		if 'comments' in item_res.keys():
			comments = item_res["comments"]
			if comments is None:
				comments = ""
		else:
			comments = ""
		
		if 'submitting_officer' in item_res.keys():
			submitting_officer = item_res["submitting_officer"]
			if submitting_officer is None:
				submitting_officer = ""
		else:
			comments = ""
		
		if 'submitting_officer_contact' in item_res.keys():
			submitting_officer_contact = item_res["submitting_officer_contact"]
			if submitting_officer_contact is None:
				submitting_officer_contact = ""
		else:
			comments = ""
		
		if 'url' in item_res.keys():
			url = item_res["url"]
			if url is None:
				url = ""
		else:
			url = ""
		
		if 'status' in item_res.keys():
			status = item_res["status"]
			if status is None:
				status = ""
		else:
			url = ""
		
		if 'source' in item_res.keys():
			source = item_res["source"]
			if source is None:
				source = ""
		else:
			source = ""
		
		if 'notice_type' in item_res.keys():
			notice_type = item_res["notice_type"]
			if notice_type is None:
				notice_type = ""
		else:
			notice_type = ""
		
		if 'procurement_office' in item_res.keys():
			procurement_office = item_res["procurement_office"]
			if procurement_office is None:
				procurement_office = ""
		else:
			procurement_office = ""
		
		if 'procurement_organization_address' in item_res.keys():
			procurement_organization_address = item_res["procurement_organization_address"]
			if procurement_organization_address is None:
				procurement_organization_address = ""
		else:
			procurement_organization_address = ""
		
		if 'classification_code' in item_res.keys():
			classification_code = item_res["classification_code"]
			if classification_code is None:
				classification_code = ""
		else:
			classification_code = ""
			
		if 'procurement_office_address' in item_res.keys():
			procurement_office_address = item_res["procurement_office_address"]
			if procurement_office_address is None:
				procurement_office_address = ""
		else:
			procurement_office_address = ""
			
		if 'contract_number' in item_res.keys():
			contract_number = item_res["contract_number"]
			if contract_number is None:
				contract_number = ""
		else:
			contract_number = ""
			
		if 'competitive_procurement_strategy' in item_res.keys():
			competitive_procurement_strategy = item_res["competitive_procurement_strategy"]
			if competitive_procurement_strategy is None:
				competitive_procurement_strategy = ""
		else:
			competitive_procurement_strategy = ""

		if 'specific_address' in item_res.keys():
			specific_address = item_res["specific_address"]
			if specific_address is None:
				specific_address = ""
		else:
			specific_address = ""
			
		trade_leads_results = TradeLeadResults(id_text, lead_source, country, specific_location, title, project_number, industry, project_size, description, tags, publish_date, end_date, funding_source, borrowing_entity, procurement_organization, contact, comments, submitting_officer, submitting_officer_contact, url, status, source, notice_type, procurement_office, procurement_organization_address, classification_code, procurement_office_address, contract_number, competitive_procurement_strategy, specific_address, search_performed_at)
		db.session.add(trade_leads_results)
		db.session.commit()
		flash('New trade_leads_results entry was successfully posted')
		twid = db.session.query(TradeLeadResults).order_by(TradeLeadResults.id.desc()).first()
		
		if 'categories' in item_res.keys():
			
			for code in item_res["categories"]: 
				result_id = twid.id
				trade_leads_categories = TradeLeadCategories(code,result_id)
				db.session.add(trade_leads_categories)
				db.session.commit()
				flash('New trade_leads_results entry was successfully posted')
				
		"""
		for item_ita_industries in item_res["ita_industries"]:
			if 'code' in item_ita_industries.keys():
				code = item_ita_industries["code"]
			else:
				code = ""
			result_id = twid.id
			industries = TradeLeadIndustries(code, result_id)
			db.session.add(industries)
			db.session.commit()
			flash('New industries entry was successfully posted')			
		"""
	for item_aggregations in data["aggregations"]["sources"]:
		itm_key = item_aggregations["key"]
		itm_doc_count= item_aggregations["doc_count"]
		result_id = twid.id
		trade_leads_aggregations = TradeLeadAggregations(itm_doc_count,result_id,itm_key)
		db.session.add(trade_leads_aggregations)
		db.session.commit()
		flash('New trade_leads_aggregations entry was successfully posted')

	for item_aggregations2 in data["aggregations"]["countries"]:
		itm_key2 = item_aggregations2["key"]
		itm_doc_count2 = item_aggregations2["doc_count"]
		result_id = twid.id
		countries = TradeLeadAggregationsCountries(itm_key2,itm_doc_count2,result_id)
		db.session.add(countries)
		db.session.commit()
		flash('New countries entry was successfully posted')
	
	return "executed"
	
@app.route('/tariff_rates')
def add_tariff_rates():
	url = 'https://api.trade.gov/tariff_rates/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')

	for item_res in data["results"]: 
		if 'source_id' in item_res.keys():
			source_id = item_res["source_id"]
			if source_id is None:
				source_id = 0
		else:
			source_id = 0
		
		if 'tariff_line' in item_res.keys():
			tariff_line = item_res["tariff_line"]
			if tariff_line is None:
				tariff_line = ""
		else:
			tariff_line = ""
		
		if 'subheading_description' in item_res.keys():
			subheading_description = item_res["subheading_description"]
			if subheading_description is None:
				subheading_description = ""
		else:
			subheading_description = ""
		
		if 'hs_6' in item_res.keys():
			hs_6 = item_res["hs_6"]
			if hs_6 is None:
				hs_6 = ""
		else:
			hs_6 = ""

		if 'base_rate' in item_res.keys():
			base_rate = item_res["base_rate"]
			if base_rate is None:
				base_rate = ""
		else:
			base_rate = ""
			
		if 'base_rate_alt' in item_res.keys():
			base_rate_alt = item_res["base_rate_alt"]
			if base_rate_alt is None:
				base_rate_alt = ""
		else:
			base_rate_alt = ""
		
		if 'final_year' is item_res.keys():
			final_year = item_res["final_year"]
			if final_year is None:
				final_year = ""
		else:
			final_year = ""
			
		if 'tariff_rate_quota' in item_res.keys():
			tariff_rate_quota = item_res["tariff_rate_quota"]
			if tariff_rate_quota is None:
				tariff_rate_quota = ""
		else:
			tariff_rate_quota = ""
		
		if 'tariff_rate_quota_note' in item_res.keys():
			tariff_rate_quota_note = item_res["tariff_rate_quota_note"]
			if tariff_rate_quota_note is None:
				tariff_rate_quota_note = ""
		else:
			tariff_rate_quota_note = ""
		
		if 'tariff_eliminated' in item_res.keys():
			tariff_eliminated = item_res["tariff_eliminated"]
			if tariff_eliminated is None:
				tariff_eliminated = ""
		else:
			tariff_eliminated = ""
		
		if 'ag_id' in item_res.keys():
			ag_id = item_res["ag_id"]
			if ag_id is None:
				ag_id = 0
		else:
			ag_id = 0
		
		if 'partner_name' in item_res.keys():
			partner_name = item_res["partner_name"]
			if partner_name is None:
				partner_name = ""
		else:
			partner_name = ""
		
		if 'reporter_name' in item_res.keys():
			reporter_name = item_res["reporter_name"]
			if reporter_name is None:
				reporter_name = ""
		else:
			reporter_name = ""
		
		if 'staging_basket' in item_res.keys():
			staging_basket = item_res["staging_basket"]
			if staging_basket is None:
				staging_basket = ""
		else:
			staging_basket = ""
		
		if 'partner_start_year' in item_res.keys():
			partner_start_year = item_res["partner_start_year"]
			if partner_start_year is None:
				partner_start_year = ""
		else:
			partner_start_year = ""
		
		if 'reporter_start_year' in item_res.keys():
			reporter_start_year = item_res["reporter_start_year"]
			if reporter_start_year is None:
				reporter_start_year = ""
		else:
			reporter_start_year = ""
		
		if 'partner_agreement_name' in item_res.keys():
			partner_agreement_name = item_res["partner_agreement_name"]
			if partner_agreement_name is None:
				partner_agreement_name = ""
		else:
			partner_agreement_name = ""
		
		if 'reporter_agreement_name' in item_res.keys():
			reporter_agreement_name = item_res["reporter_agreement_name"]
			if reporter_agreement_name is None:
				reporter_agreement_name = ""
		else:
			reporter_agreement_name = ""
		
		if 'partner_agreement_approved' in item_res.keys():
			partner_agreement_approved = item_res["partner_agreement_approved"]
			if partner_agreement_approved is None:
				partner_agreement_approved = ""
		else:
			partner_agreement_approved = ""
		
		if 'reporter_agreement_approved' in item_res.keys():
			reporter_agreement_approved = item_res["reporter_agreement_approved"]
			if reporter_agreement_approved is None:
				reporter_agreement_approved = ""
		else:
			reporter_agreement_approved = ""
		
		if 'quota_name' in item_res.keys():
			quota_name = item_res["quota_name"]
			if quota_name is None:
				quota_name = ""
		else:
			quota_name = ""
		
		if 'rule_text' in item_res.keys():
			rule_text = item_res["rule_text"]
			if rule_text is None:
				rule_text = ""
		else:
			rule_text = ""
		
		if 'link_text' in item_res.keys():
			link_text = item_res["link_text"]
			if link_text is None:
				link_text = ""
		else:
			link_text = ""
		
		if 'link_url' in item_res.keys():
			link_url = item_res["link_url"]
			if link_url is None:
				link_url = ""
		else:
			link_url = ""
		
		if 'source' in item_res.keys():
			source = item_res["source"]
			if source is None:
				source = ""
		else:
			source = ""

		trade_traffic_rate = TrafficRateResults(source_id, tariff_line, subheading_description, hs_6, base_rate, base_rate_alt, final_year, tariff_rate_quota, tariff_rate_quota_note, tariff_eliminated, ag_id, partner_name, reporter_name, staging_basket, partner_start_year, reporter_start_year, partner_agreement_name, reporter_agreement_name,partner_agreement_approved,reporter_agreement_approved, quota_name, rule_text, link_text, link_url, source, search_performed_at)
		db.session.add(trade_traffic_rate)
		db.session.commit()
		flash('New trade_traffic_rate entry was successfully posted')
		twid = db.session.query(TrafficRateResults).order_by(TrafficRateResults.id.desc()).first()
		result_id = twid.id
		
		if 'annual_rates' in item_res.keys():
			
			for code in item_res["annual_rates"]:
				year = code[0]
				rate = code[1]
				trade_traffic_rates_annual_rates = TrafficRatesAnnualRate(year,rate,result_id)
				db.session.add(trade_traffic_rates_annual_rates)
				db.session.commit()
				flash('New trade_traffic_rates_annual_rates entry was successfully posted')
				
		if 'alt_annual_rates' in item_res.keys():
			for code in item_res["annual_rates"]:
				year = code[0]
				rate = code[1]
				trade_alt_annual_rates = TrafficAltAnnualRate(year,rate,result_id)
				db.session.add(trade_alt_annual_rates)
				db.session.commit()
				flash('New trade_alt_annual_rates entry was successfully posted')
	
	return "executed"

	
@app.route('/ita_faqs')
def add_ita_faqs():
	url = 'https://api.trade.gov/ita_faqs/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')
		
	for item_res in data["results"]: 	
		if 'id' in item_res.keys():
			text_id = item_res["id"]
			if text_id is None:
				text_id = ""
		else:
			text_id = ""

		if 'question' in item_res.keys():
			question = item_res["question"]
			if question is None:
				question = ""
		else:
			question = ""
			
		if 'answer' in item_res.keys():
			answer = item_res["answer"]
			if answer is None:
				answer = ""
		else:
			answer = ""
		
		if 'update_date' in item_res.keys():
			update_date = item_res["update_date"]
			if update_date is None:
				update_date = ""
		else:
			update_date = ""
				
		trade_ita_faqs = TradeItaFaqs(text_id, question, answer, update_date, search_performed_at)
		db.session.add(trade_ita_faqs)
		db.session.commit()
		flash('New trade_ita_faqs entry was successfully posted')
		twid = db.session.query(TradeItaFaqs).order_by(TradeItaFaqs.id.desc()).first()
		result_id = twid.id
		
		if 'industry' in item_res.keys():
			for code in item_res["industry"]:
				trade_ita_faqs_industries = TradeItaFaqsIndustries(code,result_id)
				db.session.add(trade_ita_faqs_industries)
				db.session.commit()
				flash('New trade_ita_faqs_industries entry was successfully posted')
		
		if 'topic' in item_res.keys():
			for code in item_res["topic"]:
				trade_ita_faqs_topic = TradeItaFaqsTopic(code,result_id)
				db.session.add(trade_ita_faqs_topic)
				db.session.commit()
				flash('New trade_ita_faqs_topic entry was successfully posted')
		
		if 'country' in item_res.keys():
			for code in item_res["country"]:
				print code
				trade_ita_faqs_countries = TradeItaFaqsCountries(code, result_id)
				db.session.add(trade_ita_faqs_countries)
				db.session.commit()
				flash('New trade_ita_faqs_countries entry was successfully posted')
	
	return "executed"
	
@app.route('/ita_office_locations')
def add_ita_office_locations():
	url = 'https://api.trade.gov/ita_office_locations/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')
		
	for item_res in data["results"]: 	
		if 'id' in item_res.keys():
			id_text = item_res["id"]
			if id_text is None:
				id_text = ""
		else:
			id_text = ""
			
		if 'post' in item_res.keys():
			post = item_res["post"]
			if post is None:
				post = ""
		else:
			post = ""
			
		if 'office_name' in item_res.keys():
			office_name = item_res["office_name"]
			if office_name is None:
				office_name = ""
		else:
			office_name = "" 
			
		if 'country' in item_res.keys():
			country = item_res["country"]
			if country is None:
				country = ""
		else:
			country = ""
			
		if 'state' in item_res.keys():
			state = item_res["state"]
			if state is None:
				state = ""
		else:
			state = "" 
			
		if 'city' in item_res.keys():
			city = item_res["city"]
			if city is None:
				city = ""
		else:
			city = ""
			
		if 'email' in item_res.keys():
			email = item_res["email"]
			if email is None:
				email = ""
		else:
			email = "" 
			
		if 'fax' in item_res.keys():
			fax = item_res["fax"]
			if fax is None:
				fax = ""
		else:
			fax = ""
			
		if 'mail_instructions' in item_res.keys():
			mail_instructions = item_res["mail_instructions"]
			if mail_instructions is None:
				mail_instructions = ""
		else:
			mail_instructions = "" 

		if 'phone' in item_res.keys():
			phone = item_res["phone"]
			if phone is None:
				phone = ""
		else:
			phone = "" 
			
		if 'post_type' in item_res.keys():
			post_type = item_res["post_type"]
			if post_type is None:
				post_type = ""
		else:
			post_type = ""
				
		trade_ita_office_locations = TradeItaOfficeLocations(id_text, post, office_name, country, state, city, email, fax, mail_instructions, phone, post_type, search_performed_at)
		db.session.add(trade_ita_office_locations)
		db.session.commit()
		flash('New trade_ita_office_locations entry was successfully posted')
		twid = db.session.query(TradeItaOfficeLocations).order_by(TradeItaOfficeLocations.id.desc()).first()
		result_id = twid.id
		
		if 'address' in item_res.keys():
			for code in item_res["address"]:
				trade_ita_office_locations_address = TradeItaOfficeLocationsAddress(code,result_id,search_performed_at)
				db.session.add(trade_ita_office_locations_address)
				db.session.commit()
				flash('New trade_ita_office_locations_address entry was successfully posted')
				
	return "executed"

@app.route('/ita_trade_articles')
def add_ita_trade_articles():
	url = 'https://api.trade.gov/trade_articles/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')
		
	for item_res in data["results"]: 	
		if 'id' in item_res.keys():
			id_text = item_res["id"]
			if id_text is None:
				id_text = ""
		else:
			id_text = ""
			
		if 'title' in item_res.keys():
			title = item_res["title"]
			if title is None:
				title = ""
		else:
			title = ""
			
		if 'short_title' in item_res.keys():
			short_title = item_res["short_title"]
			if short_title is None:
				short_title = ""
		else:
			short_title = "" 
			
		if 'summary' in item_res.keys():
			summary = item_res["summary"]
			if summary is None:
				summary = ""
		else:
			summary = ""
			
		if 'creation_date' in item_res.keys():
			creation_date = item_res["creation_date"]
			if creation_date is None:
				creation_date = ""
		else:
			creation_date = "" 
			
		if 'release_date' in item_res.keys():
			release_date = item_res["release_date"]
			if release_date is None:
				release_date = ""
		else:
			release_date = ""
			
		if 'expiration_date' in item_res.keys():
			expiration_date = item_res["expiration_date"]
			if expiration_date is None:
				expiration_date = ""
		else:
			expiration_date = "" 
			
		if 'evergreen' in item_res.keys():
			evergreen = item_res["evergreen"]
			if evergreen is None:
				evergreen = ""
		else:
			evergreen = ""
			
		if 'content' in item_res.keys():
			content = item_res["content"]
			if content is None:
				content = ""
		else:
			content = "" 

		if 'keyword' in item_res.keys():
			keyword = item_res["keyword"]
			if keyword is None:
				keyword = ""
		else:
			keyword = "" 
			
		if 'seo_metadata_title' in item_res.keys():
			seo_metadata_title = item_res["seo_metadata_title"]
			if seo_metadata_title is None:
				seo_metadata_title = ""
		else:
			seo_metadata_title = ""

		if 'seo_metadata_description' in item_res.keys():
			seo_metadata_description = item_res["seo_metadata_description"]
			if seo_metadata_description is None:
				seo_metadata_description = ""
		else:
			seo_metadata_description = ""

		if 'seo_metadata_keyword' in item_res.keys():
			seo_metadata_keyword = item_res["seo_metadata_keyword"]
			if seo_metadata_keyword is None:
				seo_metadata_keyword = ""
		else:
			seo_metadata_keyword = ""
			
		if 'trade_url' in item_res.keys():
			trade_url = item_res["trade_url"]
			if trade_url is None:
				trade_url = ""
		else:
			trade_url = ""
			
			
		trade_ita_trade_articles = TradeItaTradeArticles(id_text, title, short_title, summary, creation_date, release_date, expiration_date, evergreen, content, keyword, seo_metadata_title, seo_metadata_description, seo_metadata_keyword, trade_url, search_performed_at)
		db.session.add(trade_ita_trade_articles)
		db.session.commit()
		flash('New trade_ita_trade_articles entry was successfully posted')
		
		twid = db.session.query(TradeItaTradeArticles).order_by(TradeItaTradeArticles.id.desc()).first()
		result_id = twid.id
		
		if 'source_agencies' in item_res.keys():
			for code in item_res["source_agencies"]:
				trade_ita_trade_article_source_agencies = TradeItaTradeArticlesAgencies(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_source_agencies)
				db.session.commit()
				flash('New trade_ita_trade_article_source_agencies entry was successfully posted')
		
		if 'source_business_units' in item_res.keys():
			for code in item_res["source_business_units"]:
				trade_ita_trade_article_source_business_units = TradeItaTradeArticlesSourcesBusinessUnits(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_source_business_units)
				db.session.commit()
				flash('New trade_ita_trade_article_source_business_units entry was successfully posted')
		
		if 'source_offices' in item_res.keys():
			for code in item_res["source_offices"]:
				trade_ita_trade_article_source_offices = TradeItaTradeArticlesSourceOffices(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_source_offices)
				db.session.commit()
				flash('New trade_ita_trade_article_source_offices entry was successfully posted')

		if 'export_phases' in item_res.keys():
			for code in item_res["export_phases"]:
				trade_ita_trade_article_export_phases = TradeItaTradeArticlesExportPhases(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_export_phases)
				db.session.commit()
				flash('New trade_ita_trade_article_export_phases entry was successfully posted')
		
		if 'industries' in item_res.keys():
			for code in item_res["industries"]:
				trade_ita_trade_article_industries = ItaTradeArticlesIndustries(code,result_id)
				db.session.add(trade_ita_trade_article_industries)
				db.session.commit()
				flash('New trade_ita_trade_article_industries entry was successfully posted')
		
		if 'countries' in item_res.keys():
			for code in item_res["countries"]:
				trade_ita_trade_article_countries = ItaTradeArticlesCountries(code,result_id)
				db.session.add(trade_ita_trade_article_countries)
				db.session.commit()
				flash('New trade_ita_trade_article_countries entry was successfully posted')
		
		if 'topics' in item_res.keys():
			for code in item_res["topics"]:
				trade_ita_trade_article_topics = TradeItaArticlesTopics(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_topics)
				db.session.commit()
				flash('New trade_ita_trade_article_topics entry was successfully posted')

		if 'sub_topics' in item_res.keys():
			for code in item_res["sub_topics"]:
				trade_ita_trade_article_sub_topics = TradeItaArticlesSubTopics(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_sub_topics)
				db.session.commit()
				flash('New trade_ita_trade_article_sub_topics entry was successfully posted')				

		if 'geo_regions' in item_res.keys():
			for code in item_res["geo_regions"]:
				trade_ita_trade_article_geo_regions = TradeItaArticlesGeoRegions(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_geo_regions)
				db.session.commit()
				flash('New trade_ita_trade_article_geo_regions entry was successfully posted')	

		if 'geo_subregions' in item_res.keys():
			for code in item_res["geo_subregions"]:
				trade_ita_trade_article_geo_subregions = TradeItaArticlesGeoSubRegions(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_geo_subregions)
				db.session.commit()
				flash('New trade_ita_trade_article_geo_subregions entry was successfully posted')	

		if 'trade_regions' in item_res.keys():
			for code in item_res["trade_regions"]:
				trade_ita_trade_article_trade_regions = TradeItaArticlesTradeRegions(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_trade_regions)
				db.session.commit()
				flash('New trade_ita_trade_article_trade_regions entry was successfully posted')	

		if 'trade_programs' in item_res.keys():
			for code in item_res["trade_programs"]:
				trade_ita_trade_article_trade_programs = TradeItaArticlesTradePrograms(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_trade_programs)
				db.session.commit()
				flash('New trade_ita_trade_article_trade_programs entry was successfully posted')	

		if 'trade_initiatives' in item_res.keys():
			for code in item_res["trade_initiatives"]:
				trade_ita_trade_article_trade_initiatives = TradeItaArticlesTradeInitiatives(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_trade_initiatives)
				db.session.commit()
				flash('New trade_ita_trade_article_trade_initiatives entry was successfully posted')

		if 'file_url' in item_res.keys():
			for code in item_res["file_url"]:
				trade_ita_trade_article_file_url = TradeItaArticlesFileUrl(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_file_url)
				db.session.commit()
				flash('New trade_ita_trade_article_file_url entry was successfully posted')
		
		if 'image_url' in item_res.keys():
			for code in item_res["image_url"]:
				trade_ita_trade_article_image_url = TradeItaArticlesImageUrl(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_image_url)
				db.session.commit()
				flash('New trade_ita_trade_article_image_url entry was successfully posted')
		
		if 'url_html_source' in item_res.keys():
			for code in item_res["url_html_source"]:
				trade_ita_trade_article_url_html_source = TradeItaArticlesUrlHtmlSource(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_url_html_source)
				db.session.commit()
				flash('New trade_ita_trade_article_url_html_source entry was successfully posted')
		
		if 'url_xml_source' in item_res.keys():
			for code in item_res["url_xml_source"]:
				trade_ita_trade_article_url_xml_source = TradeItaArticlesUrlXmlSource(code,result_id,search_performed_at)
				db.session.add(trade_ita_trade_article_url_xml_source)
				db.session.commit()
				flash('New trade_ita_trade_article_url_xml_source entry was successfully posted')
		
	return "executed"
	
@app.route('/ita_zipcode')
def add_ita_zipcode():
	url = 'https://api.trade.gov/ita_zipcode_to_post/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')
		
	for item_res in data["results"]: 
		if 'id' in item_res.keys():
			id_text = item_res["id"]
			if id_text is None:
				id_text = ""
		else:
			id_text = ""
			
		if 'post' in item_res.keys():
			post = item_res["post"]
			if post is None:
				post = ""
		else:
			post = ""
			
		if 'office_name' in item_res.keys():
			office_name = item_res["office_name"]
			if office_name is None:
				office_name = ""
		else:
			office_name = "" 
			
		if 'country' in item_res.keys():
			country = item_res["country"]
			if country is None:
				country = ""
		else:
			country = ""
			
		if 'state' in item_res.keys():
			state = item_res["state"]
			if state is None:
				state = ""
		else:
			state = "" 
			
		if 'city' in item_res.keys():
			city = item_res["city"]
			if city is None:
				city = ""
		else:
			city = ""
			
		if 'email' in item_res.keys():
			email = item_res["email"]
			if email is None:
				email = ""
		else:
			email = "" 
			
		if 'fax' in item_res.keys():
			fax = item_res["fax"]
			if fax is None:
				fax = ""
		else:
			fax = ""
			
		if 'mail_instructions' in item_res.keys():
			mail_instructions = item_res["mail_instructions"]
			if mail_instructions is None:
				mail_instructions = ""
		else:
			mail_instructions = "" 

		if 'phone' in item_res.keys():
			phone = item_res["phone"]
			if phone is None:
				phone = ""
		else:
			phone = "" 
			
		if 'post_type' in item_res.keys():
			post_type = item_res["post_type"]
			if post_type is None:
				post_type = ""
		else:
			post_type = ""
		

		trade_ita_zipcode_to_post = TradeItaZipcodeToPost(id_text, post, office_name, country, state, city, email, fax, mail_instructions, phone, post_type, search_performed_at)
		db.session.add(trade_ita_zipcode_to_post)
		db.session.commit()
		flash('New trade_zipcode_to_post_results entry was successfully posted')
		twid = db.session.query(TradeItaZipcodeToPost).order_by(TradeItaZipcodeToPost.id.desc()).first()
		
		for itm_address in item_res["address"]:
			code = itm_address
			result_id = twid.id
			trade_zipcode_to_post_address = TradeZipcodeAddress(code, result_id)
			db.session.add(trade_zipcode_to_post_address)
			db.session.commit()
			flash('New trade_zipcode_to_post_address entry was successfully posted')
		
	return "executed"
	
@app.route('/bi_service')
def add_bi_service():
	url = 'https://api.trade.gov/business_service_providers/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))
	
	search_performed_at = data["search_performed_at"]
	for item in data["sources_used"]: 
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')

	for item_res in data["results"]: 
		if 'ita_contact_email' in item_res.keys():
			ita_contact_email = item_res["ita_contact_email"]
			if ita_contact_email is None:
				ita_contact_email = ""
		else:
			ita_contact_email = ""
			
		if 'company_name' in item_res.keys():
			company_name = item_res["company_name"]
			if company_name is None:
				company_name = ""
		else:
			company_name = ""
			
		if 'company_phone' in item_res.keys():
			company_phone = item_res["company_phone"]
			if company_phone is None:
				company_phone = ""
		else:
			company_phone = "" 
			
		if 'company_address' in item_res.keys():
			company_address = item_res["company_address"]
			if company_address is None:
				company_address = ""
		else:
			company_address = ""
			
		if 'company_website' in item_res.keys():
			company_website = item_res["company_website"]
			if company_website is None:
				company_website = ""
		else:
			company_website = "" 
			
		if 'company_description' in item_res.keys():
			company_description = item_res["company_description"]
			if company_description is None:
				company_description = ""
		else:
			company_description = ""
			
		if 'company_email' in item_res.keys():
			company_email = item_res["company_email"]
			if company_email is None:
				company_email = ""
		else:
			company_email = "" 
			
		if 'ita_office' in item_res.keys():
			ita_office = item_res["ita_office"]
			if ita_office is None:
				ita_office = ""
		else:
			ita_office = ""
			
		if 'contact_title' in item_res.keys():
			contact_title = item_res["contact_title"]
			if contact_title is None:
				contact_title = ""
		else:
			contact_title = "" 

		if 'contact_name' in item_res.keys():
			contact_name = item_res["contact_name"]
			if contact_name is None:
				contact_name = ""
		else:
			contact_name = "" 
			
		if 'category' in item_res.keys():
			category = item_res["category"]
			if category is None:
				category = ""
		else:
			category = ""
		
		trade_business_service_providers = TradeBusinessServiceProviders(ita_contact_email, company_name, company_phone, company_address, company_website, company_description, company_email, ita_office, contact_title, contact_name, category)
		db.session.add(trade_business_service_providers)
		db.session.commit()
		flash('New trade_business_service_providers entry was successfully posted')
		
		return "executed"

@app.route('/ita_tax')
def add_ita_tax():
	url = 'https://api.trade.gov/ita_taxonomies/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))
	
	search_performed_at = data["search_performed_at"]
	for item in data["sources_used"]: 
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')

	for item_res in data["results"]: 
		if 'id' in item_res.keys():
			text_id = item_res["id"]
			if text_id is None:
				text_id = ""
		else:
			text_id = ""
			
		if 'name' in item_res.keys():
			name = item_res["name"]
			if name is None:
				name = ""
		else:
			name = ""
			
		if 'path' in item_res.keys():
			path = item_res["path"]
			if path is None:
				path = ""
		else:
			path = "" 

		trade_taxonomies_results = TradeTaxonomiesResults(text_id, name, path)
		db.session.add(trade_taxonomies_results)
		db.session.commit()
		flash('New trade_taxonomies_results entry was successfully posted')
		twid = db.session.query(TradeTaxonomiesResults).order_by(TradeTaxonomiesResults.id.desc()).first()
		
		for itm_taxonomies in item_res["taxonomies"]:
			code = itm_taxonomies
			result_id = twid.id
			trade_taxonomies_taxonomy = TradeTaxonomyTaxonomies(code, result_id)
			db.session.add(trade_taxonomies_taxonomy)
			db.session.commit()
			flash('New trade_taxonomies_taxonomy entry was successfully posted')

		for itm_broader_terms in item_res["broader_terms"]:
			code = itm_broader_terms
			result_id = twid.id
			trade_taxonomies_broader_terms = TradeTaxonomyBroaderTerms(code, result_id)
			db.session.add(trade_taxonomies_broader_terms)
			db.session.commit()
			flash('New trade_taxonomies_broader_terms entry was successfully posted')

		for itm_narrower_terms in item_res["narrower_terms"]:
			code = itm_narrower_terms
			result_id = twid.id
			trade_taxonomies_narrower_terms = TradeTaxonomyNarrowTerms(code, result_id)
			db.session.add(trade_taxonomies_narrower_terms)
			db.session.commit()
			flash('New trade_taxonomies_narrower_terms entry was successfully posted')
			
	return "executed"

@app.route('/de_minimis')
def add_de_minimis():
	url = 'https://api.trade.gov/v1/de_minimis/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))
	
	search_performed_at = data["search_performed_at"]
	
	for item in data["sources_used"]:
		
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')

	for item_res in data["results"]: 
		if 'country_name' in item_res.keys():
			country_name = item_res["country_name"]
			if country_name is None:
				country_name = ""
		else:
			country_name = ""
			
		if 'country' in item_res.keys():
			country = item_res["country"]
			if country is None:
				country = ""
		else:
			country = ""
			
		if 'de_minimis_value' in item_res.keys():
			de_minimis_value = item_res["de_minimis_value"]
			if de_minimis_value is None:
				de_minimis_value = 0
		else:
			de_minimis_value = 0 
			
		if 'de_minimis_currency' in item_res.keys():
			de_minimis_currency = item_res["de_minimis_currency"]
			if de_minimis_currency is None:
				de_minimis_currency = ""
		else:
			de_minimis_currency = ""
			
		if 'vat_amount' in item_res.keys():
			vat_amount = item_res["vat_amount"]
			if vat_amount is None:
				vat_amount = 0
		else:
			vat_amount = "" 
			
		if 'vat_currency' in item_res.keys():
			vat_currency = item_res["vat_currency"]
			if vat_currency is None:
				vat_currency = ""
		else:
			vat_currency = ""
			
		if 'notes' in item_res.keys():
			notes = item_res["notes"]
			if notes is None:
				notes = ""
		else:
			notes = "" 

		trade_de_minimis_results = TradeMinimisResults(country_name, country, de_minimis_value, de_minimis_currency, vat_amount, vat_currency, notes)
		db.session.add(trade_de_minimis_results)
		db.session.commit()
		flash('New trade_de_minimis_results entry was successfully posted')
	
	return "executed"

@app.route('/consolidated_screening_list')
def add_consolidated_screening_list():
	url = 'https://api.trade.gov/consolidated_screening_list/search?api_key=YwSGPRhmqZEM51Nk1hWvpyg7'
	response = requests.get(url,verify=False)
	data = json.load(StringIO(response.content))

	search_performed_at = data["search_performed_at"]
	for item in data["sources_used"]: 
		date_request = item["last_imported"]
		sources = Sources(item["source"], item["source_last_updated"], item["last_imported"], search_performed_at)
		db.session.add(sources)
		db.session.commit()
		flash('New sources entry was successfully posted')
	
	for item_result in data["results"]: 
		end_date = item_result["end_date"]		
		if end_date is None:
			end_date="0000-00-00"			
		federal_register_notice = item_result["federal_register_notice"]
		name = item_result["name"]
		remarks = item_result["remarks"]
		source = item_result["source"]
		source_information_url = item_result["source_information_url"]
		source_list_url = item_result["source_list_url"]
		standard_order = item_result["standard_order"]
		start_date = item_result["start_date"]
		consolidated_screening_list_results = ConsolidatedScreenListResults(end_date,federal_register_notice,name,remarks,source,source_information_url,source_list_url,standard_order,start_date)
		db.session.add(consolidated_screening_list_results)
		db.session.commit()
		flash('New consolidated_screening_list_results entry was successfully posted')
		
		twid = db.session.query(ConsolidatedScreenListResults).order_by(ConsolidatedScreenListResults.id.desc()).first()
		
		for item_address in item_result["addresses"]:
			address = item_address["address"]
			city = item_address["city"]
			state = item_address["state"]
			postal_code = item_address["postal_code"]
			country = item_address["country"]
			result_id = twid.id
			consolidated_screening_list_address = ConsolidatedScreenListAddresses(address,city,state,postal_code,country,result_id)
			db.session.add(consolidated_screening_list_address)
			db.session.commit()
			flash('New consolidated_screening_list_addresses entry was successfully posted')
			
	return "executed"
	

def execute_all():
	db.Model = Base
	db.drop_all()
	db.create_all()
	add_market_research_library()
	add_consolidated_screening_list()
	add_trade_events()
	add_trade_leads()
	add_tariff_rates()
	add_ita_faqs()
	add_ita_office_locations()
	add_ita_trade_articles()
	add_ita_zipcode()
	add_bi_service()
	add_ita_tax()
	add_de_minimis()
	
	return "executing tasks"

@app.route('/')	
def timer():
	date = time.strftime("%m/%Y")
	date = date.split("/")

	twid = db.session.query(MarketResearchLibraryResults).order_by(MarketResearchLibraryResults.id.desc()).first()

	if not twid:
		print 'No result found'

	row = twid.search_performed_at
	last_update_date = row.split("-")

	if last_update_date[0] == date[1]:
		print "same years"
		date_month = int(date[0])
		last_month = int(last_update_date[1])+3
		if date_month >= last_month:
			print "three months passed from the last update date"
			execute_all()
					
	if int(last_update_date[0]) < int(date[1]):
		print "a year has passed"
		if int(date[0]) == 3:
			print "three months passed from the start of the year"
			execute_all()
		
	return "executed"
	
if __name__ == '__main__':
    app.run()