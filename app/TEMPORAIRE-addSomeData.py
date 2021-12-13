from datetime import datetime
from app.models.user import *
from app.models.activity import *
from app.models.group import *

#Nettoyer la base de données
db.drop_all()
db.create_all()



adminUser = User(username = "admin", firstname = "admin", lastname = "admin",
                date = datetime.strptime("22/11/2021", "%d/%m/%Y").date(),
                email = "admin@collabcalendar.org",
                password = generate_password_hash("admin")
            )

adminGroup = Group(Name= "adminAccount")

adminLink = BelongTo(idUser=0,idGroup=0)

db.session.add(adminGroup)
db.session.add(adminUser)
db.session.add(adminLink)

task1 = Activity(name = "Étudier", dateDebut = datetime.strptime("20/12/2021", "%d/%m/%Y").date(), idGroup = 0)

db.session.add(task1)

db.session.commit()