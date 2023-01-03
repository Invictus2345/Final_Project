from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import home_model
import re
db = 'Final_Project'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__(self,data):
        self.id= data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.on_homes = []

    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save_user(cls,data):
        query= "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users =[]
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one_user(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_user_with_likes(cls,data):
        query =  "SELECT * FROM users LEFT JOIN likes ON likes.user_id = users.id LEFT JOIN toppings ON likes.home_id = homes.id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        user = cls( results[0] )
        for row in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            home_data = {
                "id" : row["homes.id"],
                "title" : row["title"],
                "network" : row["network"],
                "release_date" : row["release_date"],
                "description" : row["description"],
                "user_id" : row["user_id"],
                "created_at" : row["homes.created_at"],
                "updated_at" : row["homes.updated_at"]
            }
            user.on_homes.append(home_model.home( home_data ) )
        return user


    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
            is_valid=False
        return is_valid

