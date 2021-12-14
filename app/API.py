from datetime import datetime
import json
from app import app
from flask_login import current_user

from app.models.user import User
from app.models.group import BelongTo, Group
from app.models.activity import Activity

from app.env import isAPICalendarTesting


"""
Return a JSON file with all activities of a user
"""
@app.route("/getDataEvent")
def getDataEvent():

    res = []
    """
    res.append({
        "title": "Maintenant",
        "start": datetime.now().isoformat()
    })
    res.append({
        "title": "Maintenant",
        "start": "2022-01-11"
    })

    return json.dumps(res)
    """
    
    #Set curUser
    #curUser = current_user
    curUser = User.query.filter_by(username = "admin").first() if isAPICalendarTesting else current_user
    
    #Find all user's group
    userslink = BelongTo.query.filter_by(idUser = curUser.idUser)

    for link in userslink:

        #Get all group's activity
        groupAct = Activity.query.filter_by(idGroup = link.group.idGroup)

        for act in groupAct:

            #add Event to result
            actReadable = {
                "title": act.name,
                "start": act.dateDebut.isoformat()
            }
            res.append(actReadable)

    return json.dumps(res)
