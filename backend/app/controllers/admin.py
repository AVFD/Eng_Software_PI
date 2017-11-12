from flask import session, request, jsonify
from flask_login import login_user
from app import app, db
from werkzeug.security import generate_password_hash
from app.models.tables import Admin
from app.models.forms import LoginForm
import json

from app.controllers.functions import (DeleteFromDataBase, IsString, SaveToDataBase, 
ResponseBadRequest, ResponseCreated, ResponseConflict,
ResponseMethodNotAllowed, ResponseNotFound, ResponseOk)


@app.route("/admin/create", methods=["POST"])
def CreateAdmin():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "POST": return ResponseMethodNotAllowed()
    data = request.get_json()
    if not IsString(data['name']): return ResponseBadRequest()
    #criptografar a senha que vem do Json
    hashed_password = generate_password_hash(data['password'], method='sha256')

    #checar se já existe tal usuário no BD, caso não tenha ele inseri
    if SearchAdmin(data=data): return ResponseConflict()
    new_admin = CreateAdminData(data, hashed_password)
    if not new_admin: return ResponseBadRequest()
    SaveToDataBase(new_admin)
    return ResponseCreated()


@app.route("/admin/read/<int:ident>", methods=["GET"])
@app.route("/admin/read", defaults={"ident": None}, methods=["GET"])
def ReadAdmin(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "GET": return ResponseMethodNotAllowed()
    output = []
    admins = []
    if ident:
        admins.append(Admin.query.filter_by(id=ident).first())
    else:
        admins = Admin.query.all()

    if admins[0] == None: return ResponseNotFound()

    for admin in admins:
        admin_data = {}
        admin_data['id'] = admin.id
        admin_data['name'] = admin.name
        admin_data['email'] = admin.email
        output.append(admin_data)

    return jsonify({'admins' : output})#200-OK


@app.route("/admin/update", methods=["PUT"])
def UpdateAdmin():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "PUT": return ResponseMethodNotAllowed()
    data = request.get_json()
    if not IsString(data['name']): return ResponseBadRequest()
    admin_update = SearchAdmin(ident=data["id"])
    if not admin_update: return ResponseBadRequest()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    admin_update.name = data['name']
    admin_update.password = hashed_password
    admin_update.email = data['email']
    db.session.commit()
    return ResponseOk()


@app.route("/admin/delete/<int:ident>", methods=["DELETE"])
def DeleteAdmin(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "DELETE": return ResponseMethodNotAllowed()
    #criar o cara a ser deletado no banco
    if not ident: return ResponseBadRequest()
    admin_delete = SearchAdmin(ident=ident)
    #checar se foi encontrado o admin a ser deletado
    if not admin_delete: return ResponseNotFound()
    if len(Admin.query.all()) == 1: return ResponseMethodNotAcceptable()
    DeleteFromDataBase(admin_delete)
    return ResponseOk()


def CreateAdminData(data, hashed_password):
    return Admin(name=data['name'], login_name=data['login_name'],
                 password=hashed_password, email=data['email'])


def SearchAdmin(data=None, ident=None):
    if data:
        conflict_by_email = Admin.query.filter_by(email=data['email']).first()
        if conflict_by_email: return conflict_by_email
        return Admin.query.filter_by(login_name=data['login_name']).first()

    elif ident:
        return Admin.query.filter_by(id=ident).first()