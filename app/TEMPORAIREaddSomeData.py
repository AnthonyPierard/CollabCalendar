from datetime import date, datetime
from app.models.user import *
from app.models.activity import *
from app.env import isAPICalendarTesting

from app import db

def setUpDB():

    #creation of default user (admin)
    user = User(username = "123", firstname = "Jean-Pierre", lastname = "Polochon", date=date(1975,7,22), email="JPP@gmail.com", photo = "app/static/image/JP.jfif")
    user.set_password("admin")
    db.session.add(user)


    persoJPGroup = Group(Name= "Your calendar") #Personnal group of admin user
    db.session.add(persoJPGroup)
    db.session.commit()

    JPLink = BelongTo(idUser=User.query.filter_by(username="123").first().id,idGroup=Group.query.filter_by(Name="Your calendar").first().id)
    db.session.add(JPLink)

    if isAPICalendarTesting:

        TWGroup = Group(Name= "Techno Web")
        db.session.add(TWGroup)

        db.session.commit()

        TWLink = BelongTo(idUser=user.id,idGroup=TWGroup.id)
        db.session.add(TWLink)


        task1 = Activity(name = "Étudier", description = "Min: 7h", dateDebut = datetime.fromisoformat("2021-12-20T14:00:00"), idGroup = Group.query.filter_by(Name="Your calendar").first().id)
        task2 = Activity(name = "Dormir", description = "Pour quoi faire", dateDebut = datetime.fromisoformat("2021-12-03T15:00:00"), idGroup = Group.query.filter_by(Name="Your calendar").first().id)
        db.session.add(task1)
        db.session.add(task2)

    #Push data to the db
    db.session.commit()