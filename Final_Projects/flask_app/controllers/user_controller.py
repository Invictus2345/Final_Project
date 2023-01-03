from flask import Flask, render_template, request, session, redirect, flash
from flask_app import app
from flask_app.models.home_model import Home
from flask_app.models.user_model import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('Register_Login_Homepage.html')

@app.route('/register', methods=['POST'])
def register():
    register_form = request.form
    if not User.validate_user(register_form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name':request.form['first_name'],
        'last_name': request.form['last_name'],
        'email':request.form['email'],
        'password': pw_hash
    }
    user_id = User.save_user(data)
    session['user_id']= user_id
    print(register_form)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    print(request.form)
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Must login!')
        return redirect('/logout')
    data ={
        'id': session['user_id'],
    }

    holder = session['user_id']

    return render_template('dashboard.html',user=User.get_id(data), users=User.get_all_users(), homes = Home.get_all_homes_with_user(), please_work = holder)

@app.route('/your_purchases')
def your_purchases():
    data = {
        'id':session['user_id']
    }
    return render_template('user_purchases.html', homes = Home.get_user_all_likes(data))

