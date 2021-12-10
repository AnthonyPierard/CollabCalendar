#All importation
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from flask.helpers import flash
from werkzeug.urls import url_parse

#Importation of App and db
from app import app, db
from app import login_manager

#Importation of the form
from forms.form_user import LoginForm, RegistrationForm

#Importation of the models
from models.user import User

#+---------------+
#| Login section |
#+---------------+
@login_manager.user_loader
def load_user(userid):
    return None

#ROUTES
#Entry point
@login_required
@app.route("/")
def entry():
    #Render test template
    return render_template("temp.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index', _user=form.username.data))
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('You are not registered yet', 'info')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Invalid username or password', 'info')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    
    else:
        return render_template(url_for('login.html'), form = form)

@app.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered')
        return redirect(url_for('login'))

    else:
        return render_template('registration.html', form= form)

@app.route('/logout')
def funcLogout():
    logout_user()
    return redirect(url_for('funcLoginForm'))
