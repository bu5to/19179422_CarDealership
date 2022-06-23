from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from base import Session, engine, Base
from models import User, Car, Model
from regression import carsModel, parseAttributesToLabels
import numpy as np
import base64
import os
import pymongo
import random


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


@app.route('/photo/<int:user_id>')
def photo(user_id):
    user = User.get_user(str(user_id))
    b64_string = user.profilePic
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    image_64_decode = base64.b64decode(b64_string)
    return Response(image_64_decode, mimetype='image/jpg')


@app.route('/viewcar/<int:carId>')
def viewcar(carId):
    car = Car.getCarById(carId)  # 4975facbbce511b65e14f44719340029-cf161184-91fc #Funciona con int, no con string
    seller = User.get_user(car.user_id)
    numCars = len(Car.getCarsByAttribute("user", seller.id))
    similarBodyDict = Car.getCarsByAttribute("type", car.bodyType)
    similarPriceDict = Car.getCarsByAttribute("price", [car.price * 0.8, car.price * 1.2])
    similarCarsDict = [x for x in similarBodyDict if x in similarPriceDict]
    similarCars = random.choices(Car.parseDictToCars(similarCarsDict), k=3)
    return render_template("car.html", car=car, seller=seller, numCars=numCars, similarCars=similarCars)


@app.route('/carsearch', methods=["GET", "POST"])
def carsearch():
    cars = Car.getAllCars()
    modelslist, makeslist = Model.getDistinctModels()
    fuels = Car.getDistinctFuels()
    types = Car.getDistinctTypes()
    ranges = Car.getPriceAndYearRange()
    if 'user_id' in request.form:
        carsDicts = Car.getCarsByAttribute("user", request.form['user_id'])
        cars = Car.parseDictToCars(carsDicts)
    if request.method == "POST" and 'user_id' not in request.form:
        print(request.form)
        pricerange = request.form["pricerange"].split(",")
        yearrange = request.form["yearrange"].split(",")
        headingSearch, descSearch, makeSearch, modelSearch, fuelSearch, bodyTypeSearch, priceSearch, yearSearch = (
            Car.getAllCardicts() for i in range(8))
        if request.form["keyword"] != "":
            headingSearch = Car.getCarsByAttribute("heading", request.form["keyword"])
            descSearch = Car.getCarsByAttribute("heading", request.form["keyword"])
        if request.form["make"] != "":
            makeSearch = Car.getCarsByAttribute("make", request.form["make"])
        if request.form["model"] != "":
            modelSearch = Car.getCarsByAttribute("model", request.form["model"])
        if request.form["fuel"] != "":
            fuelSearch = Car.getCarsByAttribute("fuel", request.form["fuel"])
        if request.form["body"] != "":
            bodyTypeSearch = Car.getCarsByAttribute("type", request.form["body"])
        if request.form["pricerange"] != "":
            priceSearch = Car.getCarsByAttribute("price", [int(pricerange[0]), int(pricerange[1])])
        if request.form["yearrange"] != "":
            yearSearch = Car.getCarsByAttribute("year", [int(yearrange[0]), int(yearrange[1])])
        listSearch = [headingSearch, descSearch, makeSearch, modelSearch, fuelSearch, bodyTypeSearch, priceSearch,
                      yearSearch]
        list1 = [x for x in headingSearch if x in descSearch]
        list2 = [x for x in list1 if x in makeSearch]
        list3 = [x for x in list2 if x in modelSearch]
        list4 = [x for x in list3 if x in fuelSearch]
        list5 = [x for x in list4 if x in bodyTypeSearch]
        list6 = [x for x in list5 if x in priceSearch]
        carsDicts = [x for x in list6 if x in yearSearch]
        # Intersection done manually as there is no way to do an intersection between multiple lists of dicts
        cars = Car.parseDictToCars(carsDicts)

    cars = cars[:50]

    # intersection = headingSearch & descSearch & makeSearch & modelSearch & fuelSearch & bodyTypeSearch & priceSearch & yearSearch
    # print(intersection)

    for car in cars:
        if len(car.description) > 250:
            car.description = car.description[0:250] + "..."
    return render_template('properties.html', cars=cars, makes=makeslist, models=modelslist, fuels=fuels,
                           types=types, ranges=ranges)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        photoFile = request.files.get('file')
        photo = base64.b64encode(photoFile.read())
        new_user = User(request.form["username"], request.form["name"], request.form["email"],
                        request.form["password"], request.form["role"], request.form["address"],
                        photo, request.form["phone"])
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


@app.route('/listmycar', methods=["GET", "POST"])
@login_required
def listmycar():
    models, makes = Model.getDistinctModels()
    fuels = Car.getDistinctFuels()
    types = Car.getDistinctTypes()
    transmissions = Car.getDistinctTransmissions()
    if request.method == "POST":  # Option to include asynchronous developing to predict the cars prices?
        photoFile = request.files.get('file')
        photo = base64.b64encode(photoFile.read())
        heading = request.form('heading')
        price = request.form('price')
        description = request.form('description')
        make = request.form('make')
        if request.form('model') != "Other":
            model = request.form("model")
        else:
            model = request.form("otherModel")  # Yet to be implemented through JQuery
        body_type = request.form('bodyType')
        fuel_type = request.form('fuelType')
        year = request.form('year')
        transmission = request.form('transmission')
        doors = request.form('doors')
        color = request.form('color')
        engine_size = request.form('engineSize')
        insuranceGroup = request.form('insuranceGroup')
        emissions = request.form('emissions')
        mileage = request.form('mileage')
        user_id = current_user.id
        dictCar = {"heading": heading,
                   "price": price,
                   "miles": mileage,
                   "year": year,
                   "make": make,
                   "model": model,
                   "body_type": body_type,
                   "fuel_type": fuel_type,
                   "transmission": transmission,
                   "doors": doors,
                   "exterior_color": color,
                   "photo_url": photo,
                   "insurance_group": insuranceGroup,
                   "engine_size": engine_size,
                   "co2_emission": emissions,
                   "features": description,
                   "user_id": user_id
                   }
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        mycol.insert_one(dictCar)
        if 'predict' in request.data:
            modelLabel, makeLabel, bodyLabel, fuelLabel, colorLabel, transLabel = parseAttributesToLabels(model, make,
                                                                                                          body_type,
                                                                                                          fuel_type,
                                                                                                          color,
                                                                                                          transmission)
            X = [mileage, year, doors, insuranceGroup, engine_size, emissions, makeLabel, modelLabel, colorLabel,
                 fuelLabel,
                 transLabel, body_type]
            regr = carsModel()
            prediction = regr.predict(X)
            predPrice = int(np.exp(prediction))
            return predPrice

    return render_template("submit-property.html", makes=makes, models=models, fuels=fuels, types=types,
                           transmissions=transmissions)


@app.route('/mycars')
@login_required
def mycars():
    carsDicts = Car.getCarsByAttribute("user", current_user.id)
    cars = Car.parseDictToCars(carsDicts)
    return render_template("submit-property.html", cars=cars)


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
