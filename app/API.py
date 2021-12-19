from datetime import datetime, timedelta
import json

from flask_login.utils import login_required
from app import app, db
from flask_login import current_user
from flask import request

from app.models.user import *
from app.models.activity import Activity

from app.env import isAPICalendarTesting


#+----------------+
#| Event provider |
#+----------------+

"""
Return a JSON file with all activities of a user
==========
Parameters:
    Parameters url (method: Get)
    start: iso format of the first date of the request interval [include]
    end: iso format of the last date of the request interval [include]
----------
Return:
    List of Json data type
    Each element keys:
        title: activity name
        start: iso format of the starting date
        end: iso format of the ending date
        display: How the activity is display (see fullCalendar Doc)
        backgroundColor: Color of the activity's block background
        borderColor: Color of the activity's block barder
"""
@app.route("/getDataEvent")
def getDataEvent():

    rqstStartdate = datetime.fromisoformat(request.args['start']).replace(tzinfo=None)
    rqstEnddate = datetime.fromisoformat(request.args['end']).replace(tzinfo=None)
    res = []
    
    #Set curUser
    curUser = User.query.filter_by(username = "123").first() if isAPICalendarTesting else current_user
    
    #Find all user's group
    userslink = BelongTo.query.filter_by(idUser = curUser.id)

    first = True

    for link in userslink:

        #Get all group's activity
        groupAct = Activity.query.filter_by(idGroup = link.idGroup)

        for act in groupAct:
            endDate: datetime = act.dateDebut + timedelta(hours = act.interval)#endDate = StartDate + interval
            #Check if the activity is in the request interval
            if (act.dateDebut >= rqstStartdate and endDate <= rqstEnddate):

                #add Event to result
                actReadable = {
                    "id": act.id,
                    "className":"eventGroup"+str(link.idGroup), # + ("" if(not first) else " unDisplayEvent")
                    "title": act.name,
                    "summary": act.description,
                    "start": act.dateDebut.isoformat(),
                    "end": endDate.isoformat(),
                    "display": "block",
                    "backgroundColor": "#5dade2",
                    "borderColor": "#aed6f1"
                }
                res.append(actReadable)

    if(isAPICalendarTesting):print(res)
    if first: first = False

    return json.dumps(res)



@app.route("/pullData", methods=['POST'])
def pullData():

    #Get data posted (JSON)
    rqst = request.form

    try:
        #Get target activity
        trgtAct = Activity.query.filter_by(id=rqst["id"]).first()

        #Set new value
        trgtAct.dateDebut = datetime.fromisoformat(rqst["newDate"][:19])+timedelta(hours=1)

        #Push change
        db.session.add(trgtAct)
        db.session.commit()
        
        return "success"
    except:
        return "failed"

#+----------------+
#| group provider |
#+----------------+

@app.route("/getUserGroup")
def getUserGroup():

    res = []
    """
    res.append({
        "name": "Your calendar",
    })
    res.append({
        "name": "Projet web",
    })
    """

    #return json.dumps(res)

    #Set curUser
    curUser = User.query.filter_by(username = "123").first() if isAPICalendarTesting else current_user

    #Get user link to get group
    userLinks = BelongTo.query.filter_by(idUser = curUser.id)

    for link in userLinks:

        groupName = Group.query.filter_by(id = link.idGroup).first().Name

        if(groupName == "Your calendar"):
            res.insert(0,{
                "name": groupName,
                "idGroup": link.idGroup
            })
        else:
            res.append({
                "name": groupName,
                "idGroup": link.idGroup
            })

    if(isAPICalendarTesting):print("Group API:" + str(res))
    return json.dumps(res)


@app.route("/addGroup", methods = ["POST"])
def addGroup():

    #Set curUser
    curUser = User.query.filter_by(username = "123").first() if isAPICalendarTesting else current_user
    rqst = request.form

    try:
        newGroup = Group(Name= rqst["name"])
        db.session.add(newGroup)
        db.session.commit()

        newLink = BelongTo(idUser = curUser.id, idGroup = newGroup.id)
        db.session.add(newLink)
        db.session.commit()

        return "success"
    except:
        return "failed"


@app.route("/modifyGroup", methods = ["POST"])
def modifyGroup():


    rqst = request.form
    #print("Target Group: "+ rqst["id"])


    try:
        targetGroup = Group.query.filter_by(id = int(rqst["id"])).first()

        targetGroup.Name = rqst["newName"]

        db.session.add(targetGroup)
        db.session.commit()

        return "success"
    except:
        return "failed"


@app.route("/addUserToGroup", methods = ["POST"])
def addUserToGroup():

    rqst = request.form

    try:
        if(rqst["username"] == ""):
            targetUser = current_user
        else:
            targetUser = User.query.filter_by(username= rqst["username"]).first()
        newLink = BelongTo(idUser = targetUser.id, idGroup= rqst["idGroup"])

        db.session.add(newLink)
        db.session.commit()

        return "success"
    except:
        return "failed"


@app.route("/notifyUserJoinGroup", methods = ["POST"])
def notifyUser():

    #Get request
    #JSON => keys: username, idGroup
    rqst = request.form

    newNotif = Notification(
        title = str(current_user.username)+" invite you to "+str(Group.query.filter_by(id = rqst["idGroup"]).first().Name),
        msg = "Click on this to join his group.",
        typeNotif = 1,
        action = "/addUserToGroup&idGroup->"+rqst["idGroup"],
        idUser = User.query.filter_by(username = rqst["username"]).first().id
    )

    try:
        db.session.add(newNotif)
        db.session.commit()

        return "success"
    except:
        return "failed"


@app.route("/checkNotif")
@login_required
def checkNotif():



    res = {
        "new": True,
        "notif": []
    }
    """
    res["notif"].append({
        "id": 1,
        "title": "Welcome",
        "msg": "The whole team welcome you to CollabCalendar !",
        "type": 0,
        "data": None
    })
    res["notif"].append({
        "id": 2,
        "title": "Noe",
        "msg": "Pozza",
        "type": 1,
        "data": "/addUserToGroup&idGroup->2"
    })
    """

    userNotif = Notification.query.filter_by(idUser = current_user.id)

    for notif in userNotif:

        res["notif"].append({
            "id": notif.id,
            "title": notif.title,
            "msg": notif.msg,
            "type": notif.typeNotif,
            "data": notif.action 
        })
    
    return json.dumps(res)

@app.route("/delNotif", methods = ["POST"])
def delNotif():

    rqst = request.form

    try:
        targetNotif = Notification.query.filter_by(id = rqst["id"]).first()
        db.session.delete(targetNotif)
        db.session.commit()
        return "success"
    except:
        return "failed"

