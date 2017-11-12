from flask import jsonify, request, session
from app import app, db

from app.models.tables import Laboratory, Profession, Permission, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import (SaveToDataBase, DeleteFromDataBase, IsString,
ResponseBadRequest, ResponseCreated, ResponseConflict,
ResponseMethodNotAllowed, ResponseNotFound, ResponseOk)

import json


@app.route("/laboratory/create", methods=["POST"])
def CreateLaboratory():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "POST": return ResponseMethodNotAllowed()
    data = request.get_json()
    if not IsString(data['name']): return ResponseBadRequest()
    if SearchLaboratory(data=data): return ResponseConflict()
    new_lab = Laboratory(name=data['name'])
    if not new_lab: return ResponseBadRequest()
    SaveToDataBase(new_lab)
    return ResponseCreated()


@app.route("/laboratory/read/<int:ident>", methods=["GET"])
@app.route("/laboratory/read", defaults={"ident": None}, methods=["GET"])
def ReadLaboratory(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "GET": return ResponseMethodNotAllowed()
    output = []
    if ident:
        laboratory = Laboratory.query.filter_by(id=ident).first()
        if laboratory:
            laboratory_data = {}
            laboratory_data['id'] = laboratory.id
            laboratory_data['name'] = laboratory.name
            output.append(laboratory_data)
            return jsonify({"laboratory": laboratory_data})
        else: return ResponseNotFound()

    laboratories = Laboratory.query.all()
    for laboratory in laboratories:
        laboratory_data = {}
        laboratory_data['id'] = laboratory.id
        laboratory_data['name'] = laboratory.name
        output.append(laboratory_data)

    return jsonify({'laboratories' : output})


@app.route("/laboratory/update", methods=["PUT"])
def UpdateLaboratory():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "PUT": return ResponseMethodNotAllowed()
    data = request.get_json()
    if not IsString(data['name']): return ResponseBadRequest()
    laboratory_update = SearchLaboratory(ident=data["id"])
    if not laboratory_update: return ResponseConflict()
    laboratory_exist = SearchLaboratory(name=data["name"])
    if laboratory_exist: return ResponseBadRequest()
    laboratory_update.name = data["name"]
    db.session.commit()
    return ResponseOk()


@app.route("/laboratory/delete/<int:ident>", methods=["DELETE"])
def DeleteLaboratory(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "DELETE": return ResponseMethodNotAllowed()
    if not ident: ResponseBadRequest()
    laboratory_delete = SearchLaboratory(ident=ident)
    target_laboratory_id = laboratory_delete.id
    if not laboratory_delete: return ResponseNotFound()
    DeleteFromDataBase(laboratory_delete)
    return ResponseOk()


def SearchLaboratory(data=None, name=None, ident=None):
    if name:
        return Laboratory.query.filter_by(name=name).first()
    elif ident:
        return Laboratory.query.filter_by(id=ident).first()
    elif data:
        return Laboratory.query.filter_by(name=data["name"]).first()