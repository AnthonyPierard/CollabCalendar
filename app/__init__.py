#All importation
from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#Initialize Flask
app = Flask(__name__)

#Load config
app.config.from_object(Config)

#Initialize The database
db = SQLAlchemy( app )
migrate = Migrate(app, db)

#Create login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = "You cannot access this page"

#Create data base
db = SQLAlchemy(app)

#Get routes
#TODO Ajouter noms des fichiers contenants le routage dans l'importation de app
from app import routes, API