#All importation
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from flask.helpers import flash
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import date, datetime
import os

#Importation of App and db
from app import app, db
from app import login_manager

#Importation of the form
from app.forms.form_user import LoginForm, RegistrationForm, ModifyForm
from app.forms.form_activity import ActivityForm
from app.forms.form_group import newGroup

#Importation of the models
from app.models.user import *
from app.models.activity import Activity


from app.TEMPORAIREaddSomeData import setUpDB
setUpDB()


#+---------------+
#| Login section |
#+---------------+
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

#ROUTES
#Entry point
@app.route("/")
@login_required
def entry():
    #Render test template
    return render_template("homepage.html")

#Login and registration parts
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
            next_page = url_for('entry')
        return redirect(next_page)
    
    else:
        return render_template('login.html', form = form)

@app.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        photo = form.photo.data
        photoName = secure_filename(photo.filename)
        photo.save(os.path.join(
            app.instance_path, 'photos', photoName
        ))
        user = User(username = form.username.data, firstname = form.firstname.data, lastname = form.lastname.data, date = form.date.data, email = form.email.data, photo= photoName)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # group = Group(name= "Your callendar")
        
        flash('You are now registered')
        return redirect(url_for('login'))

    else:
        return render_template('registration.html', form = form)

@app.route('/logout')
def funcLogout():
    logout_user()
    return redirect(url_for('login'))


#Error page parts

@app.errorhandler(400)
def BadRequest(e):
    return render_template('error/400.html'), 400

@app.errorhandler(401)
def Unauthorized(e):
    return render_template('error/401.html'), 401

@app.errorhandler(403)
def Forbidden(e):
    return render_template('error/403.html'), 403
    
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def InternalServerError(e):
    return render_template('error/500.html'), 500


@app.route('/new_activity', methods=['POST', 'GET'])
@login_required
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


@app.route('/modify_activity/<ID>', methods=['POST', 'GET'])
@login_required
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

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = ModifyForm()
    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():
        print("hi")
        user.firstname= form.firstname.data
        user.lastname= form.lastname.data
        user.date= form.date.data
        user.username= form.username.data
        user.email= form.email.data
        user.set_password(form.password.data)

        db.session.commit()
        flash('informations updated')
        return redirect(url_for('account'))

    else:
        return render_template('account.html', form= form, user = user)

@app.route('/collab/<ID>', methods=['POST', 'GET'])
@login_required
def collab(ID):
    user = User.query.filter_by(idUser=ID).first()
    IDgroups = BelongTo.query.filter_by(idUser=ID).with_entities(BelongTo.idGroup).all
    groups = Group.query.filter_by(idGroup = IDgroups).all()

    form = newGroup()

    if form.validate_on_submit():
        group = Group(Name = form.name.data)
        db.session.add(group)
        # il faut que le form de nouveau groupe renvoie une liste de nouveau invité #
        for idUser in form.invited.data:
            relation = BelongTo(idUser = idUser,idGroup = group)
            db.session.add(relation)
            db.session.commit()
        flash('group created')
        return redirect(url_for('entry'))

    else:
        return render_template('collab.html', form= form, user = user, groups = groups)
app.env="development"
app.run(debug=True)