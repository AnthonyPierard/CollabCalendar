from datetime import datetime, timedelta
import json

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


"""
Pull new data event (when drag&drop)
==========
Parameters:
    Parameters (method: Post)
    id: unique id of the target event/Activity
    newDate: the new start date to push
----------
Return:
    Status of the processus
        failed -> processus failed
        success -> processus succeed
FIXME: add new interval
"""
@app.route("/pullData", methods=['POST'])
def pullData():

    #Get data posted (JSON => keys: id, newDate)
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

"""
Return a JSON file with all group of a user
==========
Parameters:
    No parameter 'cause current_user
----------
Return:
    List of Json data type
    Each element keys:
        name: group name
        idGroup: group id
"""
@app.route("/getUserGroup")
def getUserGroup():

    #Create result data structure
    res = []

    #MOCK
    """
    res.append({
        "name": "Your calendar",
    })
    res.append({
        "name": "Projet web",
    })
    return json.dumps(res)
    """

    #Set curUser
    curUser = User.query.filter_by(username = "123").first() if isAPICalendarTesting else current_user

    #Get user link to get group
    userLinks = BelongTo.query.filter_by(idUser = curUser.id)

    for link in userLinks:

        #Get group name
        groupName = Group.query.filter_by(id = link.idGroup).first().Name

        #Make sure that the first group is the personnal group
        if(groupName == "Your calendar"):

            #Insert the personnal group on first position of the result
            res.insert(0,{
                "name": groupName,
                "idGroup": link.idGroup
            })
        else:

            #Add group in result
            res.append({
                "name": groupName,
                "idGroup": link.idGroup
            })

    #Test message
    if(isAPICalendarTesting):print("Group API:" + str(res))

    return json.dumps(res)

"""
Pull new data event (when drag&drop)
==========
Parameters:
    Parameters (method: Post)
    name: new group name
----------
Return:
    Status of the processus
        failed -> processus failed
        success -> processus succeed
"""
@app.route("/addGroup", methods = ["POST"])
def addGroup():

    #Set curUser
    curUser = User.query.filter_by(username = "123").first() if isAPICalendarTesting else current_user

    #Get data posted (JSON=> keys: name)
    rqst = request.form

    try:

        #Create and commit the new group
        newGroup = Group(Name= rqst["name"])
        db.session.add(newGroup)
        db.session.commit()

        #create link btw user and group
        newLink = BelongTo(idUser = curUser.id, idGroup = newGroup.id)
        db.session.add(newLink)
        db.session.commit()

        return "success"
    except:
        return "failed"


"""
Modify data of a target group
==========
Parameters:
    Parameters (method: Post)
    id: id of the target group
    newName: new name to give to the target group
----------
Return:
    Status of the processus
        failed -> processus failed
        success -> processus succeed
"""
@app.route("/modifyGroup", methods = ["POST"])
def modifyGroup():

    #Get data posted (JSON => keys: id, newName)
    rqst = request.form

    try:

        #Get target group
        targetGroup = Group.query.filter_by(id = int(rqst["id"])).first()

        #Change name of this group and commit it 
        targetGroup.Name = rqst["newName"]
        db.session.add(targetGroup)
        db.session.commit()

        return "success"
    except:
        return "failed"


"""
Add a user to a existant group
==========
Parameters:
    Parameters (method: Post)
    username: username of the target user
    idGroup: id of the target group
----------
Return:
    Status of the processus
        failed -> processus failed
        success -> processus succeed
"""
@app.route("/addUserToGroup", methods = ["POST"])
def addUserToGroup():

    #Get data posted (JSON => keys: username, idGroup)
    rqst = request.form

    try:

        #In case user isn't given, suppose current user (user that accept to join a group)
        if(rqst["username"] == ""):
            targetUser = current_user
        #Get target user
        else:
            targetUser = User.query.filter_by(username= rqst["username"]).first()
        
        #Create link and commit
        newLink = BelongTo(idUser = targetUser.id, idGroup= rqst["idGroup"])
        db.session.add(newLink)
        db.session.commit()

        return "success"
    except:
        return "failed"


#+--------------+
#| Notification |
#+--------------+

"""
Create Joining group notification
==========
Parameters:
    Parameters (method: Post)
    idGroup: idGroup of the group to join
    username: username of the target user
----------
Return:
    Status of the processus
        failed -> processus failed
        success -> processus succeed
"""
@app.route("/notifyUserJoinGroup", methods = ["POST"])
def notifyUser():

    #Get data posted (JSON => keys: username, idGroup)
    rqst = request.form

    #Create new notification
    newNotif = Notification(
        title = str(current_user.username)+" invite you to "+str(Group.query.filter_by(id = rqst["idGroup"]).first().Name),
        msg = "Click on this to join his group.",
        typeNotif = 1,
        action = "/addUserToGroup&idGroup->"+rqst["idGroup"],
        idUser = User.query.filter_by(username = rqst["username"]).first().id
    )

    try:
        #commit notification
        db.session.add(newNotif)
        db.session.commit()

        return "success"
    except:
        return "failed"


"""
Return a JSON file with all notifications of a user
==========
Parameters:
    No parameter 'cause current_user
----------
Return:
    Json data type
    keys:
        new: TODO: is datat new (need to load notification ?)
        notif: Array of JSON
            keys:
                id: id of the notification
                title: title of the notification
                msg: message of the notification
                type: type of notification (0 -> System message; 1 -> Joinning group)
                data: extra data of the notification
"""
@app.route("/checkNotif")
def checkNotif():

    #Create result data structure
    res = {
        "new": True,
        "notif": []
    }

    #MOCK
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

    #Get list of user notifications
    userNotif = Notification.query.filter_by(idUser = current_user.id)

    for notif in userNotif:

        #Add notification to result 
        res["notif"].append({
            "id": notif.id,
            "title": notif.title,
            "msg": notif.msg,
            "type": notif.typeNotif,
            "data": notif.action 
        })
    
    return json.dumps(res)

"""
Delete a notification
==========
Parameters:
    Parameters (method: Post)
    id: id of the target notification
----------
Return:
    Status of the processus
        failed -> processus failed
        success -> processus succeed
"""
@app.route("/delNotif", methods = ["POST"])
def delNotif():

    #Get data posted (JSON => keys: id)
    rqst = request.form

    try:

        #Delete target notification
        targetNotif = Notification.query.filter_by(id = rqst["id"]).first()
        db.session.delete(targetNotif)
        db.session.commit()

        return "success"
    except:
        return "failed"

