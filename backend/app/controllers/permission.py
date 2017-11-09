from flask import jsonify, request, session
from app import app, db

from app.models.tables import Laboratory, Profession, Permission, SecurityKey
from app.models.forms import LoginForm

from app.controllers.functions import SaveToDataBase
from app.controllers.laboratory import SearchLaboratory

import json


def CreatePermissionData(user_data, laboratory):
    return Permission(member=user_data, place=laboratory)


def InsertPermission(data):
    from app.controllers.user import SearchUser
    flag = 0
    fail_list = []
    user_data = SearchUser(data=data)
    if len(data["permission"]) == 0: return {"message": "No have permissions for insertion", "state": "fail"}
    for lab in data["permission"]:
        laboratory = SearchLaboratory(name=lab)
        if not SearchPermission(data=data, user_data=user_data, laboratory=laboratory):
            SaveToDataBase(CreatePermissionData(user_data, laboratory))
        else:
            flag = 1
            fail_list.append("{}".format(lab))

    if flag == 0: return {"message": "All permissions inserted successfully", "state": "success"}

    message = ""
    for fail in fail_list:
        message = "{0} {1}".format(message, fail)
    message = message[1:]
    return {"message": "Have permissions alredy exists", "state": "exist"}


def UpdatePermission(data):
    from app.controllers.user import SearchUser
    user_data = SearchUser(data=data)
    for lab_id in data['allowed_lab_id']:
        laboratory = SearchLaboratory(ident=lab_id)
        if not SearchPermission(data=data, user_data=user_data, laboratory=laboratory):
            SaveToDataBase(CreatePermissionData(user_data, laboratory))

    return {"message": "All permissions inserted successfully", "state": "success"}


def SearchPermission(data=None, user_data=None, laboratory=None):
    if user_data:
        if laboratory:
            return Permission.query.filter_by(user_id=user_data.id, laboratory_id=laboratory.id).first()
        else:
            return Permission.query.filter_by(user_id=user_data.id).all()
    elif laboratory:
        return Permission.query.filter_by(laboratory_id=laboratory_id).all()

