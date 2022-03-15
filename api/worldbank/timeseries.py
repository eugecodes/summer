import time
import requests
from requests.exceptions import RequestException
from worldbank.exception import ApiException
from worldbank.restore import RestoreDataHandler

class TimeSeries:
    API_URL = "http://api.worldbank.org"
    KEY_REGIONS = "/regions"
    KEY_INCOME_LEVELS = "/incomeLevels"
    KEY_LENDING_TYPES = "/lendingTypes"
    KEY_SOURCES = "/sources"
    KEY_TOPICS = "/topics"
    KEY_COUNTRIES = "/countries"
    KEY_INDICATORS = "/indicators"
    KEY_INDICATORS_DATA = "/countries/%s/indicators/%s"

    CALL_ATTEMPTS = 3  # attempts to call api
    CALL_ATTEMPTS_DELAY = 2  # delay in sec between attempts

    RESULTS_PER_PAGE = 15000

    """ Callable """
    apiExceptionListener = None

    def __init__(self, logger=None):
        self._logger = logger

    def setLogger(self, logger):
        self._logger = logger

    def _log(self, str, lvl='debug'):
        if self._logger is not None:
            getattr(self._logger, lvl)(str)

    def _onApiException(self, handler):
        if self.apiExceptionListener is None:
            return False
        if not hasattr(self.apiExceptionListener, '__call__'):
            raise Exception('TimeSeries::apiExceptionListener is not callable')
        return self.apiExceptionListener(handler)

    def _getApiUrl(self, key, page, perPage, **kwargs):
        if key == TimeSeries.KEY_INDICATORS_DATA:
            countryId = kwargs.get('countryId', None)
            indicatorId = kwargs.get('indicatorId', None)
            if countryId is None:
                raise Exception('countryId missed in kwargs')
            if indicatorId is None:
                raise Exception('indicatorId missed in kwargs')
            url = TimeSeries.API_URL + key % (countryId, indicatorId) + "?page=%s&per_page=%s&format=json" % (page, perPage)
            if 'year' in kwargs:
                url += '&date=%s' % kwargs['year']
            return url

        return TimeSeries.API_URL + key + "?page=%s&per_page=%s&format=json" % (page, perPage)

    def _getResponseData(self, data):
        return data[1]

    def _getResponsePage(self, data):
        return data[0]

    def _validateResponseData(self, data):
        # TODO
        if len(data) != 2:
            raise ApiException('Wrong API response format')

    def _getApiResponse(self, key, page, perPage=None, **kwargs):
        perPage = perPage or TimeSeries.RESULTS_PER_PAGE
        apiUrl = self._getApiUrl(key, page=page, perPage=perPage, **kwargs)

        attempts = TimeSeries.CALL_ATTEMPTS
        while attempts > 0:
            self._log('Call "%s"' % apiUrl)
            self._log('Attempts remain: %s' % attempts)
            attempts -= 1
            try:
                response = requests.get(apiUrl)
                response.raise_for_status()
                data = response.json()
                self._validateResponseData(data)
                self._log('success')
            except (RequestException, ValueError, ApiException) as e:
                self._log(e, 'exception')
                if attempts > 0:
                    self._log('Try again in %s seconds' % TimeSeries.CALL_ATTEMPTS_DELAY)
                    time.sleep(TimeSeries.CALL_ATTEMPTS_DELAY)
                    continue
                raise ApiException(e)
            break

        return data

    def _hasNextPage(self, data):
        page = self._getResponsePage(data)
        return int(page['page']) * int(page['per_page']) < int(page['total'])

    def _generate(self, key, perPage, *, page=1, **kwargs):
        while True:
            try:
                data = self._getApiResponse(key, page, perPage, **kwargs)
                yield self._getResponseData(data)
                page += 1
                if not self._hasNextPage(data):
                    break
            except ApiException as e:
                handler = RestoreDataHandler(key, page=page, perPage=perPage, **kwargs)
                if not self._onApiException(handler):
                    raise
                break

    def getRegionsPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_REGIONS, perPage, **kwargs)

    def getIncomeLevelsPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_INCOME_LEVELS, perPage, **kwargs)

    def getLendingTypesPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_LENDING_TYPES, perPage, **kwargs)

    def getSourcesPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_SOURCES, perPage, **kwargs)

    def getTopicsPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_TOPICS, perPage, **kwargs)

    def getCountriesPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_COUNTRIES, perPage, **kwargs)

    def getIndicatorsPages(self, perPage=None, **kwargs):
        return self._generate(TimeSeries.KEY_INDICATORS, perPage, **kwargs)

    def getIndicatorCountryPages(self, indicatorId, countryId, year=None, perPage=None):
        kwargs = {'indicatorId': indicatorId, 'countryId': countryId}
        if year is not None:
            kwargs['year'] = year
        return self._generate(TimeSeries.KEY_INDICATORS_DATA, perPage, **kwargs)

