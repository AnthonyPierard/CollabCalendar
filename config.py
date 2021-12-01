import binascii
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    #Permet de sécuriser le formulaire
    SECRET_KEY = binascii.hexlify(os.urandom(32))
    
    #SQL configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
