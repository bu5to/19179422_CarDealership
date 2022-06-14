from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from base import Session, engine, Base
import base64
from models import User, Car
import os

import base64

app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    '''
    Implementation of LoginManager in Flask.
    :param user_id: the ID of the user that will be logging in
    :return: The user as an object, with his/her detailed information.
    '''
    users = User.get_users()
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/')
def index():
    return render_template('properties.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.files)
        photoFile = request.files.get('file')
        photo = base64.b64encode(photoFile.read())
        print(photo)
        new_user = User(request.form["username"],request.form["name"],request.form["email"],
                        request.form["password"],request.form["role"],request.form["address"],
                        photo,request.form["phone"])
        session = Session()
        session.add(new_user)
        session.commit()
        session.expunge_all()
        session.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

def create_tables():
    '''
    Method to create the tables in the PostgreSQL database with the SQLAlchemy library.
    '''
    Base.metadata.create_all(engine)
    print("Tables have been created.")
	
if __name__ == '__main__':
    os.environ["SECRET_KEY"] = "thisisasecretkey"
    os.environ["DATABASE_URL"] = "postgres://vglacsrsmzejof:07d04f521d50bb923ad37e6fcc55deabdd2a80984ec9d118880d8401abfa0cfc@ec2-54-228-32-29.eu-west-1.compute.amazonaws.com:5432/d3krde6k3aj05f"
    os.environ["MONGO_CLIENT"] = "mongodb://localhost:27017"
    app.run()