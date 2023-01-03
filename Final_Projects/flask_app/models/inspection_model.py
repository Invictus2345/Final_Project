from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

db = 'Final_Project'

class Inspection:
    def __init__(self,data):
        self.doors_that_close = data['doors_that_close']
        self.foundation_cracks = data['foundation_cracks']
        self.moldly_smell = data['moldly_smell']
        self.insects_pests = data['insects_pests']
        self.water_damage = data['water_damage']
        self.diy_additions = data['diy_additions']
        self.roof_issues = data['roof_issues']
        self.hvac_age = data['hvac_age']
        self.flooring = data['flooring']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.on_users = []



    @classmethod
    def save(cls,data):
        query = "INSERT INTO inspections (doors_that_close,foundation_cracks,moldly_smell,insects_pests,water_damage,diy_additions,roof_issues,hvac_age,flooring) VALUES (%(doors_that_close)s,%(foundation_cracks)s,%(moldly_smell)s,%(insects_pests)s,%(water_damage)s,%(diy_additions)s,%(roof_issues)s,%(hvac_age)s,%(flooring)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM inspections;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        print(users)
        return users

    @classmethod
    def get_one_home(cls,data):
        query  = "SELECT * FROM inspections WHERE id = %(id)s"
        result = connectToMySQL(db).query_db(query,data)
        yes = []
        for row in result:
            yes.append(cls(row))
        return yes

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM inspections WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_inspection(cls,data):
        query = "UPDATE inspections SET `doors_that_close`=%(doors_that_close)s,`foundation_cracks`=%(foundation_cracks)s,`moldly_smell`=%(moldly_smell)s, insects_pests=%(insects_pests)s,`water_damage`=%(water_damage)s,`diy_additions`=%(diy_additions)s,`roof_issues`=%(roof_issues)s,`hvac_age`=%(hvac_age)s,`flooring`=%(flooring)s WHERE id = %(id)s;" 
        return connectToMySQL(db).query_db(query,data)