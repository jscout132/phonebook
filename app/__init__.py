# flask looks for files with specific names 
# they need to be these names
# runs most of the logic, instantite, get all the parts moving

from flask import Flask

# imports the config class from the config file
from config import Config

# import the site folder
from .site.routes import site

#imports the auth folder
from .authentication.routes import auth

from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma 
from flask_cors import CORS
from helpers import JSONEncoder

# makes the app, this is where flask will run from
app = Flask(__name__)
CORS(app)

# could do all python in one file, but it would be so big
# troubleshooting is about to get much more intense
# something call separation of concerns
# these different files have different jobs, it helps clarify
# where the different tasks will be run
# helps clarify what the goal is for each files
# clarifies both the what we're doing and the why we're doing it

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

app.json_encoder = JSONEncoder

root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)
