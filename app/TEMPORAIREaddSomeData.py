from datetime import datetime
from app.models.user import *
from app.models.activity import *
from app.models.group import *
from app.env import isAPICalendarTesting

def setUpDB():
    #Nettoyer la base de données
    db.drop_all()
    db.create_all()

    #Create admin user
    adminUser = User(username = "admin", firstname = "admin", lastname = "admin",
                    date = datetime.strptime("22/11/2021", "%d/%m/%Y").date(),
                    email = "admin@collabcalendar.org",
                    password = generate_password_hash("admin")
                )
    adminGroup = Group(Name= "Your calendar") #Personnal group of admin user

    #fletch data
    db.session.add(adminGroup)
    db.session.add(adminUser)

    if isAPICalendarTesting:

        adminLink = BelongTo(idUser=User.query.filter_by(username="admin").first().idUser,idGroup=Group.query.filter_by(Name="Your calendar").first().idGroup)

        db.session.add(adminLink)

        task1 = Activity(name = "Étudier", description = "Min: 7h", dateDebut = datetime.fromisoformat("2021-12-20T14:00:00"), idGroup = Group.query.filter_by(Name="Your calendar").first().idGroup)
        task2 = Activity(name = "Dormir", description = "Pour quoi faire", dateDebut = datetime.fromisoformat("2021-12-03T15:00:00"), idGroup = Group.query.filter_by(Name="Your calendar").first().idGroup)

        db.session.add(task1)
        db.session.add(task2)

    #Push data to the db
    db.session.commit()