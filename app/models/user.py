from flask_login import UserMixin
from __init__ import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = "User"

    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    firstname = db.Column(db.String(80), nullable=False)

    lastname = db.Column(db.String(80), nullable=False)

    date = db.Column(db.Date, nullable=False)

    email = db.Column(db.String(80), nullable=False)

    photo = db.Column(db.String(128))

    password = db.Column(db.String(128))

    UserToGroup = db.relationship('idUser', backref ='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "username = {}".format(self.username)



@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))