from flask import render_template, session, request, redirect, url_for, jsonify, Response, escape, make_response
from flask_login import login_user
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.tables import Admin, Laboratory, Profession, Permission, SecurityKey, User
from app.models.tables import AllowedKey, EventLog, Schedule

from app.models.forms import LoginForm
#Se for passar para a funcao jsonify(), passar um dicionario.
#Se antes de passar fazer um json.dumps, destroi a estrutura json.
#Continua sendo JSON mas a leitura e o visual fica comprometido.
import json


######################################################################
################## FUNCTIONS WITH ROUTES #############################
######################################################################

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
        if request.method == "GET":
            #return render_template('login.html')
            return ResponseAccepted()
        else:
            return ResponseMethodNotAllowed()


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method=="POST":
        dado = request.get_json()
        name = dado['username']
        password = dado['password']    
        #name = request.form['username']
        #password = request.form['password']
        if auth_database_check(name, password):
            #session['logged_in'] = name
            #return redirect(url_for('index'))
            resp = make_response('')
            resp.set_cookie(name, password, 3600)
            #return ResponseOK()
            return resp
        else:
            return ResponseBadRequest()
    else:
        return ResponseMethodNotAllowed()  


#deslogar o user
@app.route("/logout", methods=['GET'])
def logout():
    if request.method=="GET":
        if 'logged_in' in session:
            #session.pop('logged_in', None)
            #return redirect(url_for('index'))
            return ResponseOK()
        else:
            return ResponseUnauthorized() 
    else:
        return ResponseMethodNotAllowed()


#função para checar no banco se os dados da entrada de login estão corretas de acordo com o banco
def auth_database_check(username, userpassword):
    admin_try = Admin.query.filter_by(login_name=username).first()
    password = check_password_hash(admin_try.password, userpassword)
    if admin_try and password:
        return True
    else:
        return False


##############################################################################
################## ADMIN'S FUNCTIONS #########################################
##############################################################################
@app.route("/admin/create", methods=["POST"])
def CreateAdmin():
    #if 'logged_in' in session:
        if request.method == "POST":
            data = request.get_json()

            #criptografar a senha que vem do Json
            hashed_password = generate_password_hash(data['password'], method='sha256')

            #checar se já existe tal usuário no BD, caso não tenha ele inseri
            if not SearchAdmin(data=data):
                new_admin = CreateAdminData(data, hashed_password)
                if new_admin:
                    SaveToDataBase(new_admin)
                    return ResponseCreated()
                else:
                    return ResponseBadRequest()
            else:
                return ResponseConflict()
    #else:
        #return ResponseUnauthorized()


@app.route("/admin/read/<int:ident>", methods=["GET"])
@app.route("/admin/read", defaults={"ident": None}, methods=["GET"])
def ReadAdmin(ident):
    #if 'logged_in' in session:
        if request.method == "GET":
            output = []
            if ident:
                admin = Admin.query.filter_by(id=ident).first()
                if admin:
                    admin_data = {}
                    admin_data['id'] = admin.id
                    admin_data['name'] = admin.name
                    admin_data['email'] = admin.email
                    return jsonify({"admin": admin_data})#200-OK
                else:
                    return ResponseNotFound()
            else:
                admins = Admin.query.all()
            
            for admin in admins:
                admin_data = {}
                admin_data['id'] = admin.id
                admin_data['name'] = admin.name
                admin_data['email'] = admin.email
                output.append(admin_data)

            return jsonify({'admins' : output})#200-OK
        else:
            return ResponseMethodNotAllowed()
    
    #else:
        #return ResponseUnauthorized()

@app.route("/admin/update", methods=["PUT"])
def UpdateAdmin():
    #if 'logged_in' in session:
        if request.method == "PUT":
            data = request.get_json()
            admin_update = SearchAdmin(ident=data["id"])
            if admin_update:
                hashed_password = generate_password_hash(data['password'], method='sha256')
                admin_update.name = data['name']
                admin_update.password = hashed_password
                admin_update.email = data['email']
                db.session.commit()
                return ResponseOK()
            else:
                return ResponseBadRequest()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/admin/delete/<int:ident>", methods=["DELETE"])
