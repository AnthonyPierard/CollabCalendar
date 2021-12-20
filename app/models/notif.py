from app import db

class Notification(db.Model):

    __tablename__ = "Notification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.String(128), nullable=False)
    msg = db.Column(db.String(128), nullable=True)
    # 0-> System; 1-> Group invite; 
    typeNotif = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(128), nullable=True)

    idUser = db.Column(db.Integer, db.ForeignKey('User.id'))