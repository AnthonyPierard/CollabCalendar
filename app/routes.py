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
from forms.form_activity import ActivityForm

#Importation of the models
from models.user import User
from models.activity import Activity

#+---------------+
#| Login section |
#+---------------+
@login_manager.user_loader
def load_user(userid):
    return None

#ROUTES
#Entry point
# @login_required
@app.route("/")
def entry():
    #Render test template
    return render_template("homepage.html")

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

# @login_required
@app.route('/new_activity', methods=['POST', 'GET'])
def new_activity():
    form = ActivityForm()

    if form.validate_on_submit():
        activity = Activity(name = form.name.data, description= form.description.data,
        dateDebut= form.date.data, interval= form.interval.data, status = False)

        db.session.add(activity)
        db.session.commit()
        flash('New activity created')
        return redirect(url_for('entry'))

    else:
        return render_template('new_activity.html', form= form)

# @login_required
@app.route('/modify_activity/<ID>', methods=['POST', 'GET'])
def modify_activity(ID):
    form = ActivityForm()
    activity = Activity.query.filter_by(idTask=ID).first()

    if form.validate_on_submit():
        activity.name= form.name.data
        activity.description= form.description.data
        activity.dateDebut= form.date.data
        activity.interval= form.interval.data

        db.session.commit()
        flash('Activity updated')
        return redirect(url_for('entry'))

    else:
        return render_template('new_activity.html', form= form, activity = activity)

# @login_required
@app.route('/account/<ID>', methods=['POST', 'GET'])
def account(ID):
    form = RegistrationForm()
    user = User.query.filter_by(idUser=ID).first()

    if form.validate_on_submit():
        user.username= form.username.data
        user.set_password(form.password.data)

        db.session.commit()
        flash('informations updated')
        return redirect(url_for('entry'))

    else:
        return render_template('new_activity.html', form= form, user = user)