def DeleteAdmin(ident):
    #if 'logged_in' in session:
        if request.method == "DELETE":
            #criar o cara a ser deletado no banco
            if ident:
                admin_delete = SearchAdmin(ident=ident)
                #checar se foi encontrado o admin a ser deletado
                if admin_delete:
                    DeleteAdminData(admin_delete)
                    return ResponseGone()
                else:
                    return ResponseNotFound()
            else:
                return ResponseBadRequest()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/user/create", methods=["POST"])
def CreateUser():
    #if 'logged_in' in session:
        if request.method == "POST":
            insertion_result_list = {}
            data = request.get_json()
            if data:
                #Fazer a inserção da security key. O retorno é um dicionario
                result = InsertSecurityKey(data)
                insertion_result_list["security key"] = result["state"]
                #Se teve sucesso na inserção da security key ou já existe...
                if insertion_result_list["security key"] == "fail":
                    return ResponseBadRequest()
                else:
                    if not SearchUser(data=data):
                        sk = SearchSecurityKey(data=data)
                        insertion_result_list["user"] = SaveToDataBase(CreateUserData(data, sk))
                    else:
                        insertion_result_list["user"] = "exist"

                    result = InsertPermission(data)
                    insertion_result_list["permission"] = result["state"]

                    if insertion_result_list["user"] == "success":
                        return ResponseCreated()
                    elif insertion_result_list["user"] == "exist":
                        return ResponseConflict()

            else:
                return ResponseBadRequest()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/user/read/<int:ident>", methods=["GET"])
@app.route("/user/read", defaults={"ident": None}, methods=["GET"])
def ReadUser(ident):
    #if 'logged_in' in session:
        if request.method == "GET":
            output = []
            if ident:
                user = User.query.filter_by(id=ident).first()
                if user:
                    permissions = Permission.query.filter_by(user_id=user.id).all()
                    allowed_labs = []
                    for permission in permissions:
                        laboratory = Laboratory.query.filter_by(id=permission.laboratory_id).first()
                        allowed_labs.append(laboratory.name)
                    user_data = {}
                    user_data['email'] = user.email
                    user_data['security_key_id'] = user.security_key_id
                    user_data['internal_id'] = user.internal_id
                    user_data['name'] = user.name
                    user_data['id'] = user.id
                    user_data['permission'] = allowed_labs
                    if user.profession == Profession.estudante:
                        user_data["profession"] = "Estudante"
                    
                    return jsonify({"user": user_data})
                else:
                    return ResponseNotFound()
            else:
                users = User.query.all()
                for user in users:
                    permissions = Permission.query.filter_by(user_id=user.id).all()
                    allowed_labs = []
                    for permission in permissions:
                        laboratory = Laboratory.query.filter_by(id=permission.laboratory_id).first()
                        allowed_labs.append(laboratory.name)

                    user_data = {}
                    user_data['email'] = user.email
                    user_data['security_key_id'] = user.security_key_id
                    user_data['internal_id'] = user.internal_id
                    user_data['name'] = user.name
                    user_data['id'] = user.id
                    user_data['permission'] = allowed_labs

                    #user.profession devolve a classe com o enum
                    if user.profession == Profession.estudante:
                        user_data["profession"] = "Estudante"
                    output.append(user_data)

                return jsonify({'users' : output})#200-OK
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/user/update", methods=["PUT"])
def UpdateUser():
    #if 'logged_in' in session:
        if request.method == "PUT":
            data = request.get_json()
            user_update = SearchUser(ident=data["id"])
            if user_update:
                user_update.name = data['name']
                user_update.email = data['email']
                user_update.internal_id = data['internal_id']
                user_update.profession = data['profession']
                if user_update.profession == Profession.estudante:
                    user_data["profession"] = "Estudante"
                permissions_delete = SearchPermission(user=user_update)
                DeletePermission(permissions_delete)
                InsertPermission(data)
                db.session.commit()
                return ResponseOK()
            else:
                return ResponseBadRequest()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()

