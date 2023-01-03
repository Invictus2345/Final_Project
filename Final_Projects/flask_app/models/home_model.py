from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user_model
from flask_app.models import home_model
from flask import flash
import datetime

db = "Final_Project"

class Home:
    def __init__(self, data):
        self.id = data['id']
        self.image = data['image']
        self.location = data['location']
        self.size = data['size']
        self.price = data['price']
        self.beds = data['beds']
        self.baths = data['baths']
        self.style_of_home = data['style_of_home']
        self.HOA_fees = data['HOA_fees']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.on_users = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO homes (price,location,size,user_id,beds,baths,style_of_home,HOA_fees) VALUES (%(price)s,%(location)s,%(size)s,%(user_id)s,%(beds)s,%(baths)s,%(style_of_home)s,%(HOA_fees)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM homes;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        print(users)
        return users

    @classmethod
    def get_all_homes_with_user(cls):
        query ="SELECT * FROM homes left join users as user1 on homes.user_id = user1.id left join users as user2 on homes.id = user2.id;"
        results = connectToMySQL(db).query_db(query)
        all_homes = []
        for row in results:
            home = cls(row)
            home_data = {
            'id':row['id'],
            'image':row['image'],
            'location':row['location'],
            'size':row['size'],
            'price':row['price'],
            'beds':row['beds'],
            'baths':row['baths'],
            'style_of_home':row['style_of_home'],
            'HOA_fees':row['HOA_fees'],
            'user_id':row['user_id'],
            'created_at':row['created_at'],
            'updated_at':row['updated_at']
            }
            home_model.Home(home_data)

            user_data = {
                'id': row['user2.id'],
                'first_name':row['first_name'],
                'last_name': row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['user2.created_at'],
                'updated_at':row['user2.updated_at']
            }
            home.creator=user_model.User(user_data)
            all_homes.append(home)
        return all_homes

    @classmethod
    def get_one_home_user(cls,data):
        query  = "SELECT * FROM users LEFT JOIN homes on users.id = homes.user_id WHERE homes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        home = cls(result[0])
        for row in result:
            home_data = {
            'id':row['id'],
            'image':row['image'],
            'location':row['location'],
            'size':row['size'],
            'price':row['price'],
            'beds':row['beds'],
            'baths':row['baths'],
            'style_of_home':row['style_of_home'],
            'HOA_fees':row['HOA_fees'],
            'user_id':row['user_id'],
            'created_at':row['created_at'],
            'updated_at':row['updated_at']
            }
            home_model.Home(home_data)
            
            user_data = {
                'id':row['user_id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at']
            }
            
            home.creator= user_model.User(user_data)
            
        return home

    @classmethod
    def get_one_home(cls,data):
        query  = "SELECT * FROM homes WHERE id = %(id)s"
        result = connectToMySQL(db).query_db(query,data)
        yes = []
        for row in result:
            yes.append(cls(row))
        return yes

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM homes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete2(cls,data):
        query  = "DELETE FROM homes WHERE user_id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_home(cls,data):
        query = "UPDATE homes SET `location`=%(location)s,`size`=%(size)s,`price`=%(price)s, beds=%(beds)s,`baths`=%(baths)s,`style_of_home`=%(style_of_home)s,`HOA_fees`=%(HOA_fees)s WHERE id = %(id)s;" 
        return connectToMySQL(db).query_db(query,data)
        

    @classmethod
    def get_home_with_likes(cls,data):
        query = "SELECT * FROM homes LEFT JOIN likes ON likes.home_id = homes.id LEFT JOIN users ON likes.user_id = users.id WHERE homes.id = %(id)s;"
        results = connectToMySQL(db).query_db( query , data )
        home = cls( results[0] )
        for row in results:
            if row['homes.id']== None:
                break
            # Now we parse the topping data to make instances of toppings and add them into our list.
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password": row['password'],
                "created_at" : row["created_at"],
                "updated_at" : row["updated_at"]
            }
            home.on_users.append(user_model.User(user_data) )
        count =len(home.on_users)
        return count


    @classmethod
    def add_like_to_home(cls,data):
        query = "INSERT INTO likes (user_id,home_id) VALUES (%(user_id)s, %(home_id)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def delete_like_from_home(cls,data):
        query = "DELETE FROM `likes` WHERE (`home_id` = %(home_id)s) and (`user_id` = %(user_id)s);"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def get_user_all_likes(cls,data):
        query ="SELECT * from likes WHERE user_id= %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_form(home_form):
        is_valid = True
        if len(home_form['price']) <= 0:
            flash("price must be greater than 0")
            is_valid = False
        if len(home_form['location']) < 3:
            flash("location must be at least 3 characters")
            is_valid = False
        if len(home_form['price']) <=0 :
            flash("Price must be greater than 0")
            is_valid = False
        return is_valid

