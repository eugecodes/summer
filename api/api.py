from flask import render_template, request, jsonify
import os
import logging
import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from trade_models import db, Sources, Base, CommonColumns, MarketResearchLibraryResults, Countries, Industries, ItaIndustries, ConsolidatedScreenListAddresses, ConsolidatedScreenListResults, TradeEventsResults, TradeEventVenues, TradeEventContacts, TradeEventAggregations, TradeLeadResults, TradeLeadCategories, TradeLeadAggregations, TrafficRateResults, TrafficRatesAnnualRate, TrafficAltAnnualRate, TradeItaFaqs, TradeItaFaqsTopic, TradeItaOfficeLocations, TradeItaOfficeLocationsAddress, TradeItaTradeArticles, TradeItaTradeArticlesAgencies, TradeItaTradeArticlesSourcesBusinessUnits, TradeItaTradeArticlesSourceOffices, TradeItaTradeArticlesExportPhases, TradeItaArticlesTopics, TradeItaArticlesSubTopics, TradeItaArticlesGeoRegions, TradeItaArticlesGeoSubRegions, TradeItaArticlesTradeRegions, TradeItaArticlesTradePrograms, TradeItaArticlesTradeInitiatives, TradeItaArticlesFileUrl, TradeItaArticlesImageUrl, TradeItaArticlesUrlHtmlSource, TradeItaArticlesUrlXmlSource, TradeBusinessServiceProviders, TradeTaxonomiesResults,TradeTaxonomyTaxonomies,TradeTaxonomyBroaderTerms,TradeTaxonomyNarrowTerms, TradeMinimisResults, TradeItaZipcodeToPost, TradeZipcodeAddress, MarketResearchLibraryIndustries, MarketResearchLibraryItaIndustries, MarketResearchLibraryCountries, TradeEventAggregationsCountries, TradeEventIndustries, TradeLeadAggregationsCountries, TradeLeadIndustries, TradeItaFaqsCountries, TradeItaFaqsIndustries, ItaTradeArticlesIndustries, ItaTradeArticlesCountries, MarketResearchLibraryAddress
from worldbank.model.models import Region, IncomeLevel, LendingType, Country, Indicator, Topic, IndicatorCountry, IndicatorRegion, IndicatorIncomeLevel, CountryIncomeLevelHistory, CountryLendingTypeHistory
import simplejson as json

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://argentina:mountains@twisted-dragon.cu3ugwf8wzsx.us-west-2.rds.amazonaws.com:5432/twisted'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

def postprocessor(data):
	json.dumps(data, use_decimal=True)
	return data

db = flask.ext.sqlalchemy.SQLAlchemy(app)
Base.metadata.bind = db.engine
db.create_all()
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

