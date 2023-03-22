# flask looks for files with specific names 
# helps computer and app talk to each other
# allows appliation to communicate with the internet

# allows app to talk to the operating system
# this can usually be a frequent copy base, a pretty consistent 
# across many projects
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    '''
        Set config variables for the flask app using
        Enviornment variables where available.
        Otherwise, create the config variable if not done already
    '''

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('KEY_SECRET') or "Never forget the OR"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False


