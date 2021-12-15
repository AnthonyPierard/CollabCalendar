from app import db

class Group(db.Model):

    __tablename__ = "Group"

    idGroup = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(80), unique=True, nullable=False)


    def __repr__(self):
        return "Group = {}".format(self.Name)
    GroupToUser = db.relationship('BelongTo', backref ='author', lazy='dynamic')



class BelongTo(db.Model):

    __tablename__ = "Belong to"
    
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'), primary_key=True)

    def __repr__(self):
        return "Link btw user: {} <-> group: {}".format(self.user.username,self.group.Name)

    idGroup = db.Column(db.Integer, db.ForeignKey('Group.idGroup'), primary_key=True)
