import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt

class user_model():
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


    #Logica de Negocio
    def user_getall_model(self):
        #Query execution code
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result) > 0:
            #Retorna dados em forma json
            res = make_response({"payload": result}, 200)
            res.headers['Acesse-Contol-Allow-Origin'] = "*"
            return res
        else:
            #Retorna uma mensagem em forma de json
            return make_response({"messege":"Nenhum dado foi Encontrado!"}, 204)
        

    def user_addone_model(self, data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}')")        
        return make_response({"messege":"Usuario Criado com sucesso!"}, 201)
    

    def user_update_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}' WHERE id='{data['id']}'")
        if self.cur.rowcount > 0:
            return make_response({"messege":"Dados Actualizados com Sucesso!"}, 201)
        else:
            return make_response({"messege":"Nenhum Dados foi Actualizado!"}, 202)


    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount > 0:
            return make_response({"messege":"Dados Excluidos com Sucesso!"}, 200)
        else:
            return make_response({"messege":"Nenhum Dados foi Excluido!"}, 202)
        

    def user_patch_model(self, data, id):
        #UPDATE users SET col=val, col=val WHERE id={id}
        qry = "UPDATE users SET "
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id={id}"
        
        self.cur.execute(qry)
        if self.cur.rowcount > 0:
            return make_response({"messege":"Dados Atualizados com Sucesso!"}, 200)
        else:
            return make_response({"messege":"Nenhum Dado foi Excluido!"}, 202)
        
    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f" SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result) > 0:
            #Retorna dados em forma json
            res = make_response({"payload": result, "page_no":page, "limit":limit}, 200)
            return res
        else:
            #Retorna uma mensagem em forma de json
            return make_response({"messege":"Nenhum dado foi Encontrado!"}, 204)
        
    
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        
        userdata = result[0]
        exp_time =  datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload": userdata,
            "exp": exp_epoch_time
        }
        jwtoken = jwt.encode(payload, "Helton", algorithm="HS256")
        return make_response({"token": jwtoken}, 200)
        