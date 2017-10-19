import os
#basedir = os.path.abspath(os.path.dirname(__file__))

#Recebe alerta de debugs. Ele também reinicia automaticamente
#quando houver uma modificação no código.
DEBUG = True

#Configuração para conectar no banco de dados
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/PI'

#Faz a warning parar de acontecer
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.urandom(12)