@app.route("/user/delete/<int:ident>", methods=["DELETE"])
def DeleteUser(ident):
    #if 'logged_in' in session:
        if request.method == "DELETE":
            if ident:
                user_delete = SearchUser(ident=ident)
                if user_delete:
                    target_user_id = user_delete.id
                    DeleteUserData(user_delete)
                    result = DeleteSecurityKey(target_user_id)
                    return ResponseGone()
                else:
                    return ResponseNotFound()
            else:
                return ResponseBadRequest()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/laboratory/create", methods=["POST"])
def CreateLaboratory():
    #if 'logged_in' in session:
        if request.method == "POST":
            data = request.get_json()
            if not SearchLaboratory(data=data)  :
                new_lab = Laboratory(name=data['name'])
                if new_lab:
                    SaveToDataBase(new_lab)
                    return ResponseCreated()
                else:
                    return ResponseBadRequest()
            else:
                return ResponseConflict()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/laboratory/read/<int:ident>", methods=["GET"])
@app.route("/laboratory/read", defaults={"ident": None}, methods=["GET"])
def ReadLaboratory(ident):
    #if 'logged_in' in session:
        if request.method == "GET":
            output = []
            if ident:
                laboratory = Laboratory.query.filter_by(id=ident).first()
                if laboratory:
                    laboratory_data = {}
                    laboratory_data['id'] = laboratory.id
                    laboratory_data['name'] = laboratory.name
                    output.append(laboratory_data)
                    
                    return jsonify({"laboratory": laboratory_data})
                else:
                    return ResponseNotFound()
            else:
                laboratories = Laboratory.query.all()
                for laboratory in laboratories:
                    laboratory_data = {}
                    laboratory_data['id'] = laboratory.id
                    laboratory_data['name'] = laboratory.name
                    output.append(laboratory_data)

                return jsonify({'laboratories' : output})
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/laboratory/update", methods=["PUT"])
def UpdateLaboratory():
    #if 'logged_in' in session:
        if request.method == "PUT":
            data = request.get_json()
            laboratory_update = SearchLaboratory(ident=data["id"])
            if laboratory_update:
                laboratory_exist = SearchLaboratory(name=data["name"])
                if not laboratory_exist:
                    laboratory_update.name = data["name"]
                    db.session.commit()
                    return ResponseOK()
                else:
                    return ResponseBadRequest()
            else:
                return ResponseConflict()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


@app.route("/laboratory/delete/<int:ident>", methods=["DELETE"])
def DeleteLaboratory(ident):
    #if 'logged_in' in session:
        if request.method == "DELETE":
            if ident:
                laboratory_delete = SearchLaboratory(ident=ident)
                target_laboratory_id = laboratory_delete.id
                if laboratory_delete:
                    DeleteLaboratoryData(laboratory_delete)
                    return ResponseGone()
                else:
                    return ResponseNotFound()
            else:
                return ResponseBadRequest()
        else:
            return ResponseMethodNotAllowed()
    #else:
        #return ResponseUnauthorized()


#################################################################
############### FUNCOES - Ordem Alfabetica ######################
#################################################################
def CreateAdminData(data, hashed_password):
    return Admin(name=data['name'], login_name=data['login_name'],
                 password=hashed_password, email=data['email'])

def CreatePermissionData(user, laboratory):
    return Permission(member=user, place=laboratory)


def CreateSecurityKeyData(data):
    return SecurityKey(security_key=data["security_key"])


def CreateUserData(data, sk):
    return User(name=data["name"], email=data["email"], internal_id=data["internal_id"],
                profession=data["profession"], access_key=sk)


