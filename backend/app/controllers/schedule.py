from flask import jsonify, request, session
from app import app, db

from app.models.tables import DayOfTheWeek, Laboratory, Profession, Permission, Schedule, SecurityKey, User
from app.models.forms import LoginForm

from app.controllers.functions import (SaveToDataBase, DeleteFromDataBase,
ResponseBadRequest, ResponseCreated, ResponseConflict,
ResponseMethodNotAllowed, ResponseNotFound, ResponseOk)
from app.controllers.laboratory import SearchLaboratory
import json
import datetime


@app.route("/schedule/create", methods=["POST"])
def CreateSchedule():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "POST": return ResponseMethodNotAllowed()
    data = request.get_json()
    if SearchSchedule(data_for_one=data): return ResponseConflict()
    
    if not CanCreateNewSchedule(data):
        print("Conflito de horário")
        return ResponseConflict()

    lab = SearchLaboratory(ident=data['laboratory_id'])
    if not lab: return ResponseNotFound()
    new_schedule = CreateScheduleData(data, lab)
    if not new_schedule: return ResponseBadRequest()
    SaveToDataBase(new_schedule)
    return ResponseCreated()


@app.route("/schedule/read/<int:ident>", methods=["GET"])
@app.route("/schedule/read", defaults={"ident": None, "dayoftheweek": None, "laboratory": None}, methods=["GET"])
def ReadSchedule(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "GET": return ResponseMethodNotAllowed()
    output = []
    schedules = []
    arg_week = request.args.get('dayoftheweek')
    arg_laboratory = request.args.get('laboratory')

    if ident:
        schedules.append(Schedule.query.filter_by(id=ident).first())
    
    elif arg_week and arg_laboratory:
        schedules.append(Schedule.query.filter_by(day_of_the_week=arg_week, laboratory=arg_laboratory))
    
    elif arg_week:
        schedules.append(Schedule.query.filter_by(day_of_the_week=arg_week))

    elif arg_laboratory:
        schedules.append(Schedule.query.filter_by(laboratory=arg_laboratory))

    else:
        schedules = Schedule.query.all()
    
    if schedules[0] == None: return ResponseNotFound()

    for schedule in schedules:
        schedule_data = {}
        schedule_data['id'] = schedule.id
        schedule_data['start'] = schedule.start.__str__()
        schedule_data['end'] = schedule.end.__str__()
        schedule_data['purpouse'] = schedule.purpouse
        schedule_data['day_of_the_week'] = schedule.day_of_the_week.value
        schedule_data['profession'] = schedule.profession.value
        schedule_data['laboratory_id'] = schedule.laboratory_id
        output.append(schedule_data)
    
    return jsonify({"schedules": output})


@app.route("/schedule/update", methods=["PUT"])
def UpdateSchedule():
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "PUT": return ResponseMethodNotAllowed()

    data = request.get_json()
    schedule_update = SearchSchedule(ident=data["id"])
    if not schedule_update: return ResponseNotFound()

    if not CanUpdateSchedule(data): return ResponseConflict()
    schedule_update.start = data['start']
    schedule_update.end = data['end']
    schedule_update.purpouse = data['purpouse']
    schedule_update.day_of_the_week = DayOfTheWeek(data['day_of_the_week']).name 
    schedule_update.laboratory_id = data['laboratory_id']
    schedule_update.profession = Profession(data['profession']).name
    db.session.commit()
    return ResponseOk()


@app.route("/schedule/delete/<int:ident>", methods=["DELETE"])
def DeleteSchedule(ident):
    #if not 'logged_in' in session: return ResponseUnauthorized()
    if request.method != "DELETE": return ResponseMethodNotAllowed()
    if not ident: ResponseBadRequest()
    schedule_delete = SearchSchedule(ident=ident)
    if not schedule_delete: return ResponseNotFound()
    DeleteFromDataBase(schedule_delete)
    return ResponseOk()


def CanCreateNewSchedule(data):
    schedules = SearchSchedule(data_for_various=data)
    for schedule in schedules:
        if SubtractTime(schedule.start, data['start']) >= 0:
            if ConvertToMinutes(schedule.start) < ConvertToMinutes(data['end']):
                return False
        else:
            if ConvertToMinutes(schedule.end) > ConvertToMinutes(data['start']):
                return False
    return True


def CanUpdateSchedule(data):
    schedules = SearchSchedule(data_for_various=data)
    current_schedule = SearchSchedule(ident=data['id'])
    for schedule in schedules:
        if schedule.id == current_schedule.id:
            continue
        if SubtractTime(schedule.start, data['start']) >= 0:
            if ConvertToMinutes(schedule.start) < ConvertToMinutes(data['end']):
                return False
        else:
            if ConvertToMinutes(schedule.end) > ConvertToMinutes(data['start']):
                return False
    return True


def ConvertToMinutes(time):
    if type(time) == datetime.time:
        time = time.__str__()
    time = time.split(':')
    return int(time[0])*60 + int(time[1]) 


def CreateScheduleData(data, lab):
    return Schedule(start=data['start'], end=data['end'], purpouse=data['purpouse'],
                    day_of_the_week=DayOfTheWeek(data['day_of_the_week']).name,
                    profession=Profession(data['profession']).name, lab_agenda=lab)


def SearchSchedule(data_for_one=None, ident=None, data_for_various=None):
    if ident:
        return Schedule.query.filter_by(id=ident).first()

    elif data_for_one:
        return Schedule.query.filter_by(start=data_for_one['start'],
                                        day_of_the_week=DayOfTheWeek(data_for_one['day_of_the_week']).name,
                                        laboratory_id=data_for_one['laboratory_id']).first()

    elif data_for_various:
        return Schedule.query.filter_by(laboratory_id=data_for_various['laboratory_id'],
                                        day_of_the_week=DayOfTheWeek(data_for_various['day_of_the_week']).name).all()


def SubtractTime(time_a, time_b):
    sum_a = ConvertToMinutes(time_a)
    sum_b = ConvertToMinutes(time_b)
    return sum_a-sum_b