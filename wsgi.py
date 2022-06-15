from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from base import Session, engine, Base
import base64
from models import User, Car, Model
import os

import base64
def create_app():
    '''
    This method creates the application and sets up some environment variables that will need to be accessed
    later.
    :return: The created application.
    '''
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "thisisasecretkey"
    os.environ[
        "DATABASE_URL"] = "postgres://vglacsrsmzejof:07d04f521d50bb923ad37e6fcc55deabdd2a80984ec9d118880d8401abfa0cfc@ec2-54-228-32-29.eu-west-1.compute.amazonaws.com:5432/d3krde6k3aj05f"
    app.config["MONGO_CLIENT"] = "mongodb://localhost:27017"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app = create_app()
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
        try:
            if user.id == user_id:
                return user
        except:
            return None

@app.route('/viewcar/<int:carId>')
def viewcar(carId):
    car = Car.getCarById(carId) #4975facbbce511b65e14f44719340029-cf161184-91fc #Funciona con int, no con string
    return render_template("car.html", car=car)

@app.route('/carsearch')
def carsearch():
    cars = Car.getAllCars()
    modelslist, makeslist = Model.getDistinctModels()
    fuels = Car.getDistinctFuels()
    types = Car.getDistinctTypes()
    for car in cars:
        if len(car.description) > 250:
            car.description = car.description[0:250] + "..."
    return render_template('properties.html', cars = cars, makes = makeslist, models = modelslist, fuels = fuels,
                           types = types)



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        photoFile = request.files.get('file')
        photo = base64.b64encode(photoFile.read())
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
    if request.method == "POST":
        user = User.get_user(request.form['username'])
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('carsearch'))
        else:
            flash(u'Invalid user or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    '''
    The user is logged out.
    :return: Login webpage.
    '''
    logout_user()
    return redirect(url_for('login'))


def create_tables():
    '''
    Method to create the tables in the PostgreSQL database with the SQLAlchemy library.
    '''
    Base.metadata.create_all(engine)
    print("Tables have been created.")
	
if __name__ == '__main__':
    app.run()