from flask import escape, jsonify, make_response, redirect, render_template, request, Response, session, url_for
from flask_login import login_user
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.tables import Admin

from app.models.forms import LoginForm
#Se for passar para a funcao jsonify(), passar um dicionario.
#Se antes de passar fazer um json.dumps, destroi a estrutura json.
#Continua sendo JSON mas a leitura e o visual fica comprometido.

from app.controllers.functions import SaveToDataBase, DeleteFromDataBase
from app.controllers.functions import ResponseAccepted, ResponseBadRequest, ResponseCreated, ResponseGone
from app.controllers.functions import ResponseMethodNotAllowed, ResponseNotFound, ResponseUnauthorized

import json


@app.route("/index", methods=['GET'])
@app.route("/", methods=['GET'])
def index():
    #if 'logged_in' not in session:
        #if not 'logged_in' in session:
        #if not session.get('logged_in'):
            #return render_template('login.html')
            # PEGAR NOME DO USUARIO LOGADO
            #login = '%s' % escape(session['logged_in'])
            #return jsonify({'adminss: ': login})  
        #return ResponseUnauthorized()
    #else:
        if request.method != "GET": return ResponseMethodNotAllowed()
        #return render_template('login.html')
        return ResponseAccepted()


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method!="POST": return ResponseMethodNotAllowed() 
    dado = request.get_json()
    name = dado['username']
    password = dado['password']    
    #name = request.form['username']
    #password = request.form['password']
    if not auth_database_check(name, password): return ResponseBadRequest()
    #session['logged_in'] = name
    #return redirect(url_for('index'))
    resp = make_response('')
    resp.set_cookie(name, password, 3600)
    #return ResponseOk()
    return resp


#deslogar o user
@app.route("/logout", methods=['GET'])
def logout():
    from app.controllers.functions import ResponseOk
    if request.method!="GET": return ResponseMethodNotAllowed()
    if not 'logged_in' in session: return ResponseUnauthorized() 
    #session.pop('logged_in', None)
    #return redirect(url_for('index'))
    return ResponseOk()


#função para checar no banco se os dados da entrada de login estão corretas de acordo com o banco
def auth_database_check(username, userpassword):
    admin_try = Admin.query.filter_by(login_name=username).first()
    password = check_password_hash(admin_try.password, userpassword)
    if admin_try and password: return True
    return False