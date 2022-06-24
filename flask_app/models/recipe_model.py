from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty = data['under_thirty']
        self.created_at =  data['created_at']
        self.updated_at =  data['updated_at']
        self.user_id =  data['user_id']
    
    @classmethod
    def create(cls,data):
        query ="INSERT INTO recipes ( name, description, instructions, under_thirty, created_at, user_id) " 
        query += "VALUES( %(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(created_at)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    

    @classmethod
    def get_all(cls):
        query =  "SELECT * "
        query += "FROM recipes;"
        result = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        if len(result )> 0:
            for recipe in result:
                recipes.append( cls( recipe ) )
        return recipes


    @classmethod
    def get_one(cls,data):
        query = "SELECT * "
        query += "FROM recipes "
        query += "WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result )>0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM recipes "
        query += "WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def update_one(cls,data):
        query =  "UPDATE recipes "
        query += "SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, "
        query += "under_thirty = %(under_thirty)s, user_id = %(user_id)s,created_at = %(created_at)s "
        query += "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)



    @staticmethod
    def validate_recipes(data):
        is_valid = True
        if data['name']=="":
            flash("Must provide a name",'error_recipe_name')
            is_valid = False
        if len(data['name']) <3:
            flash("At least 3 characters.", 'error_recipe_name')
            is_valid = False
        if data['description']=="":
            flash("Must provide a name",'error_recipe_description')
            is_valid = False
        if len(data['description']) <3:
            flash("At least 3 characters.", 'error_recipe_description')
            is_valid = False
        if data['instructions']=="":
            flash("Must provide a name",'error_recipe_instructions')
            is_valid = False
        if len(data['instructions']) <3:
            flash("At least 3 characters.", 'error_recipe_instructions')
            is_valid = False
        return is_valid