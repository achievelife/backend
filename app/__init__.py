from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('app.config')

# Setup scheduler
scheduler = BackgroundScheduler()

# Setup extensions
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Setup CORS
cors = CORS(app)

# Add automated schedules
from app.scheduler import *

# Grab all the views
## Main view
from app.views.main import *

## v1 Admin
from app.views.admin_v1 import admin_v1
app.register_blueprint(admin_v1, url_prefix='/admin/v1')

## v1 API
from app.views.api_v1 import api_v1
app.register_blueprint(api_v1, url_prefix='/api/v1')