from app import db
import enum

"""Define as classes que serão transformadas em tabelas pelo Flask-SQLAlchemy.
Observações:

	- Não é necessário criar a função __init__.
	- Não é necessário a função __repr__.
	- Não é necessário usar o __tablename__. O SQLAlchemy nomeará a tabela de
		acordo com o nome da classe. Por padrão, será: transformado em
		minúsculo e/ou com underline.
			+ class name: Admin -> admin
			+ class name: SecurityKey -> security_key
	- A boa prática é colocar nullable = False mesmo sendo chave primária.
	- Adote explícito do que implícito.
	- Desde que uma variável está relacionada com a outra variável que precisa
		adicionar ao banco de dados, pode passar uma só que será adicionada.
	- relationship() serve para criar uma relação entre tabelas para evitar
		que faça pesquisa no banco para pegar valores da outra tabela.

"""

class Profession(enum.Enum):
	zelador = "Zelador(a)"
	professor = "Professor(a)"
	estudante = "Estudante"
	funcionario = "Funcionario"


class DayOfTheWeek(enum.Enum):
	segunda = "Segunda-feira"
	terca = "Terça-feira"
	quarta = "Quarta-feira"
	quinta = "Quinta-feira"
	sexta = "Sexta-feira"
	sabado = "Sábado"
	domingo = "Domingo"


###############################################
"""Tabelas que estarão no Servidor"""
###############################################
class Admin(db.Model):
	#__tablename__ = "admins"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	name = db.Column(db.String(90), nullable = False)
	login_name = db.Column(db.String(45), nullable = False, unique = True)
	password = db.Column(db.String(128), nullable = False)
	email = db.Column(db.String(128), nullable = False, unique = True)

	#def __init__(self, name, login_name, password, email):

	def __repr__(self):
		return "<Admin %r>" % self.name


class SecurityKey(db.Model):
	#__tablename__ = "security_keys"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	security_key = db.Column(db.String(90), nullable = False, unique = True)
	user = db.relationship("User", backref="access_key")


class Laboratory(db.Model):
	#__tablename__ = "laboratories"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	name = db.Column(db.String(20), nullable = False, unique = True)
	permission = db.relationship("Permission", cascade="delete", backref="place", lazy="dynamic")
	schedule = db.relationship("Schedule", cascade="delete", backref="lab_agenda", lazy="dynamic")


class User(db.Model):
	#__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	email = db.Column(db.String(128), nullable = False, unique = True)
	internal_id = db.Column(db.Integer, nullable = True, unique = True)
	security_key_id = db.Column(db.Integer, db.ForeignKey("security_key.id"), nullable = False, unique = True)
	name = db.Column(db.String(90), nullable = False)
	profession = db.Column(db.Enum(Profession), nullable = False)
	permission = db.relationship("Permission", cascade="delete", backref="member", lazy="dynamic")

	#exemplo para delete on cascade:
    #addresses = relationship("Address", cascade="save-update, merge, delete")

class Permission(db.Model):
	#__tablename__ = "permissions"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	laboratory_id = db.Column(db.Integer, db.ForeignKey("laboratory.id"), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

###############################################
"""Tabelas que estarão no Rapsberry"""
###############################################
class AllowedKey(db.Model):
	#__tablename__ = "allowed_keys"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True) 
	allowed_key = db.Column(db.String(90), nullable = False, unique = True)
	profession = db.Column(db.Enum(Profession), nullable = False)
	user_name = db.Column(db.String(90), nullable = False)

	def __repr__(self):
		return "<User %r>" % self.user_name


class Schedule(db.Model):
	#__tablename__ = "schedules"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	start = db.Column(db.Time, nullable = False)
	end = db.Column(db.Time, nullable = False)
	purpouse = db.Column(db.String(45), nullable = False)
	day_of_the_week = db.Column(db.Enum(DayOfTheWeek), nullable = False)
	profession = db.Column(db.Enum(Profession), nullable = False)
	laboratory_id = db.Column(db.Integer, db.ForeignKey("laboratory.id"), nullable = False)


class EventLog(db.Model):
	#__tablename__ = "events_log"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	timestamp = db.Column(db.DateTime, nullable = False)
	event = db.Column(db.String(45), nullable = False)
	allowed_key = db.Column(db.Integer, nullable = False)
	user_name = db.Column(db.String(90), nullable = False)
	profession = db.Column(db.Enum(Profession), nullable = False)
	day_of_the_week = db.Column(db.Enum(DayOfTheWeek), nullable = False)
	laboratory_name = db.Column(db.String(20), nullable = False, unique = True)

db.create_all()
from app.controllers.functions import SaveToDataBase
from app.controllers.user import CreateUserData
from app.controllers.securitykey import InsertSecurityKey, SearchSecurityKey


if len(Admin.query.all()) == 0:
	first_admin = Admin(name="Admin", login_name="admin", password="password", email="admin@email.com.br")
	db.session.add(first_admin)
	db.session.commit()

if len(User.query.all()) == 0:
	data = {"name": "Estudante001", "internal_id": "00000",
			"email": "estudante001@email.com.br", "profession": "estudante",
			"security_key" : "990011223344", "permission" : []}
	InsertSecurityKey(data)
	sk = SearchSecurityKey(data=data)
	SaveToDataBase(CreateUserData(data, sk))