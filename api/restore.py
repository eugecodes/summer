from api_exception_processor import ApiExceptionProcessor
import config
from import_helper import isLockedProcess, logger, lockProcess, unlockProcess
from worldbank.dataimport import TimeSeriesImport
from worldbank.timeseries import TimeSeries
from worldbank import model as db

db_engine = db.sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
db.init_model(db_engine)
DbSession = db.DBSession
db.metadata.create_all(db_engine)

try:
    if isLockedProcess():
        raise Exception('Process is locked')
    else:
        try:
            logger.debug('Restore started')

            imp = TimeSeriesImport(DbSession)
            imp.setLogWriter(logger)
            tsApi = imp.getTimeSeriesApi()

            session = DbSession()
            processor = ApiExceptionProcessor()
            handlers = processor.getHandlers()
            for key in handlers:
                obj = handlers[key]
                if obj.type == TimeSeries.KEY_REGIONS:
                    imp.importRegions(**obj.kwargs)
                    session.commit()
                    processor.removeHandler(key)
        except BaseException as e:
            unlockProcess()
            raise
        finally:
            DbSession.remove()
except BaseException as e:
    logger.exception(e)
    raise e

