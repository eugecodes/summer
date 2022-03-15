from api_exception_processor import ApiExceptionProcessor
from import_helper import isLockedProcess, logger, lockProcess, unlockProcess, sendDebugEmail, sendErrorEmail
from worldbank import model as db
import config
from worldbank.dataimport import TimeSeriesImport


db_engine = db.sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
db.init_model(db_engine)
DbSession = db.DBSession
db.metadata.create_all(db_engine)

try:
    if not isLockedProcess():
        try:
            logger.debug('Import started')

            imp = TimeSeriesImport(DbSession)
            imp.setLogWriter(logger)
            tsApi = imp.getTimeSeriesApi()
            tsApi.apiExceptionListener = ApiExceptionProcessor().clear().saveHandler

            session = DbSession()
            lockProcess()
            imp.importRegions()
            imp.importTopics()
            imp.importLendingTypes()
            imp.importIncomeLevels()
            imp.importSources()
            imp.importCountries()
            session.commit()
            imp.importIndicators()
            session.commit()
            imp.importIndicatorCountryData()
            session.commit()
            # imp.importIndicatorRegionData()
            # session.commit()
            imp.importIndicatorIncLevelData()
            session.commit()
            unlockProcess()
            logger.debug('Import completed')
            sendDebugEmail()
        except BaseException as e:
            unlockProcess()
            raise
        finally:
            DbSession.remove()

except BaseException as e:
    logger.exception(e)
    sendErrorEmail(e)
    raise
