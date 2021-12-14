from datetime import datetime
from app.models.user import *
from app.models.activity import *
from app.models.group import *
from app.env import isAPICalendarTesting

def setUpDB():
    #Nettoyer la base de données
    db.drop_all()
    db.create_all()



    adminUser = User(username = "admin", firstname = "admin", lastname = "admin",
                    date = datetime.strptime("22/11/2021", "%d/%m/%Y").date(),
                    email = "admin@collabcalendar.org",
                    password = generate_password_hash("admin")
                )
    adminGroup = Group(Name= "adminAccount")

    db.session.add(adminGroup)
    db.session.add(adminUser)

    if isAPICalendarTesting:

        adminLink = BelongTo(idUser=User.query.filter_by(username="admin").first().idUser,idGroup=Group.query.filter_by(Name="adminAccount").first().idGroup)

        db.session.add(adminLink)

        task1 = Activity(name = "Étudier", dateDebut = datetime.strptime("20/12/2021", "%d/%m/%Y").date(), idGroup = Group.query.filter_by(Name="adminAccount").first().idGroup)

        db.session.add(task1)

    db.session.commit()