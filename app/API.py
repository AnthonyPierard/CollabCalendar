from datetime import datetime
import json
from app import app
from flask_login import current_user

from app.models.user import User
from app.models.group import BelongTo, Group
from app.models.activity import Activity


"""
Return a JSON file with all activities of a user
"""
@app.route("/getDataEvent")
def getDataEvent():

    res = []

    res.append({
        "title": "Dormir",
        "start": datetime.now().isoformat()
    })

    return json.dumps(res)

    
    #Set curUser
    #curUser = current_user
    curUser = User.query.filter_by(username = "admin").first() #TODO: change curuser

    #Find all user's group
    userslink = BelongTo.query.filter_by(idUser = curUser.idUser)

    for link in userslink:

        #Get curGroup
        curGroup = Group.query.filter_by(idGroup = link.idGroup)

        #Get all group's activity
        groupAct = Activity.query.filter_by(idGroup = curGroup.idGroup)

        for act in groupAct:
            actReadable = {
                "title": act.name,
                "start": act.date.isoformat()
            }
            res.append(actReadable)
    
    print(res)
