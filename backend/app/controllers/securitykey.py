from flask import jsonify, request, session
from app import app, db

from app.models.tables import Laboratory, Profession, Permission, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import SaveToDataBase, DeleteFromDataBase

import json


def CreateSecurityKeyData(data):
    return SecurityKey(security_key=data["security_key"])


def DeleteSecurityKey(target_user_id):
    sk_delete = SearchSecurityKey(ident=target_user_id)
    if not sk_delete: return jsonify({'message': 'Cannot delete this one'})
    DeleteFromDataBase(sk_delete)
    return jsonify({"message": "Security Key deleted successfully"})


def InsertSecurityKey(data):
    new_data = None
    if not data: return {"message": "Failed security key insertion", "state": "fail"}
    if SearchSecurityKey(data=data): return {"message": "Security key alredy exists", "state": "exist"}
    result = SaveToDataBase(CreateSecurityKeyData(data))
    return {"message": "Security key inserted successfully", "state": result}


def SearchSecurityKey(data=None, ident=None):
    if data:
        return SecurityKey.query.filter_by(security_key=data["security_key"]).first()
    elif ident:
        return SecurityKey.query.filter_by(id=ident).first()
