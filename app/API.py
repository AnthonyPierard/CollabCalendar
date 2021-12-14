from datetime import datetime, timedelta
import json
from app import app, db
from flask_login import current_user
from flask import request

from app.models.user import User
from app.models.group import BelongTo, Group
from app.models.activity import Activity

from app.env import isAPICalendarTesting


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
    curUser = User.query.filter_by(username = "admin").first() if isAPICalendarTesting else current_user
    
    #Find all user's group
    userslink = BelongTo.query.filter_by(user = curUser)

    for link in userslink:

        #Get all group's activity
        groupAct = Activity.query.filter_by(group = link.group)

        for act in groupAct:
            endDate: datetime = act.dateDebut + timedelta(hours = act.interval)#endDate = StartDate + interval
            #Check if the activity is in the request interval
            if (act.dateDebut >= rqstStartdate and endDate <= rqstEnddate):

                #add Event to result
                actReadable = {
                    "id": act.id,
                    "title": act.name,
                    "start": act.dateDebut.isoformat(),
                    "end": endDate.isoformat(),
                    "display": "block",
                    "backgroundColor": "#5dade2",
                    "borderColor": "#aed6f1"
                }
                res.append(actReadable)

    if(isAPICalendarTesting):print(res)

    return json.dumps(res)



@app.route("/pullData", methods=['POST'])
def pullData():

    #Get data posted (JSON)
    rqst = request.form

    #Get target activity
    trgtAct = Activity.query.filter_by(id=rqst["id"]).first()

    #Set new value
    trgtAct.dateDebut = datetime.fromisoformat(rqst["newDate"][:19])

    #Push change
    db.session.add(trgtAct)
    db.session.commit()
    
    return "success"