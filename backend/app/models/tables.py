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
	name = db.Column(db.String(20), nullable = False)
	permission = db.relationship("Permission", cascade="delete", backref="place", lazy="dynamic")

class User(db.Model):
	#__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	email = db.Column(db.String(128), nullable = False, unique = True)
	internal_id = db.Column(db.Integer)
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
	allowed_key = db.Column(db.String(90), nullable = False)
	profession = db.Column(db.Enum(Profession), nullable = False)
	event_log = db.relationship("EventLog", backref="permission_key")


	def __repr__(self):
		return "<User %r>" % self.user_name


class Schedule(db.Model):
	#__tablename__ = "schedules"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	start = db.Column(db.DateTime, nullable = False)
	end = db.Column(db.DateTime, nullable = False)
	purpouse = db.Column(db.String(45), nullable = False)
	i_can_enter = db.Column(db.Boolean, nullable = False)
	weeks_day = db.Column(db.String(45), nullable = False)


class EventLog(db.Model):
	#__tablename__ = "events_log"

	id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
	timestamp = db.Column(db.DateTime, nullable = False)
	event = db.Column(db.String(45), nullable = False)
	allowed_key_id = db.Column(db.Integer, db.ForeignKey("allowed_key.id"), nullable = False)

db.create_all()
"""
	@property
	def is_authenticated(self):
		return True


	@property
	def is_active(self):
		return True


	@property
	def is_anonymous(self):
		return False


	@property
	def get_id(self):
		return str(self.id)
"""