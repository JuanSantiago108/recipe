import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at =  data['created_at']
        self.updated_at =  data['updated_at']

    @classmethod
    def get_one(cls,data):
        query = "SELECT *"
        query += "FROM users "
        query += "WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result )> 0:
            return cls(result[0])
        else:
            return None


    @classmethod
    def create (cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password ) "
        query += "VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)


    @staticmethod
    def validate_registracion(data):
        is_valid = True
        if data['first_name']=="":
            flash("Please provide your first name.", 'error_register_first_name')
            is_valid = False
        if len(data['first_name']) <2:
            flash("At least 2 characters.", 'error_register_first_name')
            is_valid = False
        if data['last_name']=="":
            flash("Please provide your last name.",'error_register_last_name')
            is_valid = False
        if len(data['last_name']) <2:
            flash("At least 2 characters.", 'error_register_last_name')
            is_valid = False
        if len(data['password']) =="":
            flash("Must provide a password,",'error_register_password')
            is_valid = False
        if  data['password'] != data['confirm_password']:
            flash("Password does not match",'error_register_password_confirmation')
            is_valid = False
        if data['confirm_password'] =="":
            flash("Must provide a password confirmation,",'error_register_password_confirmation')
            is_valid = False
        if data['email'] =="":
            flash("Must provide a email,",'error_register_email')
            is_valid = False
        if User.get_one(data)=="":
            flash("This email is already taken",'error_register_email')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email",'error_register_email')
            is_valid = False
        return is_valid
