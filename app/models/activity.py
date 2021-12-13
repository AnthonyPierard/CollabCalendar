from app import db

class Activity(db.Model):

    __tablename__ = "Activity"

    idTask = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    name = db.Column(db.String(128), nullable=False)

    status = db.Column(db.Boolean, default = False)

    description = db.Column(db.String(400))

    dateDebut = db.Column(db.Date)

    interval = db.Column(db.Date)

    #Ajout si pas corrigé
    idGroup = db.Column(db.Integer, db.ForeignKey('Group.idGroup'), nullable=False)

