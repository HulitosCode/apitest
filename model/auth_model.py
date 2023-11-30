from datetime import datetime, timedelta
from logging import exception
import mysql.connector
import jwt
from flask import make_response, request, json
import re
from functools import wraps

class auth_model():
    def __init__(self):

        #Conexao com Base de dados  
        try:
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="apitest"
            )
            self.mydb.autocommit = True
            self.cur = self.mydb.cursor(dictionary = True)
            print("Conexao bem Sucedida!")
        except:
            print("Erro na Conexao!")

    def token_auth(self, endpoint):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                authorization = request.headers.get("authorization")
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwtdecoded = jwt.decode(token, "Helton", algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                       return make_response({"ERROR": "Token Expirou!"}, 401)
                    role_id = jwtdecoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint='{endpoint}' ")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        print(json.loads(result[0]['roles']))
                        return func(*args)     
                    else:
                       return make_response({"ERROR":"Endpoint Desconhecido!"}, 404)      
                else:
                    return make_response({"ERROR":"ENDPOINT DESCONHECIDO"}, 404)               

            return inner2
        return inner1
