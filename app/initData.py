from datetime import date
from app.models.user import *
from app.models.activity import *
from app.env import *

from app import db

def setUpDB():

    #creation of default user (admin)
    user = User(username = "admin", firstname = "Jean-Pierre", lastname = "Polochon", date=date(1975,7,22), email="JPP@gmail.com", photo = "static/image/JP.jfif")
    user.set_password("admin")
    db.session.add(user)

    #Personnal group of admin user
    persoJPGroup = Group(Name= "Your calendar")
    db.session.add(persoJPGroup)

    #PreCommit to database (use to get id for building BelongTo)
    db.session.commit()

    #Link user to his personnal group
    JPLink = BelongTo(idUser=user.id,idGroup=persoJPGroup.id)
    db.session.add(JPLink)

    #Commit to database
    db.session.commit()
