from datetime import date, datetime
from app.models.user import *
from app.models.activity import *
from app.env import *

from app import db

def setUpDB():

    #creation of default user (admin)
    user = User(username = "123", firstname = "Jean-Pierre", lastname = "Polochon", date=date(1975,7,22), email="JPP@gmail.com", photo = "static/image/JP.jfif")
    user.set_password("admin")
    db.session.add(user)


    persoJPGroup = Group(Name= "Your calendar") #Personnal group of admin user
    TWGroup = Group(Name= "TechnoWeb")
    db.session.add(persoJPGroup)
    db.session.add(TWGroup)
    db.session.commit()

    welcomeNotif = Notification(
        title = welTitle,
        msg = welMsg,
        typeNotif = 0,
        action = None,
        idUser = user.id
    )
    joinNotif = Notification(
        title = "Join my group !",
        msg = welMsg,
        typeNotif = 1,
        action = "/addUserToGroup&idGroup->2",
        idUser = user.id
    )
    db.session.add(welcomeNotif)
    db.session.add(joinNotif)

    JPLink = BelongTo(idUser=user.id,idGroup=persoJPGroup.id)
    db.session.add(JPLink)

    if isAPICalendarTesting:

        #creation of default user (admin)
        userLouis = User(username = "Louis", firstname = "Louis", lastname = "XVI", date=date(1972,7,24), email="LouisXVI@gmail.com", photo = "")
        userLouis.set_password("XVI")
        db.session.add(userLouis)


        persoLouisGroup = Group(Name= "Your calendar") #Personnal group of admin user
        db.session.add(persoLouisGroup)
        db.session.commit()

        LouisLink = BelongTo(idUser=userLouis.id,idGroup=persoLouisGroup.id)
        db.session.add(LouisLink)



        TWLink = BelongTo(idUser=user.id,idGroup=TWGroup.id)
        db.session.add(TWLink)

        task1 = Activity(name = "Étudier", description = "Min: 7h", dateDebut = datetime.fromisoformat("2021-12-20T14:00:00"), idGroup = persoJPGroup.id)
        task2 = Activity(name = "Dormir", description = "Pour quoi faire", dateDebut = datetime.fromisoformat("2021-12-03T15:00:00"), idGroup = persoJPGroup.id)
        db.session.add(task1)
        db.session.add(task2)
        task3 = Activity(name = "Rapport", description = "min: 1000 mots", dateDebut = datetime.fromisoformat("2021-12-26T17:00:00"), idGroup = TWGroup.id)
        db.session.add(task3)

    else:
        #creation of default user (admin)
        userLouis = User(username = "Louis", firstname = "Louis", lastname = "XVI", date=date(1972,7,24), email="LouisXVI@gmail.com", photo = "")
        userLouis.set_password("XVI")
        db.session.add(userLouis)


        persoLouisGroup = Group(Name= "Your calendar") #Personnal group of admin user
        db.session.add(persoLouisGroup)
        db.session.commit()

        LouisLink = BelongTo(idUser=userLouis.id,idGroup=persoLouisGroup.id)
        db.session.add(LouisLink)

    #Push data to the db
    db.session.commit()