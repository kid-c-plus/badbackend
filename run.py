"""run.py

Build server and load services. If run as main, start Werkzeug
development server. Import flaskapp from this script for WSGI scripts
"""

from badbackend.core import *
from badbackend.loggers
import yaml

config = yaml.load(open("config.yaml"), Loader=yaml.Loader)
