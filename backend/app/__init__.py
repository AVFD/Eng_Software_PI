from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
#from flask_login import LoginManager

#Manager é controle de informações que vamos passar na execução
#Migrate

app = Flask(__name__)
#Declaração para receber o arquivo de configuração.
#Com base nesse arquivo, ele vai configurar o app.
#O nome do arquivo é config.py mas não colocamos a
#extenção.
app.config.from_object("config")

db = SQLAlchemy(app)
CORS(app)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

#lm = LoginManager()
#lm.init_app(app)

from app.models import tables, forms
from app.controllers import default
