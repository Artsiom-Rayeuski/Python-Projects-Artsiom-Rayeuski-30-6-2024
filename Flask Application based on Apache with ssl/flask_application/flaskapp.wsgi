import sys
import logging

sys.path.insert(0, '/var/www/flask-application')
sys.path.insert(0, '/var/www/flask-application/venv/lib/python3.11/site-packages/')

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app from __init__.py
from project import app as application

if __name__ == "__main__":
    application.run()