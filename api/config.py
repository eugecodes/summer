import os
# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# DB options
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost:5433/exab'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
# DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Secret key for signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

LOG_DEBUG = 'log/debug.log'
LOG_TS_INCOME_LEVEL = 'log/incomelevel.log'

DATA_IMPORT_YEARS = 5

# email
EMAIL = {
    'ALLOW': False,  # should send email
    'FROM': 'vladimir.shvechko@gmail.com',  # from address
    'TO': 'vladimir.shvechko@hiqo-solutions.com',  # to address
    'SUBJ': 'Import result',  # email subject
    'SERVER_SMTP': 'smtp.gmail.com',  # smtp
    'SERVER_PORT': 587,  # port
    'SERVER_USER': '',  # user
    'SERVER_PASS': ''  # password
}


