#!/home2/slowerin/venv/drone_daydream/bin/python

from flup.server.fcgi import WSGIServer
from drone_daydream_app import app as application

WSGIServer(application).run()
