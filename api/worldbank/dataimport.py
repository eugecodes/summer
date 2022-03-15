from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from sqlalchemy import event
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.base import NEVER_SET, NO_VALUE
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from worldbank.model import Region, Country, IncomeLevel, LendingType, Source, Topic, Indicator, IndicatorCountry, \
    IndicatorRegion, IndicatorIncomeLevel, CountryIncomeLevelHistory, CountryLendingTypeHistory
from worldbank.timeseries import TimeSeries


class TimeSeriesImport:

    MAX_WORKERS = 10

    def __init__(self, sessionClass):
        self.DbSession = sessionClass
        self.db_session = sessionClass()
        self.tsApi = None
        self._logger = None

    def setLogWriter(self, logWriter):
        self._logger = logWriter
        ts = self.getTimeSeriesApi()
        if ts is not None:
            ts.setLogger(self._logger)

    def _log(self, str, lvl='debug'):
        if self._logger is not None:
            getattr(self._logger, lvl)(str)

    def getTimeSeriesApi(self):
        if self.tsApi is None:
            self.tsApi = TimeSeries(self._logger)
        return self.tsApi

    def importRegions(self, **kwargs):
        ts = self.getTimeSeriesApi()
        for page in ts.getRegionsPages(**kwargs):
            if page is None:
                break
            for data in page:
                model = Region(
                    id=data.get('code'),
                    name=data.get('name')
                )
                self.db_session.merge(model)

    def importIncomeLevels(self):
        ts = self.getTimeSeriesApi()
        for page in ts.getIncomeLevelsPages():
            if page is None:
                break
            for data in page:
                model = IncomeLevel(
                    id=data.get('id'),
                    value=data.get('value')
                )
                self.db_session.merge(model)

    def importLendingTypes(self):
        ts = self.getTimeSeriesApi()
        for page in ts.getLendingTypesPages():
            if page is None:
                break
            for data in page:
                model = LendingType(
                    id=data.get('id'),
                    value=data.get('value')
                )
                self.db_session.merge(model)

    def importSources(self):
        ts = self.getTimeSeriesApi()
        for page in ts.getSourcesPages():
            if page is None:
                break
            for data in page:
                model = Source(
                    id=data.get('id'),
                    name=data.get('name'),
                    description=data.get('description'),
                    url=data.get('url')
                )
                self.db_session.merge(model)

    def importTopics(self):
        ts = self.getTimeSeriesApi()
        for page in ts.getTopicsPages():
            if page is None:
                break
            for data in page:
                model = Topic(
                    id=data.get('id'),
                    value=data.get('value'),
                    sourceNote=data.get('sourceNote')
                )
                self.db_session.merge(model)

    @staticmethod
    def _checkSkipCountry(countryData):
        regionData = countryData.get('region')
        if regionData.get('id') == 'NA' or regionData.get('value') == 'Aggregates':
            return True
        ilData = countryData.get('incomeLevel')
        if ilData.get('id') == 'NA' or ilData.get('value') == 'Aggregates':
            return True
        ltData = countryData.get('lendingType')
        if ltData.get('id') == 'NA' or ltData.get('value') == 'Aggregates':
            return True
        return False

    @staticmethod
    def _isValueChanged(oldval, newval):
        return oldval is not NEVER_SET and oldval is not NO_VALUE and oldval != newval

    def _onIncomeLevelChanged(self, target, value, oldvalue, initiator):
        if self._isValueChanged(oldvalue, value):
            self.db_session.add(CountryIncomeLevelHistory(
                oldValue=oldvalue,
                newValue=value
            ))

    def _onLendingTypeChanged(self, target, value, oldvalue, initiator):
        if self._isValueChanged(oldvalue, value):
            self.db_session.add(CountryLendingTypeHistory(
                oldValue=oldvalue,
                newValue=value
            ))

    def _setCountryListeners(self):
        event.listen(Country.incomeLevel, 'set', self._onIncomeLevelChanged)
        event.listen(Country.lendingType, 'set', self._onLendingTypeChanged)

    def _removeCountryListeners(self):
        event.remove(Country.incomeLevel, 'set', self._onIncomeLevelChanged)
        event.remove(Country.lendingType, 'set', self._onLendingTypeChanged)

    def importCountries(self):
        ts = self.getTimeSeriesApi()
        self._setCountryListeners()

        lendingTypes = self.db_session.query(LendingType).all()
        lendingTypesFormatted = {lt.id: lt for lt in lendingTypes}

        regions = self.db_session.query(Region).all()
        regionsFormatted = {r.id: r for r in regions}

        incomeLevels = self.db_session.query(IncomeLevel).all()
        incomeLevelsFormatted = {il.id: il for il in incomeLevels}
        for page in ts.getCountriesPages():
            if page is None:
                break
            for data in page:
                regionData = data.get('region')
                if regionData.get('id') == 'NA' or regionData.get('value') == 'Aggregates':
                    # search region to update iso2code
                    regionId = data.get('id')
                    regionIso2code = data.get('iso2Code')
                    if regionId in regionsFormatted:
                        region = regionsFormatted[regionId]
                        region.iso2code = regionIso2code
                    continue

                # skip aggregates not in DB
                if self._checkSkipCountry(data):
                    # self._log('Skip country id="%s"' % data.get('iso2code'))
                    continue

                create = False
                model = self.db_session.query(Country).options(joinedload(Country.lendingType),
                                                               joinedload(Country.incomeLevel)).get(
                    data.get('iso2Code'))
                if model is None:
                    model = Country(id=data.get('iso2Code'))
                    create = True

                try:
                    longitude = Decimal(data.get('longitude'))
                    latitude = Decimal(data.get('latitude'))
                except Exception:
                    longitude = None
                    latitude = None

                # region
                region = None
                regionId = data.get('region').get('id')
                if regionId is not None:
                    region = regionsFormatted.get(regionId)
                # admin region
                adminRegion = None
                admRegId = data.get('adminregion').get('id')
                if admRegId is not None:
                    adminRegion = regionsFormatted.get(admRegId)

                # income level
                incomeLevel = None
                ilId = data.get('incomeLevel').get('id')
                if ilId is not None:
                    incomeLevel = incomeLevelsFormatted.get(ilId)

                # lending type
                lendingType = None
                ltId = data.get('lendingType').get('id')
                if ltId is not None:
                    lendingType = lendingTypesFormatted.get(ltId)

                model.iso2code = data.get('iso2Code')
                model.iso3code = data.get('id')
                model.name = data.get('name')
                model.capital = data.get('capitalCity')
                model.longitude = longitude
                model.latitude = latitude
                model.region = region
                model.adminRegion = adminRegion
                model.incomeLevel = incomeLevel
                model.lendingType = lendingType

                if create:
                    self.db_session.add(model)

        self._removeCountryListeners()

    def importIndicators(self):
        ts = self.getTimeSeriesApi()

        sources = self.db_session.query(Source).all()
        sourcesFormatted = {s.id: s for s in sources}
        topicModels = self.db_session.query(Topic).all()
        topicsFormatted = {t.id: t for t in topicModels}
        for page in ts.getIndicatorsPages():
            if page is None:
                break
            for data in page:
                create = False
                model = self.db_session.query(Indicator).get(data.get('id'))
                if model is None:
                    model = Indicator(id=data.get('id'))
                    create = True

                # source
                sourceId = data.get('source').get('id')
                source = None
                if sourceId is not None:
                    source = sourcesFormatted.get(int(sourceId))

                # topics
                topics = []
                topicsData = data.get('topics')
                for topicTmp in topicsData:
                    tId = topicTmp.get('id')
                    topic = None
                    if tId is not None:
                        topic = topicsFormatted.get(int(tId))
                    if topic is not None:
                        topics.append(topic)

                model.name = data.get('name')
                model.sourceNote = data.get('sourceNote')
                model.sourceOrganization = data.get('sourceOrganization')
                model.source = source
                model.topics = topics

                if create:
                    self.db_session.add(model)

    def _importIndicatorCountries(self, indicatorId, year, ctryIds):
        ts = self.getTimeSeriesApi()
        session = self.DbSession()
        ctryId = 'all'
        indicator = session.query(Indicator).get(indicatorId)
        for page in ts.getIndicatorCountryPages(indicator.id, ctryId, year):
            if page is None:
                break
            for data in page:
                date = data.get('date')

                countryId = data.get('country').get('id')
                if countryId not in ctryIds:
                    continue
                country = session.query(Country).get(countryId)

                try:
                    date = int(date)
                except Exception:
                    # self._log('Indicator id="%s", Country id="%s": wrong date type: "%s"'
                    #           % (indicator.id, countryId, date))
                    continue

                create = False
                model = session.query(IndicatorCountry).get((indicator.id, date, country.id))
                if model is None:
                    model = IndicatorCountry(country=country, indicator=indicator, date=date)
                    create = True

                model.value = data.get('value')
                if create:
                    session.add(model)
        session.commit()
        self.DbSession.remove()

    def _importIndicatorCountriesRegions(self, indicatorId, year, ctryIds, regionsCodes):
        ts = self.getTimeSeriesApi()
        session = self.DbSession()
        ctryId = 'all'
        for page in ts.getIndicatorCountryPages(indicatorId, ctryId, year):
            if page is None:
                break
            for data in page:
                value = data.get('value')
                if not value:
                    continue

                date = data.get('date')
                try:
                    date = int(date)
                except Exception:
                    # self._log('Indicator id="%s", Country id="%s": wrong date type: "%s"'
                    #           % (indicator.id, countryId, date))
                    continue

                id = data.get('country').get('id')
                if id in ctryIds:
                    self._saveIndicatorCountryData(indicatorId, id, date, value)
                    continue
                if id in regionsCodes:
                    self._saveIndicatorRegionData(indicatorId, id, date, value)

        session.commit()
        self.DbSession.remove()

    def _saveIndicatorCountryData(self, indicatorId, countryId, date, value):
        session = self.DbSession()
        country = session.query(Country).get(countryId)
        indicator = session.query(Indicator).get(indicatorId)

        create = False
        model = session.query(IndicatorCountry).get((indicator.id, date, country.id))
        if model is None:
            model = IndicatorCountry(country=country, indicator=indicator, date=date)
            create = True

        model.value = value
        if create:
            session.add(model)

    def _saveIndicatorRegionData(self, indicatorId, iso2code, date, value):
        session = self.DbSession()
        try:
            region = session.query(Region).filter(Region.iso2code == iso2code).one()
        except (MultipleResultsFound, NoResultFound):
            return
        indicator = session.query(Indicator).get(indicatorId)

        create = False
        model = session.query(IndicatorRegion).get((indicator.id, date, region.id))
        if model is None:
            model = IndicatorRegion(region=region, indicator=indicator, date=date)
            create = True

        model.value = value
        if create:
            session.add(model)

    def importIndicatorCountryData(self, year=None):
        self._log('importIndicatorCountryData')
        indicators = self.db_session.query(Indicator).order_by(Indicator.id).all()
        countries = self.db_session.query(Country).all()
        countriesIds = [country.id for country in countries]
        regions = self.db_session.query(Region).all()
        regionsCodes = [region.iso2code for region in regions]

        # logging.basicConfig(
        #     level=logging.INFO,
        #     format='%(relativeCreated)s %(message)s',
        # )
        # start_time = time.time()
        # logging.info('start')
        executor = ThreadPoolExecutor(max_workers=TimeSeriesImport.MAX_WORKERS)
        ex = []
        for indicator in indicators:
            # self._importIndicatorCountries(indicator.id, year, countriesIds)
            ex.append(executor.submit(self._importIndicatorCountriesRegions, indicator.id, year, countriesIds,
                                      regionsCodes))
        # logging.info('end')
        # logging.info("--- %s seconds ---" % (time.time() - start_time))
        for future in futures.as_completed(ex):
            res = future.result()
        # logging.info("--- %s seconds EVERYTHING END ---" % (time.time() - start_time))
        self._log('importIndicatorCountryData COMPLETE')

    def importIndicatorIncLevelData(self, year=None):
        self._log('importIndicatorIncLevelData')
        indicators = self.db_session.query(Indicator).all()
        incLevels = self.db_session.query(IncomeLevel).all()

        # logging.basicConfig(
        #     level=logging.INFO,
        #     format='%(relativeCreated)s %(message)s',
        # )
        # start_time = time.time()
        # logging.info('start')
        executor = ThreadPoolExecutor(max_workers=10)
        ex = []
        for indicator in indicators:
            for incLevel in incLevels:
                ex.append(executor.submit(self._importIndicatorIncomeLevels, indicator.id, incLevel.id, year))
        # logging.info('end')
        # logging.info("--- %s seconds ---" % (time.time() - start_time))
        for future in futures.as_completed(ex):
            res = future.result()
        # logging.info("--- %s seconds EVERYTHING END ---" % (time.time() - start_time))
        self._log('importIndicatorIncLevelData COMPLETE')

    def _importIndicatorIncomeLevels(self, indicatorId, incLevelId, year):
        session = self.DbSession()
        ts = self.getTimeSeriesApi()
        for page in ts.getIndicatorCountryPages(indicatorId, incLevelId, year):
            if page is None:
                break
            for data in page:
                date = data.get('date')
                value = data.get('value')
                if not value:
                    continue
                try:
                    date = int(date)
                except Exception:
                    # self._log('Indicator id="%s", Income Level id="%s": wrong date type: "%s"'
                    #           % (indicator.id, incLevel.id, date))
                    continue

                create = False
                model = session.query(IndicatorIncomeLevel).get((indicatorId, date, incLevelId))
                if model is None:
                    indicator = session.query(Indicator).get(indicatorId)
                    incLevel = session.query(IncomeLevel).get(incLevelId)
                    model = IndicatorIncomeLevel(incomeLevel=incLevel, indicator=indicator, date=date)
                    create = True

                model.value = value
                if create:
                    session.add(model)
        session.commit()
        self.DbSession.remove()
