from flask import session,request,render_template,redirect,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt =  Bcrypt(app)

@app.route("/")
def display_login_registracion():
    return render_template( "index.html")


@app.route('/user/new', methods = ['POST'])
def create_user():
    if not User.validate_registracion(request.form) == True:
        return redirect('/')
    data = {
        "email": request.form['email']
    }
    result = User.get_one(data) # checking if the email that ther user is providing is not in user with anothoer user

    if result == None: # if its new i we sahll continue
        # Add the new user
        data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
        }

        user_id = User.create(data)
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        session['user_id'] = user_id
        return redirect ("/dashboard")
    else:
        flash("That email already exists,please select another one","error_register_email")
        return redirect ("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route("/login", methods=['POST'])
def login():
    if not session:
        data = {
            'email':request.form['email']
        }
        result = User.get_one(data)
        # result has id, first_name, last_name, email, password
        if result == None:
            flash("Incorrect password/email","error_login")
            return redirect ('/')
            # ^ Checks if email exists/matches one in the database
        elif  not bcrypt.check_password_hash(result.password, request.form['password']):
            flash("Incorrect password/email","error_login")
            return redirect('/')
            # ^ Checks if password from form matches the hashed password stored in the database.
        else:
            session['user_id'] = result.id
            session['first_name'] = result.first_name
            session['last_name'] = result.last_name
            session['email'] = result.email
            return redirect ('/dashboard')
            # ^ Lets user login if all credentials are correct.
    return redirect('/dashboard')
    


