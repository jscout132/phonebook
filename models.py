# flask looks for files with specific names 
# helps with databases, less sql table and query creation, will automate somet of it

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

#set up the login decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#this entire class is for users to create accounts and log in, log out
class User(db.Model, UserMixin):
    #nullable = True means it can be empty
    #nullable = False means it cannot be empty
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default='')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    #every class needs __init__
    #the ones that don't have a defaul value should go near the front
    #some of the above variables aren't in the init and that's ok
    #the yellow text here calls functions that are created below
    def __init__(self, email, first_name='',last_name='', password='', token = '', g_auth_verify=False):
        self.id=self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    #sends back a token hex that is 24 characters long
    #a randomized bunch of letters and numbers
    def set_token(self, length):
        return secrets.token_hex(length)
    
    #uuid4() is a function within the uuid module
    #creates unique id as the primary key
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self,password):
        self.pw_hash=generate_password_hash(password)
        return self.pw_hash
    
    #reprint
    #used to spit out everything created in a class, but we're using it
    #to confirm something was added to the database
    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
#this is the class for the actual contacts to create that database
class Contact(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, email, phone_number, address, user_token, id=''):
       self.id = self.set_id()
       self.name = name
       self.email = email
       self.phone_number = phone_number
       self.address = address
       self.user_token = user_token

    def __repr__(self):
        return f'The following contact has been added to the phonebook {self.name}'
    
    def set_id(self):
        return (secrets.token_urlsafe())

#ma is marshmallow    
class ContactSchema(ma.Schema):
    class Meta:
        fields=['id','name','email','phone_number','address']

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)