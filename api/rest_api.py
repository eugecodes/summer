import os
import sqlite3
import urllib
import urllib2
import json
import time
import requests
from eve import Eve
from StringIO import StringIO
from trade_models import db
from sqlalchemy import create_engine
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

SETTINGS = {
    'SQLALCHEMY_DATABASE_URI': ('postgresql+psycopg2://argentina:mountains@twisted-dragon.cu3ugwf8wzsx.us-west-2.rds.amazonaws.com:5432/twisted'),
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS': ['GET'],
    'DOMAIN': {
        'submission': Submission._eve_schema['submission'],
    },
}

application = Eve(auth=None, settings=SETTINGS, data=SQL)
 
# bind SQLAlchemy
db = application.data.driver
Base.metadata.bind = db.engine
#db.Model = db
db.create_all()

if __name__ == "__main__":
    application.run(debug=True)

if __name__ == '__main__':
    app.run()