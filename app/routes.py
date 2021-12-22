#All importation

from threading import active_count
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from flask.helpers import flash
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import date, datetime
from flask import jsonify
import os

#Importation of App and db
from app import app, db
from app import login_manager

#Importation of the form
from app.forms.form_user import LoginForm, RegistrationForm
from app.forms.form_activity import ActivityForm
from app.forms.form_group import newGroup

#Importation of the models
from app.models.user import *
from app.models.activity import Activity

#import env
from app.env import *


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
    activity = Activity.query.filter_by(idGroup='Your calendar').all()
    print(activity)
    user = User.query.filter_by(id=current_user.id).first()

    #Render test template
    return render_template("homepage.html",tasklist=activity, user = user)








#Login and registration parts
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('entry', _user=form.username.data))
    
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
        basedir = os.path.abspath(os.path.dirname(__file__))
        
        photo.save(os.path.join(
            basedir, 'static', 'image', photoName
        ))
        path_to_name = "static/image/" + photoName
        user = User(username = form.username.data, firstname = form.firstname.data, lastname = form.lastname.data, date = form.date.data, email = form.email.data, photo= path_to_name)
        user.set_password(form.password.data)
        db.session.add(user)
        
        group = Group(Name= "Your Callendar")
        db.session.add(group)
        db.session.commit()
        userLink = BelongTo(idUser=User.query.filter_by(username=form.username.data).first().id,idGroup=Group.query.filter_by(id= group.id).first().id)
        db.session.add(userLink)
        db.session.commit()

        welcomeNotif = Notification(
            title = welTitle,
            msg = welMsg,
            typeNotif = 0,
            action = None,
            idUser = user.id
        )
        db.session.add(welcomeNotif)
        db.session.commit()

        
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
def new_activity():

    # reçoit les données à partir de loadNewEvent.js
    taskname = request.form['name']
    taskdescription = request.form['description']
    taskDateBegin = datetime.fromisoformat(request.form['dateBegin'])
    taskinterval = request.form['interval']
    taskGroup = Group.query.filter_by(id = request.form['idGroup']).first().id


    if taskname!='' and taskDateBegin and taskGroup:
        
        activity = Activity(name = taskname, description= taskdescription,
        dateDebut= taskDateBegin, interval=taskinterval, idGroup = taskGroup)

        db.session.add(activity)
        db.session.commit()
        flash('New activity created')
        return jsonify({'name' : taskname})
        # return redirect(url_for('entry'))
    
    return redirect(url_for('entry'))





@app.route('/remove_activity', methods=['POST', 'GET'])
def remove_activity():

    idtask = int( request.form['id'] )

    try :
        # 1. retrouver l'id de la tache
        activity = Activity.query.filter_by(id=idtask).first()

        # 2. supprimer la tache de la BD avec son id
        # If task is in the task list, delete it and update the database
        if activity:
            db.session.delete(activity)
            db.session.commit()

        flash('the task does not exist', 'warning')
        # # Get the list of tasks of the current user
        # list = Activity.query.filter_by(user_id=current_user.id).all()

        return "succes"

    except:
        return "return"






@app.route('/modify_activity', methods=['POST', 'GET'])
@login_required
def modify_activity():

    # reçoit les données à partir de loadNewEvent.js
    taskid = request.form['taskid']
    taskname = request.form['name']
    taskdescription = request.form['description']
    taskDateBegin = datetime.fromisoformat(request.form['dateBegin'])
    taskinterval = request.form['interval']

    print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(taskdescription)
    print(taskname)
    print(taskDateBegin)
    print(taskinterval)
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++')



    activity = Activity.query.filter_by(id=int(taskid)).first()
    
    activity.name= taskname
    activity.description = taskdescription
    activity.dateDebut = taskDateBegin
    activity.interval = taskinterval
    
    db.session.add(activity)
    db.session.commit()
    flash('New activity created')
    return jsonify({'name' : taskname})


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    user = User.query.filter_by(id=current_user.id).first()
    
    # if form.validate_on_submit():
    #     print("hello")
    #     print(form.lastname.data)
    #     user.firstname= form.firstname.data
    #     user.lastname= form.lastname.data
    #     user.date= form.date.data
    #     user.username= form.username.data
    #     user.email= form.email.data
    #     user.set_password(form.password.data)

    #     db.session.commit()
    #     flash('informations updated')
    #     return redirect(url_for('entry'))

    return render_template('account.html', user = user)

@app.route('/modifyAccount', methods=['POST'])
# @login_required
def modifyAccount():

    rqst = request.form
    try :
        user = User.query.filter_by(id=int(rqst["id"])).first()
        action = rqst["action"]
        value = rqst["value"]
        if action=="1":
            user.firstname = value
        
        elif action=="2":
            user.lastname = value

        elif action=="4":
            user.username = value
        
        elif action=="5":
            user.email = value

        db.session.add(user)
        db.session.commit()
        return "success"
    except:
        return "failed"

    

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