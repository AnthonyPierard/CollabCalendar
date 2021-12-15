from flask_login import UserMixin

from app import login_manager, db

from werkzeug.security import generate_password_hash, check_password_hash

class BelongTo(db.Model):

    __tablename__ = "Belong to"
    
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    idGroup = db.Column(db.Integer, db.ForeignKey('Group.id'), primary_key=True)

class User(UserMixin, db.Model):

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    firstname = db.Column(db.String(80), nullable=False)

    lastname = db.Column(db.String(80), nullable=False)

    date = db.Column(db.Date, nullable=False)

    email = db.Column(db.String(80), nullable=False)

    photo = db.Column(db.String(128))

    password = db.Column(db.String(128))

    UserToGroup = db.relationship(BelongTo, backref ='user', lazy='dynamic')


    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "username = {}".format(self.username)



@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class Group(db.Model):

    __tablename__ = "Group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Name = db.Column(db.String(80), unique=True, nullable=False)

    GroupToUser = db.relationship(BelongTo, backref ='group', lazy='dynamic')

db.drop_all()
db.create_all()

