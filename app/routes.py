#All importation
from flask import render_template

#Importation of App
from app import app
from app import login_manager

#+---------------+
#| Login section |
#+---------------+
@login_manager.user_loader
def load_user(userid):
    return None

#ROUTES
#Entry point
@app.route("/")
def entry():
    #Render test template
    return render_template("temp.html")