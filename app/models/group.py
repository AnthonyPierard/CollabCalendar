from app import db

class Group(db.Model):

    __tablename__ = "Group"

    idGroup = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Name = db.Column(db.String(80), unique=True, nullable=False)

    GroupToUser = db.relationship('idGroup', backref ='author', lazy='dynamic')


class BelongTo(db.Model):

    __tablename__ = "Belong to"
    
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'))

    idGroup = db.Column(db.Integer, db.ForeignKey('User.idGroup'))