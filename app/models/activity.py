from app import db
from app.env import defaudTimeOfActivity

class Activity(db.Model):

    __tablename__ = "Activity"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    name = db.Column(db.String(128), nullable=False)

    status = db.Column(db.Boolean, default = False)

    description = db.Column(db.String(400))

    dateDebut = db.Column(db.DateTime, nullable=False)

    #Interval est le nombre d'heure attribuer à l'activité
    interval = db.Column(db.Integer, default = defaudTimeOfActivity)

    #Ajout si pas corrigé
    idGroup = db.Column(db.Integer, db.ForeignKey('Group.id'), nullable=False)

    group = db.relationship('Group', backref ='authorGroup', lazy=True)

    def __repr__(self):
        return "Activity {} for group {}".format(self.name,self.group.Name)

