#Importando app do app.py
from app import app
from flask import request, send_file
from datetime import datetime
import os

#Importando a class user_model no model
from model.user_model import user_model
from model.auth_model import auth_model

#importando o objecto da funcao user_model dentro da class user_model
obj = user_model()
auth = auth_model()

@app.route("/user/getall")
@auth.token_auth("/user/getall")
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/addone", methods = ["POST"])
@auth.token_auth("/user/addone")
def user_addone_controller():
    return obj.user_addone_model(request.form)

@app.route("/user/addmultiple", methods = ["POST"])
def add_multiple_users_controller():
    return obj.add_multiple_users_model(request.json)

@app.route("/user/update", methods = ["PUT"])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route("/user/delete/<int:id>", methods = ["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route("/user/patch/<int:id>", methods = ["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods = ["GET"])
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)


@app.route("/user/login", methods = ["POST"])
def user_login_controller():
    return obj.user_login_model(request.form)