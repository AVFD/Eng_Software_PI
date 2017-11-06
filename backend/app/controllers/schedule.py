from flask import jsonify, request, session
from app import app, db

from app.models.tables import DayOfTheWeek, Laboratory, Profession, Permission, Schedule, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import (SaveToDataBase, DeleteFromDataBase,
ResponseBadRequest, ResponseCreated, ResponseGone, ResponseConflict,
ResponseMethodNotAllowed, ResponseNotFound)
from app.controllers.laboratory import SearchLaboratory
import json
import datetime

@app.route("/schedule/create", methods=["POST"])
def CreateSchedule():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "POST": return ResponseMethodNotAllowed()
    data = request.get_json()
    if SearchSchedule(data_for_one=data): return ResponseConflict()
    lab = SearchLaboratory(ident=data['laboratory id'])
    if not lab: return ResponseNotFound()
    new_schedule = CreateScheduleData(data, lab)
    if not new_schedule: return ResponseBadRequest()
    SaveToDataBase(new_schedule)
    return ResponseCreated()


@app.route("/schedule/read/<int:ident>", methods=["GET"])
@app.route("/schedule/read", defaults={"ident": None}, methods=["GET"])
def ReadSchedule(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "GET": return ResponseMethodNotAllowed()
    output = []
    schedules = []
    if ident:
        schedules.append(Schedule.query.filter_by(id=ident).first())
    else:
        schedules = Schedule.query.all()
    
    if schedules[0] == None: return ResponseNotFound()
    count=0
    print("SCHEDULES")
    print(schedules)
    print("Tamanho da Schedules")
    print(len(schedules))
    print("TIpo da schedules")
    print(type(schedules))
    for schedule in schedules:
        print("CONTADOR: {}".format(count))
        schedule_data = {}
        schedule_data['id'] = schedule.id
        schedule_data['start'] = schedule.start
        schedule_data['end'] = schedule.end
        schedule_data['purpouse'] = schedule.purpouse
        schedule_data['day of the week'] = schedule.day_of_the_week.value
        schedule_data['profession'] = schedule.profession.value
        schedule_data['laboratory id'] = schedule.laboratory_id

        print("O QUE TEM NO SCHEDULE_DATA")
        print(schedule_data)

        print("SOBRE AS DATAS")
        print(schedule.start.value)
        print("Tipo dela")
        print(type(schedule.start))
        print("tamanho")
        print(len(schedule.start))
        output.append(schedule_data)
    
    print("Karamatte hanashite mogake!  ")
    
    return jsonify({"schedules": output})


def CanInsertNewData(data):
    schedules = SearchSchedule(data_for_various=data)
    #Schedule nova
    for schedule in schedules:
        tempo = schedule.start - data['start']
        print("Tempo: {}".format())
        if schedule.start - data['start'] >= 0:
            if schedule.start < data['end']:
                return False
        else:
            if schedule.end > data['start']:
                return False


def CanUpdateSchedule(data):
    schedules = SearchSchedule(data_for_various=data)
    current_schedule = SearchSchedule(ident=data['id'])
    for schedule in schedules:
        tempo = schedule.start - current_schedule.start
        print("Tempo: {}".format())
        if tempo >= 0:
            if schedule.start < current_schedule.end:
                return False
        else:
            if schedule.end > current_schedule.start:
                return False

    return True
"""
    day_of_the_week = db.execute('SELECT DAYOFWEEK(NOW())')
    print(type(day_of_the_week))
    print(day_of_the_week)
    day_of_the_week
"""

@app.route("/schedule/update", methods=["PUT"])
def UpdateSchedule():
    from app.controllers.functions import ResponseOk
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "PUT": return ResponseMethodNotAllowed()
    data = request.get_json()
    schedule_update = SearchSchedule(ident=data["id"])
    if not schedule_update: return ResponseNotFound()
    schedule_exist = SearchSchedule(data_for_one=data)
    if schedule_exist: return ResponseBadRequest()
    schedule_update.name = data["name"]
    db.session.commit()
    return ResponseOK()


@app.route("/schedule/delete/<int:ident>", methods=["DELETE"])
def DeleteSchedule(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "DELETE": return ResponseMethodNotAllowed()
    if not ident: ResponseBadRequest()
    schedule_delete = SearchSchedule(ident=ident)
    target_schedule_id = schedule_delete.id
    if not schedule_delete: return ResponseNotFound()
    DeleteFromDataBase(schedule_delete)
    return ResponseGone()


def CreateScheduleData(data, lab):
    return Schedule(start=data['start'], end=data['end'], purpouse=data['purpouse'],
                    day_of_the_week=data['day of the week'], profession=data['profession'],
                    lab_agenda=lab)


def SearchSchedule(data_for_one=None, ident=None, data_for_various=None):
    if ident:
        return Schedule.query.filter_by(id=ident).first()

    elif data_for_one:
        return Schedule.query.filter_by(start=data_for_one['start'], day_of_the_week=data_for_one['day of the week'], laboratory_id=data_for_one['laboratory id']).first()

    elif data_for_various:
        return Schedule.query.filter_by(laboratory_id=data_for_various['laboratory id'], day_of_the_week=data_for_various['day of the week']).all()