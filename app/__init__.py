from flask import Flask
import os
from app.config.config import DevelopmentConfig, ProductionConfig

app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

from app import controllers
from app.views import routes