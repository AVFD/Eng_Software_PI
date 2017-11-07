from flask import jsonify, request, session
from app import app, db

from app.models.tables import Laboratory, Profession, Permission, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import SaveToDataBase, DeleteFromDataBase, MassiveDeleteFromDataBase
from app.controllers.functions import ResponseBadRequest, ResponseCreated, ResponseGone, ResponseConflict
from app.controllers.functions import ResponseMethodNotAllowed, ResponseNotFound#, ResponseOk
from app.controllers.permission import InsertPermission, SearchPermission
from app.controllers.securitykey import InsertSecurityKey, SearchSecurityKey

import json


@app.route("/user/create", methods=["POST"])
def CreateUser():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "POST": return ResponseMethodNotAllowed()

    insertion_result_list = {}
    data = request.get_json()
    if not data: return ResponseBadRequest()

    #Fazer a inserção da security key. O retorno é um dicionario
    result = InsertSecurityKey(data)
    insertion_result_list["security_key"] = result["state"]
    #Se teve sucesso na inserção da security key ou já existe...
    if insertion_result_list["security_key"] == "fail": return ResponseBadRequest()

    if SearchUser(data=data):
        insertion_result_list["user"] = "exist"
    else:
        sk = SearchSecurityKey(data=data)
        insertion_result_list["user"] = SaveToDataBase(CreateUserData(data, sk))

    result = InsertPermission(data)
    insertion_result_list["permission"] = result["state"]
    if insertion_result_list["user"] == "success": return ResponseCreated()
    elif insertion_result_list["user"] == "exist": return ResponseConflict()


@app.route("/user/read/<int:ident>", methods=["GET"])
@app.route("/user/read", defaults={"ident": None}, methods=["GET"])
def ReadUser(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
        if request.method != "GET": return ResponseMethodNotAllowed()
        output = []
        users = []
        user_data = {}
        if ident:
            users.append(User.query.filter_by(id=ident).first())
        else:
            users = User.query.all()
            
        if users[0] == None: return ResponseNotFound()

        for user in users:
            permissions = Permission.query.filter_by(user_id=user.id).all()
            allowed_labs = []
            for permission in permissions:
                laboratory = Laboratory.query.filter_by(id=permission.laboratory_id).first()
                allowed_labs.append({"laboratory_id": laboratory.id, "laboratory_name": laboratory.name})

            sk = SearchSecurityKey(ident=user.security_key_id)
            user_data['email'] = user.email
            user_data['security_key'] = sk.security_key
            user_data['internal_id'] = user.internal_id
            user_data['name'] = user.name
            user_data['id'] = user.id
            user_data['permission'] = allowed_labs
            user_data["profession"] = user.profession.value
            output.append(user_data)
            user_data = {}

        return jsonify({'users' : output})#200-OK


@app.route("/user/update", methods=["PUT"])
def UpdateUser():
    from app.controllers.functions import ResponseOk
    #if not 'logged_in' in session: ResponseUnauthorized()
    if request.method != "PUT": return ResponseMethodNotAllowed()
    data = request.get_json()
    user_update = SearchUser(ident=data["id"])
    if not user_update: return ResponseBadRequest() 
    user_update.name = data['name']
    user_update.email = data['email']
    user_update.internal_id = data['internal_id']
    user_update.profession = data['profession']
    print("Valor do data[profession]: {0}\nTIpo da variável: {1}".format(data['profession'], type(data['profession'])))
    if user_update.profession == Profession.estudante:
        user_data["profession"] = "Estudante"
    permissions_delete = SearchPermission(user_data=user_update)
    MassiveDeleteFromDataBase(permissions_delete)
    InsertPermission(data)
    db.session.commit()
    return ResponseOk()


@app.route("/user/delete/<int:ident>", methods=["DELETE"])
def DeleteUser(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "DELETE": return ResponseMethodNotAllowed()
    if not ident: return ResponseBadRequest()
    user_delete = SearchUser(ident=ident)
    if not user_delete: return ResponseNotFound()
    target_user_id = user_delete.id
    DeleteFromDataBase(user_delete)
    result = DeleteSecurityKey(target_user_id)
    return ResponseGone()


def CreateUserData(data, sk):
    return User(name=data["name"], email=data["email"], internal_id=data["internal_id"],
                profession=Profession(data["profession"]).name, access_key=sk)


def SearchUser(data=None, ident=None):
    if data:
        conflict_by_email = User.query.filter_by(email=data["email"]).first()
        if conflict_by_email: return conflict_by_email
        
        conflict_by_internal_id = User.query.filter_by(internal_id=data["internal_id"]).first()
        if conflict_by_internal_id: return conflict_by_internal_id
        
        #conflict by security key id
        sk = SearchSecurityKey(data=data)
        return User.query.filter_by(access_key=sk).first()

    elif ident:
        return User.query.filter_by(id=ident).first() 