def DeleteAdminData(admin_delete):
    db.session.delete(admin_delete)
    db.session.commit()
    return "success"


def DeleteLaboratoryData(laboratory_delete):
    db.session.delete(laboratory_delete)
    db.session.commit()
    return "success"


def DeletePermission(permissions_delete):
    if len(permissions_delete) == 0:
        return "empty"
    else:
        for permission in permissions_delete:
            DeletePermissionData(permission)


def DeletePermissionData(permission):
    db.session.delete(permission)
    db.session.commit()
    return "success"


def DeleteSecurityKey(target_user_id):
        sk_delete = SearchSecurityKey(ident=target_user_id)
        if sk_delete:
            DeleteSecurityKeyData(sk_delete)
            return jsonify({"message": "Security Key deleted successfully"})
        
        return jsonify({'message': 'Cannot delete this one'})


def DeleteSecurityKeyData(delete_sk):
    db.session.delete(delete_sk)
    db.session.commit()
    return "success"


def DeleteUserData(delete_user):
    db.session.delete(delete_user)
    db.session.commit()
    return "success"


def InsertPermission(data):
    flag = 0
    fail_list = []
    user = SearchUser(data=data)
    if len(data["permission"]) > 0:
        for lab in data["permission"]:
            laboratory = SearchLaboratory(name=lab)
            if not SearchPermission(data=data, user=user, laboratory=laboratory):
                SaveToDataBase(CreatePermissionData(user, laboratory))
            else:
                flag = 1
                fail_list.append("{}".format(lab))

        if flag == 0:
            return {"message": "All permissions inserted successfully", "state": "success"}
        else:
            message = ""
            for fail in fail_list:
                message = "{0} {1}".format(message, fail)
            message = message[1:]
            return {"message": "Have permissions alredy exists", "state": "exist"}

    else:
        return {"message": "No have permissions for insertion", "state": "fail"}


def InsertSecurityKey(data):
    new_data = None
    if data:
        if not SearchSecurityKey(data=data):
            result = SaveToDataBase(CreateSecurityKeyData(data))
            return {"message": "Security key inserted successfully", "state": result}
        else:
           return {"message": "Security key alredy exists", "state": "exist"}
    else:
        return {"message": "Failed security key insertion", "state": "fail"}


def SaveToDataBase(new_data):
    db.session.add(new_data)
    db.session.commit()
    return "success"


def SearchAdmin(data=None, ident=None):
    if data:
        return Admin.query.filter_by(email=data['email'], login_name=data['login_name']).first()
    elif ident:
        return Admin.query.filter_by(id=ident).first()


def SearchLaboratory(data=None, name=None, ident=None):
    if name:
        return Laboratory.query.filter_by(name=name).first()
    elif ident:
        return Laboratory.query.filter_by(id=ident).first()
    elif data:
        return Laboratory.query.filter_by(name=data["name"]).first()


def SearchPermission(data=None, user=None, laboratory=None):
    if user and laboratory:
        return Permission.query.filter_by(user_id=user.id, laboratory_id=laboratory.id).first()
    elif user:
        return Permission.query.filter_by(user_id=user.id).all()
    elif laboratory:
        return Permission.query.filter_by(laboratory_id=laboratory_id).all()


def SearchSecurityKey(data=None, ident=None):
    if data:
        return SecurityKey.query.filter_by(security_key=data["security_key"]).first()
    elif ident:
        return SecurityKey.query.filter_by(id=ident).first()


def SearchUser(data=None, ident=None):
    if data:
        return User.query.filter_by(name=data["name"], email=data["email"], profession=data["profession"]).first()
    elif ident:
        return User.query.filter_by(id=ident).first()

#################################################################
############# FUNCOES PARA RETORNO DAS RESPOSTAS ################
#################################################################

def ResponseContinue():
    return Response(None, status=100, mimetype="")

def ResponseOK():
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

def ResponseConflict():
    return Response(None, status=409, mimetype="")

def ResponseGone():
    return Response(None, status=410, mimetype="")


