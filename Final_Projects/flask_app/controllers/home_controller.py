from crypt import methods
from flask import Flask, render_template, request, session, redirect, flash
from flask_app import app
from flask_app.models.home_model import Home
from flask_app.models.user_model import User
from collections import Counter
import requests

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/create_page')
def create_pg():
    return render_template('/create_a_home_page.html')

@app.route('/Register_Page')
def register_page():
    return render_template('Register_Page.html')


@app.route('/create_a_home', methods=['POST'])
def create_home():
        home_form = request.form
        # if not Home.validate_form(home_form):
        #     return redirect('/create_page')
        Home.save(request.form)
        return redirect('/dashboard')

@app.route('/view_home/<int:id>')
def view(id):
    data ={
        'id':id
    }

    return render_template('View_Single_home.html',home =Home.get_one_home_user(data))

@app.route('/edit_page/<int:id>')
def edit(id):
    data ={
        'id':id
    }
    return render_template('Edit_home.html', home = Home.get_one_home(data))

@app.route('/update_home/', methods=['POST'])
def update():
    home_form = request.form
    if not Home.validate_form(home_form):
            return redirect('/dashboard')
    Home.update_home(request.form)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    data ={
        'id': id
    }
    print(data, "@@@@@@@@@@@@@@@@@@@@@@@@@")
    Home.delete(data)
    return redirect('/dashboard')

@app.route('/delete2/<int:id>')
def delete2(id):
    data ={
        'id': id
    }
    print(data, "@@@@@@@@@@@@@@@@@@@@@@@@@")
    Home.delete2(data)
    return redirect('/dashboard')


@app.route('/like/', methods=['POST'])
def like():
    data = {
        'user_id':request.form['user_id'],
        'home_id':request.form['home_id']
    }
    Home.add_like_to_home(data)
    return redirect('/your_purchase')

@app.route('/unlike',methods=['POST'])
def unlike():
    data = {
        'user_id':request.form['user_id'],
        'home_id':request.form['home_id']
    }
    Home.delete_like_from_home(data)
    return redirect('/your_purchases')

def mortage(request):
    import requests

    api_url = 'https://api.api-ninjas.com/v1/mortgagecalculator?loan_amount=200000&interest_rate=3.5&duration_years=30'
    response = requests.get(api_url, headers={'X-Api-Key': 'FZMY+8nGEBnzglhbKYvsZQ==BcGAhzQnYL31wttZ'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

# FZMY+8nGEBnzglhbKYvsZQ==BcGAhzQnYL31wttZ
