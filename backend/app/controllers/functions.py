from flask import Response, session
from app import db

#################################################################
############### FUNCOES - Ordem Alfabetica ######################
#################################################################
def MassiveDeleteFromDataBase(datas):
    if len(datas) == 0: return "empty"
    [DeleteFromDataBase(data) for data in datas]
    return "success"


def DeleteFromDataBase(data):
    db.session.delete(data)
    db.session.commit()
    return "success"
    

def SaveToDataBase(new_data):
    db.session.add(new_data)
    db.session.commit()
    return "success"


#################################################################
#### FUNCOES PARA RETORNO DAS RESPOSTAS - Ordem Numerica ########
#################################################################
def ResponseContinue():
    return Response(None, status=100, mimetype="")

def ResponseOk():
    return Response(None, status=200, mimetype="")

def ResponseCreated():
    return Response(None, status=201, mimetype="")

def ResponseAccepted():
    return Response(None, status=202, mimetype="")

def ResponseNoContent():
    return Response(None, status=204, mimetype="")

def ResponseFound():
    return Response(None, status=302, mimetype="")

def ResponseNotModified():
    return Response(None, status=304, mimetype="")

def ResponseBadRequest():
    return Response(None, status=400, mimetype="")

def ResponseUnauthorized():
    return Response(None, status=401, mimetype="")

def ResponseNotFound():
    return Response(None, status=404, mimetype="")

def ResponseMethodNotAllowed():
    return Response(None, status=405, mimetype="")

def ResponseMethodNotAcceptable():
    return Response(None, status=406, mimetype="")

def ResponseConflict():
    return Response(None, status=409, mimetype="")

def ResponseGone():
    return Response(None, status=410, mimetype="")