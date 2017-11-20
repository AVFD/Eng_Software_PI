from flask import jsonify, request, session
from app import app, db

from app.models.tables import Laboratory, Profession, Permission, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import (DeleteFromDataBase, IsString,
MassiveDeleteFromDataBase, SaveToDataBase, ResponseBadRequest,
ResponseCreated, ResponseConflict, ResponseMethodNotAllowed,
ResponseNotFound, ResponseOk)
from app.controllers.permission import InsertPermission, SearchPermission, UpdatePermission
from app.controllers.securitykey import InsertSecurityKey, SearchSecurityKey, DeleteSecurityKey

import json


@app.route("/user/create", methods=["POST"])
def CreateUser():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "POST": return ResponseMethodNotAllowed()

    insertion_result_list = {}
    data = request.get_json()
    if not data: return ResponseBadRequest()
    if not IsString(data['name']): return ResponseBadRequest()

    #Fazer a inserção da security key. O retorno é um dicionario
    result = InsertSecurityKey(data)
    insertion_result_list["security_key"] = result["state"]
    #Se teve sucesso na inserção da security key ou já existe...
    if insertion_result_list["security_key"] == "fail": return ResponseBadRequest()

    if SearchUser(data=data):
        insertion_result_list["user"] = "exist"
    else:
        sk = SearchSecurityKey(data=data)
        u = CreateUserData(data, sk)
        if u == None: return ResponseNotFound()
        insertion_result_list["user"] = SaveToDataBase(u)

    result = UpdatePermission(data)
    insertion_result_list["allowed_lab_id"] = result["state"]
    if insertion_result_list["user"] == "success": return ResponseCreated()
    elif insertion_result_list["user"] == "exist": return ResponseConflict()


#@app.route("/user/read/<str:profession>", methods=["GET"])
@app.route("/user/read/<int:ident>", methods=["GET"])
@app.route("/user/read", defaults={"ident": None}, methods=["GET"])
def ReadUser(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
        if request.method != "GET": return ResponseMethodNotAllowed()
        output = []
        users = []
        user_data = {}
        arg_profession = request.args.get('profession')
        tab = User
        print("O que é um User?")
        print(type(tab))
        print("Conteúdo dele")
        print(tab.__tablename__)
        #help(tab)

        if ident:
            users.append(User.query.filter_by(id=ident).first())
        
        elif arg_profession:
            users = User.query.filter_by(profession=arg_profession).all()
        
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
            user_data['allowed_lab'] = allowed_labs
            user_data["profession"] = user.profession.value
            output.append(user_data)
            user_data = {}

        return jsonify({'users' : output})#200-OK


@app.route("/user/update", methods=["PUT"])
def UpdateUser():
    #if not 'logged_in' in session: ResponseUnauthorized()
    if request.method != "PUT": return ResponseMethodNotAllowed()
    data = request.get_json()
    if not IsString(data['name']): return ResponseBadRequest()

    #checa se realmente ouve alteração
    if SearchUser(check=data):
        print("Tá tentando atualizar com o mesmo conteúdo")
        return ResponseConflict()

    user_update = SearchUser(ident=data["id"])
    if not user_update: return ResponseBadRequest() 
    user_update.name = data['name']
    user_update.email = data['email']
    user_update.internal_id = data['internal_id']
    user_update.profession = Profession(data['profession']).name

    permissions_delete = SearchPermission(user_data=user_update)
    MassiveDeleteFromDataBase(permissions_delete)
    UpdatePermission(data)
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
    return ResponseOk()


def CreateUserData(data, sk):
    return User(name=data["name"], email=data["email"], internal_id=data["internal_id"], profession=Profession(data["profession"]).name, access_key=sk)


def SearchUser(check=None, data=None, ident=None):
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

    elif check:
        check_user = User.query.filter_by(id=check['id'], name=check['name'], email=check['email'], internal_id=check['internal_id'], profession=Profession(check['profession']).name).first()
        if not check_user:
            print("Atualização com dados distintos")
            return None

        check_user_permissions = SearchPermission(user_data=check_user)
        if len(check_user_permissions) != len(check['allowed_lab_id']):
            print("Só está atualizando a permissão")
            return None

        for permission in check_user_permissions:
            result = permission.laboratory_id in check['allowed_lab_id']
            if result == False:
                return None
        return check_user