#WorldBank API Endpoints
app.register_blueprint(manager.create_api_blueprint(Region, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(IncomeLevel, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(LendingType, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(Country, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(Indicator, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(Topic, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(IndicatorCountry, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(IndicatorRegion, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(IndicatorIncomeLevel, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(CountryIncomeLevelHistory, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(CountryLendingTypeHistory, results_per_page = 100, methods=['GET', 'POST']))

#Trade API Endpoints
app.register_blueprint(manager.create_api_blueprint(Sources, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(MarketResearchLibraryResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(Countries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(ConsolidatedScreenListAddresses, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(ConsolidatedScreenListResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeEventsResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeEventVenues, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeEventContacts, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeEventAggregations, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeLeadResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeLeadCategories, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeLeadAggregations, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TrafficRateResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TrafficRatesAnnualRate, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TrafficAltAnnualRate, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaFaqs, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaFaqsTopic, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaOfficeLocations, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaOfficeLocationsAddress, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaTradeArticles, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaTradeArticlesAgencies, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaTradeArticlesSourcesBusinessUnits, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaTradeArticlesSourceOffices, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaTradeArticlesExportPhases, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesTopics, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesSubTopics, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesGeoRegions, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesGeoSubRegions, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesTradeRegions, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesTradePrograms, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesTradeInitiatives, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesFileUrl, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesImageUrl, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesUrlHtmlSource, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaArticlesUrlXmlSource, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeBusinessServiceProviders, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeTaxonomiesResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeTaxonomyTaxonomies, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeTaxonomyBroaderTerms, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeTaxonomyNarrowTerms, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeMinimisResults, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaZipcodeToPost, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeZipcodeAddress, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(MarketResearchLibraryIndustries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(MarketResearchLibraryItaIndustries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(MarketResearchLibraryCountries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeEventAggregationsCountries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeEventIndustries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeLeadAggregationsCountries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeLeadIndustries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaFaqsCountries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(TradeItaFaqsIndustries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(ItaTradeArticlesIndustries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(ItaTradeArticlesCountries, results_per_page = 100, methods=['GET', 'POST']))
app.register_blueprint(manager.create_api_blueprint(MarketResearchLibraryAddress, results_per_page = 100, methods=['GET', 'POST']))

if __name__ == '__main__':
	if 'PORT' in os.environ:
		port = int(os.environ.get('PORT'))
		host = '0.0.0.0'
	else:
	
		port = 5000
		host = '127.0.0.1'

@app.route('/', methods=['GET'])
def index():
	hosturl = "" + request.host
	list = [
		#WorldBank API Endpoints
		{'url': hosturl + "/api/" + Region.__tablename__, 'desc': 'WorldBank API Endpoint Region'},
		{'url': hosturl + "/api/" + IncomeLevel.__tablename__, 'desc': 'WorldBank API Endpoint Income Level'},
		{'url': hosturl + "/api/" + LendingType.__tablename__, 'desc': 'WorldBank API Endpoint Lending Type'},
		{'url': hosturl + "/api/" + Country.__tablename__, 'desc': 'WorldBank API Endpoint Country'},
		{'url': hosturl + "/api/" + Indicator.__tablename__, 'desc': 'WorldBank API Endpoint Indicator'},
		{'url': hosturl + "/api/" + Topic.__tablename__, 'desc': 'WorldBank API Endpoint Topic'},
		{'url': hosturl + "/api/" + IndicatorCountry.__tablename__, 'desc': 'WorldBank API Endpoint Indicator Country'},
		{'url': hosturl + "/api/" + IndicatorRegion.__tablename__, 'desc': 'WorldBank API Endpoint Indicator Region'},
		{'url': hosturl + "/api/" + IndicatorIncomeLevel.__tablename__, 'desc': 'WorldBank API Endpoint Indicator Income Level'},
		{'url': hosturl + "/api/" + CountryIncomeLevelHistory.__tablename__, 'desc': 'WorldBank API Endpoint Country Income Level History'},
		{'url': hosturl + "/api/" + CountryLendingTypeHistory.__tablename__, 'desc': 'WorldBank API Endpoint Country Lending Type History'},
		#Trade API Endpoints
		{'url': hosturl + "/api/" + Sources.__tablename__, 'desc': 'Sources of where trade info is got'},
		{'url': hosturl + "/api/" + MarketResearchLibraryResults.__tablename__, 'desc': 'provides metadata for country and industry reports that are produced by ITAs trade experts and are available in ITAs online market research library. ITA commercial officers that are stationed around the world, publish these authoritative reports in conjunction with Foreign Service officers from the State Department.'},
		{'url': hosturl + "/api/" + ConsolidatedScreenListResults.__tablename__, 'desc': 'consolidates eleven export screening lists of the Departments of Commerce, State and the Treasury into a single data feed as an aid to industry in conducting electronic screens of potential parties to regulated transactions.'},
		{'url': hosturl + "/api/" + TradeEventsResults.__tablename__, 'desc': 'provides data on events for U.S. businesses interested in selling their products and services overseas. These events include industry conferences, webinars, lectures, and trade missions organized by ITA and other trade agencies including: The U.S. Trade and Development Agency, The State Department, The Small Business Administration.'},
		{'url': hosturl + "/api/" + TradeLeadResults.__tablename__, 'desc': 'provides contract opportunities for U.S. businesses selling their products and services overseas. These leads come from a variety of sources and we continue to expand the number of leads available. We currently provide trade leads, procurement opportunities, and contract notifications from: The State Departments Business Information Database System (BIDS), FedBizOps, The United Kingdom, Canada, The Millennium Challenge Corporation, Australia, The United States Trade and Development Agency (USTDA)'},
		{'url': hosturl + "/api/" + TrafficRateResults.__tablename__, 'desc': 'provides data about each country with whom the United States has a Free Trade Agreement (FTA). When the U.S. enters into an FTA with a foreign government, it negotiates lower tariff rates with that government for a wide variety of products. A tariff is a tax that a company must pay a foreign country when shipping a product to that country. Typically the FTA tariffs rates decline over several years.provides information on tariff rates for the following countries: Australia, Bahrain, Chile, Colombia, Costa Rica, Dominican Republic, El Salvador, Guatemala, Honduras, Morocco, Nicaragua, Oman, Panama, Peru, Singapore, and South Korea.Because the North American Free Trade Agreement (NAFTA) tariff rates have declined to zero, Canada and Mexico data is not included. Similarly, the tariff rates for almost all products shipped to Israel and Jordon have declined to zero and are not included here.'},
		{'url': hosturl + "/api/" + TradeItaFaqs.__tablename__, 'desc': 'Frequent Asked Questions of Trade Information'},
		{'url': hosturl + "/api/" + TradeItaOfficeLocations.__tablename__, 'desc': 'provides contact and address information for all of ITAs domestic and international export assistance centers. There are almost 200 ITA centers worldwide whose locations are managed by ITAs internal office management system'},
		{'url': hosturl + "/api/" + TradeItaTradeArticles.__tablename__, 'desc': 'provides in-depth news and articles written by Trade Specialists working in the Federal government. The authors include staff from ITA as well as other Trade Promotion Coordinating Committee (TPCC) agencies such as:Export-Import Bank, Overseas Private Investment Corporation (OPIC), U.S. Trade and Development Agency (USTDA), Small Business Administration (SBA)'},
		{'url': hosturl + "/api/" + TradeBusinessServiceProviders.__tablename__, 'desc': 'directory of U.S. and foreign-based businesses providing services that many small and medium sized exporters require to succeed in foreign markets. Businesses can sign up to be a Service Provider on export.gov.'},
		{'url': hosturl + "/api/" + TradeTaxonomiesResults.__tablename__, 'desc': 'gives developers direct access to the exporting, trade, and investment terms that ITA uses to tag the content and data in its other APIs. Currently, ITA has three taxonomies: Geographic Regions, Industries, and Topics. This API includes all terms in their proper hierarchy in the relevant taxonomy. ITA imports data for its other APIs from many sources. If the source data is already tagged, ITA does the following: Imports those tags (terms) along with the data, Maps the terms to ITAs taxonomies, Publishes both the original terms and the ITA terms with the data in the API.'},
		{'url': hosturl + "/api/" + TradeMinimisResults.__tablename__, 'desc': 'provides data about the De Minimis amount and the Value Added Tax (VAT) amount that products may be subject to when exported to foreign countries. De Minimis is the threshold for a products value below which no duty or tariff is charged. Furthermore, products below the De Minimis undergo minimal clearance procedures, such as customs and paperwork requirements. Similarly, the value of the exported products must exceed the VAT amount before it is subject to VAT.'},
		{'url': hosturl + "/api/" + TradeItaZipcodeToPost.__tablename__, 'desc': 'provides direct access to the U.S. Export Assistance Centers (USEACs) that have been assigned to all of the 40,000+ zip codes in the United States. It is not enough to do a proximity search for a zip code and a USEAC. Each center has specialists on hand for each particular region'},
	]
    # jsonify will do for us all the work, returning the
    # previous data structure in JSON
	return jsonify(results=postprocessor(list))

    #return list
	
app.run(host = host, port = port)