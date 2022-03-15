#!/usr/bin/python3
activate_this = '/var/www/exab/venv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))
exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'), dict(__file__=activate_this))

import sys
sys.path.append("/var/www/exab")
from app import app as application