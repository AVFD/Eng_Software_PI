from flask import jsonify, request, session
from app import app, db

from app.models.tables import DayOfTheWeek, Event, EventLog, Laboratory, Profession, Permission, Schedule, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import (SaveToDataBase, DeleteFromDataBase,
ResponseBadRequest, ResponseCreated, ResponseConflict,
ResponseMethodNotAllowed, ResponseNotFound, ResponseOk)

import json
import datetime


@app.route("/event_log/create", methods=["POST"])
def CreateEventLog():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    errors = []
    count = 1

    if request.method != "POST": return ResponseMethodNotAllowed()
    datas = request.get_json()

    for data in datas['events']:
        if SearchEventLog(data_for_one=data):
            errors.append(RegisterError("exist", count))
            count+=1
            continue

        new_event_log = CreateEventLogData(data)
        if not new_event_log: 
            errors.append(RegisterError("not created"), count)
            count+=1
            continue
        SaveToDataBase(new_event_log)
    
    for error in errors:
        print(error)

    return ResponseCreated()


@app.route("/event_log/read/<int:ident>", methods=["GET"])
@app.route("/event_log/read", defaults={"ident": None}, methods=["GET"])
def ReadEventLog(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "GET": return ResponseMethodNotAllowed()
    output = []
    event_logs = []
    if ident:
        event_logs.append(EventLog.query.filter_by(id=ident).first())
    else:
        event_logs = EventLog.query.all()
    
    if event_logs[0] == None: return ResponseNotFound()

    for event_log in event_logs:
        event_log_data = {}
        event_log_data['id'] = event_log.id
        event_log_data['timestamp'] = event_log.timestamp.__str__()
        event_log_data['event'] = event_log.event.value
        event_log_data['security_key'] = event_log.security_key
        event_log_data['user_name'] = event_log.user_name
        event_log_data['profession'] = event_log.profession.value
        event_log_data['day_of_the_week'] = event_log.day_of_the_week.value
        event_log_data['laboratory_name'] = event_log.laboratory_name
        output.append(event_log_data)
    
    return jsonify({"event_logs": output})


@app.route("/event_log/delete/<int:ident>", methods=["DELETE"])
def DeleteEventLog(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "DELETE": return ResponseMethodNotAllowed()
    if not ident: ResponseBadRequest()
    event_log_delete = SearchSchedule(ident=ident)
    if not event_log_delete: return ResponseNotFound()
    DeleteFromDataBase(event_log_delete)
    return ResponseOk()


def CreateEventLogData(data):
    time = datetime.datetime.strptime(data['timestamp'], "%d-%m-%Y %H:%M:%S")
    return EventLog(timestamp=time, event=data['event'], security_key=data['security_key'],
                    user_name=data['user_name'], day_of_the_week=data['day_of_the_week'], profession=data['profession'],
                    laboratory_name=data['laboratory_name'])


def RegisterError(cause, count):
    return {"event number": count, "error type": cause}


def SearchEventLog(data_for_one=None, ident=None, data_for_various=None):
    if ident:
        return Schedule.query.filter_by(id=ident).first()

    elif data_for_one:
        return Schedule.query.filter_by(start=data_for_one['timestamp'], day_of_the_week=data_for_one['day_of_the_week'], laboratory_id=data_for_one['laboratory_name']).first()

    elif data_for_various:
        return Schedule.query.filter_by(laboratory_id=data_for_various['laboratory_name'], day_of_the_week=data_for_various['day_of_the_week']).all()
