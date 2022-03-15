from flask import Flask
import config
from worldbank import model as db
import logging

class App(Flask):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.db_engine = db.sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
        db.init_model(self.db_engine)
        self.db_session = db.DBSession()

    def connectToDb(self):
        self.db_engine = db.sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
        db.init_model(self.db_engine)
        self.db_session = db.DBSession()

    def getEngine(self):
        return self.db_engine

    def getDbSession(self):
        return self.db_session

    def getLogWriter(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(config.LOG_DEBUG)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger

app = App(__name__)

from app import views