#################################################################
############# FUNCOES DESCARTADAS OU DE TESTE ###################
#################################################################

#apenas para criar o primeiro usuário do sistema
'''
@app.route("/createFirstUser")
def createFirst():

    hashed_password = generate_password_hash('321', method='sha256')

    first_user = Admin(name='Augusto', login_name='Goias', password=hashed_password, email='augusto@gmail.com')
    db.session.add(first_user)
    db.session.commit()

    return jsonify({'message' : 'First User registed'})

#teste para inserir uma chave de acesso
@app.route("/createtest")
def createtest():
    if session.get('logged_in'):
        chave = SecurityKey(security_key = "000")
        db.session.add(chave)
        db.session.commit()
        return jsonify({'message' : 'Successful login'})
    else: 
        return jsonify({'message' : 'Voce precisa logar'})
'''

"""
#Rota de CRUD para Securty Key
@app.route("/crud_securityKey", methods = ["GET", "POST", "DELETE", "PUT"])
def CRUDSecurityKey():
    ##if session.get("logged_in"):
        if request.method == "POST":
            #criar uma variavel para receber o Json
            data = request.get_json()            
            #checar se já existe tal chave no BD, caso não tenha ele inseri
            if not SecurityKey.query.filter_by(security_key=data['security_key']).first():
                new_key = SecurityKey(security_key=data['security_key'])
                if new_key:
                    db.session.add(new_key)
                    db.session.commit()
                    return jsonify({"message" : "SecurityKey user added!"})
                else:
                    return jsonify({"message" : "SecurityKey user not added!"})
            else:
                return jsonify({"message" : "Key duplicate!"})
        elif request.method == "DELETE":
            #pegar o Json do cara a ser deletado
            data = request.get_json()
            #criar o cara a ser deletado no banco
            key_delete = SecurityKey.query.filter_by(security_key=data['security_key']).first()
            #checar se foi encontrado a key a ser deletado
            if key_delete:
                db.session.delete(key_delete)
                db.session.commit()
                return jsonify({"message" : "Key has been deleted!"})
            else:
                return jsonify({"message" : "Target not found!"})
        else:
            return jsonify({"message " : "Method not allowed!"})
    #else:
        #return jsonify({"message " : "You are not logged!"})
"""
"""
@app.route("/cadastroSecurityKey")
def cadastrarSecurityKey():
    if session.get('logged_in'):
        return render_template("cadastro.html")

    return jsonify({'message' : 'Voce precisa logar'})


@app.route("/SecurityKey/cadastro", methods=['POST'])
def cadastro():
    if request.method == "POST":
        data = request.form.get("SecurityKey")

        if data:
            new_key = SecurityKey(security_key=data)
            db.session.add(new_key)
            db.session.commit()

        else:
            return jsonify({'message' : 'Cannot register on database'})

    return redirect(url_for("index"))


@app.route("/deletarSecurityKey")
def deletar():
    if session.get('logged_in'):
        return render_template("delete.html")

    return jsonify({'message' : 'Voce precisa logar'})


@app.route("/editarSecurityKey", methods=["PUT"])
def editar():
    if session.get('logged_in'):
        edit_key = SecurityKey.query.filter_by(id=1)

        if not edit_key:
            return jsonify({'message' : 'Target not found'})

        edit_key.security_key = 55
        db.session.commit()
        return jsonify({'message' : 'Target changed'})

    return jsonify({'message' : 'Voce precisa logar'})


@app.route("/listaSecurityKey")
def lista():
    if session.get('logged_in'):
        keys = SecurityKey.query.all()

        output = []

        for security_key in keys:
            security_key_data = {}
            security_key_data['id'] = security_key.id
            security_key_data['security_key'] = security_key.security_key
            output.append(security_key_data)

        return jsonify({'keys' : output})
    else:
        return jsonify({'message' : 'Voce precisa logar'})

    #return render_template("lista.html", Keys=Keys)
    """