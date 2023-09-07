import imp
import os
import sys

from a2wsgi import ASGIMiddleware

from main import app

sys.path.insert(0, os.path.dirname(__file__))

# wsgi = imp.load_source('wsgi', 'main.py')
# application = wsgi.app

application = ASGIMiddleware(app)
