from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, make_response, \
    send_from_directory
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from base import Session, engine, Base
from models import User, Car, Model
from regression import carsModel, parseAttributesToLabels
from werkzeug.security import generate_password_hash
import numpy as np
import pgeocode
import pyotp
import base64
import os
import pymongo
import random
import string

compress = Compress()


def create_app():
    '''
    This method creates the application and sets up some environment variables that will need to be accessed
    later. Moreover, the application will compress its contents in Gzip.
    Moreover, a new random secret key is instantiated per each user session.
    :return: The created application.
    '''
    app = Flask(__name__)
    app.config["SECRET_KEY"] = ''.join(random.choice(string.ascii_letters) for i in range(64))
    app.config["SECRET_KEY"] = 'secretkey'

    app.config[
        "DATABASE_URL"] = os.environ.get('DATABASE_URL')
    app.config["MONGO_CLIENT"] = os.environ.get('MONGO_CLIENT')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    compress.init_app(app)
    app.config["COMPRESS_REGISTER"] = False
    app.config["COMPRESS_ALGORITHM"] = 'gzip'
    return app


app = create_app()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.before_request
def before_request():
    '''
    HSTS is enabled and the requests starting with HTTP are forced to be replaced with HTTPS.
    :return: Redirect to the new HTTPS URL.
    '''
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@login_manager.user_loader
def load_user(user_id):
    '''
    Implementation of LoginManager in Flask.
    :param user_id: the ID of the user that will be logging in
    :return: The user as an object, with his/her detailed information.
    '''
    users = User.get_users()
    for user in users:
        if user.id == user_id:
            return user
        else:
            return None


@app.route('/sw.js')
def sw():
    '''
    Loads the service worker file within the application.
    :return: The service worker's content as a response.
    '''
    response = make_response(send_from_directory('static', path='assets/sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response


@app.route('/photo/<user_id>')
def photo(user_id):
    '''
    URL that returns the decoded Base64 string as an image containing the profile picture of an user.
    :param user_id: The ID of the user whose picture is intended to be returned.
    :return: The decoded image as a response.
    '''
    user = User.get_user(str(user_id))
    b64_string = user.profilePic
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    image_64_decode = base64.b64decode(b64_string)
    return Response(image_64_decode, mimetype='image/jpg')


@app.route('/carpic/<int:carId>')
def carpic(carId):
    '''
    URL that returns the decoded Base64 string as an image containing the picture of a car.
    :param user_id: The ID of the car whose picture is intended to be returned.
    :return: The decoded image as a response.
    '''
    car = Car.getCarById(carId)
    b64_string = car.images
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    image_64_decode = base64.b64decode(b64_string)
    return Response(image_64_decode, mimetype='image/jpg')


@app.route('/delete/<int:carId>')
@login_required
def delete(carId):
    '''
    Method that deletes a certain car from the database.
    :param carId: The ID of the car that will be deleted.
    :return: The URL containing the cars listed by the user.
    '''
    car = Car.getCarById(carId)
    if car.user_id == current_user.id:
        myclient = pymongo.MongoClient(os.environ.get("MONGO_CLIENT"))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        myquery = {"id": int(carId)}
        mycol.delete_many(myquery)
        return redirect(url_for("mycars"))
    else:
        return redirect(url_for("login"))


@app.route('/edit/<int:carId>', methods=["GET", "POST"])
@login_required
def edit(carId):
    '''
    Method that edits the information of a car listed by the user.
    :param carId: The ID of the car whose information is intended to be edited.
    :return: The form containing the parameters of the car.
    '''
    car = Car.getCarById(carId)
    modelslist, makeslist = Model.getDistinctModels()
    fuels = Car.getDistinctFuels()
    types = Car.getDistinctTypes()
    transmissions = Car.getDistinctTransmissions()
    if request.method == "POST":
        photoFile = request.files.get('file')
        if photoFile.filename != "":
            photo = str(base64.b64encode(photoFile.read()).decode())
        else:
            photo = car.images

        heading = request.form['heading']
        price = int(request.form['price'])
        description = request.form['description']
        make = request.form['make']
        if request.form['model'] != "Other":
            model = request.form["model"]
        else:
            model = request.form["otherModel"]  # Yet to be implemented through JQuery
        body_type = request.form['bodyType']
        fuel_type = request.form['fuelType']
        year = int(request.form['year'])
        transmission = request.form['transmission']
        doors = int(request.form['doors'])
        tax = request.form['tax']
        engine_size = request.form['engineSize']
        insuranceGroup = int(request.form['insuranceGroup'])
        emissions = int(request.form['emissions'])
        mileage = int(request.form['mileage'])
        filter = {'id': carId}
        newvalues = {"$set": {'heading': heading,
                              'price': price,
                              'miles': mileage,
                              'year': year,
                              'make': make,
                              'model': model,
                              'body_type': body_type,
                              'fuel_type': fuel_type,
                              'transmission': transmission,
                              'tax': tax,
                              'doors': doors,
                              'photo_url': photo,
                              'features': description,
                              'engine_size': engine_size,
                              'insurance_group': insuranceGroup,
                              'emissions': emissions
                              }}
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        mycol.update_one(filter, newvalues)
    return render_template("edit-car.html", car=car, makes=makeslist, models=modelslist, fuels=fuels, types=types,
                           transmissions=transmissions)


@app.route('/viewcar/<int:carId>')
@compress.compressed()
def viewcar(carId):
    '''
    Method that allows the user to view the details of a certain car.
    :param carId: The car whose information will be viewed.
    :return: The URL containing the information of the car.
    '''
    car = Car.getCarById(carId)
    seller = User.get_user(car.user_id)
    numCars = len(Car.getCarsByAttribute("user", seller.id))
    similarBodyDict = Car.getCarsByAttribute("type", car.bodyType)
    similarPriceDict = Car.getCarsByAttribute("price", [car.price * 0.8, car.price * 1.2])
    similarCarsDict = [x for x in similarBodyDict if x in similarPriceDict]
    similarCars = random.choices(Car.parseDictToCars(similarCarsDict), k=3)
    return render_template("car.html", car=car, seller=seller, numCars=numCars, similarCars=similarCars)


@app.route('/', methods=["GET", "POST"])
@compress.compressed()
def carsearch():
    '''
    This URL will be used for the main search engine of the website.
    Cars will be searched using this address.
    :return: The main search engine, or the results of a certain query.
    '''
    cars = Car.getAllCars()
    modelslist, makeslist = Model.getDistinctModels()
    fuels = Car.getDistinctFuels()
    types = Car.getDistinctTypes()
    transmissions = Car.getDistinctTransmissions()
    ranges = Car.getPriceAndYearRange()
    if 'user_id' in request.form:
        carsDicts = Car.getCarsByAttribute("user", request.form['user_id'])
        cars = Car.parseDictToCars(carsDicts)
    if request.method == "POST" and 'user_id' not in request.form:
        pricerange = [request.form["minPrice"], request.form["maxPrice"]]
        yearrange = [request.form["minYear"], request.form["maxYear"]]

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
        if request.form["minPrice"] != "" and request.form["maxPrice"] != "":
            priceSearch = Car.getCarsByAttribute("price", [int(pricerange[0]), int(pricerange[1])])
        if request.form["minYear"] != "" and request.form["maxYear"] != "":
            yearSearch = Car.getCarsByAttribute("year", [int(yearrange[0]), int(yearrange[1])])
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

    for car in cars:
        if len(car.description) > 140:
            car.description = car.description[0:140] + "..."
    return render_template('cars.html', cars=cars, makes=makeslist, models=modelslist, fuels=fuels,
                           types=types, ranges=ranges, transmissions=transmissions)


@app.route('/register', methods=["GET", "POST"])
def register():
    '''
    Method that allows a user to create an account.
    :return: The form that the user will use to register.
    '''
    if request.method == "POST":
        if request.files["file"].filename != '':
            photoFile = request.files.get('file')
            photo = str(base64.b64encode(photoFile.read()).decode())
        else:
            photoFile = open('static/assets/img/testuser.jpg', 'rb')
            photo = str(base64.b64encode(photoFile.read()).decode())
        new_user = User(request.form["username"], request.form["name"], request.form["email"],
                        request.form["password"], request.form["role"], request.form["address"],
                        photo, request.form["phone"])
        ses = Session()
        ses.add(new_user)
        ses.commit()
        ses.expunge_all()
        ses.close()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/settings', methods=["GET", "POST"])
def settings():
    '''
    This URL allows the user to update his/her account details.
    :return: A form with the user's account details.
    '''
    if request.method == "POST":
        ses = Session()
        dictupdate = {User.id: request.form['username'],
                      User.name: request.form['name'],
                      User.email: request.form['email'],
                      User.role: request.form['role'],
                      User.address: request.form['address'],
                      User.phone: request.form['phone']
                      }
        query = ses.query(User)
        query.filter(User.id == current_user.id).update(dictupdate, synchronize_session=False)
        ses.commit()
        if request.form["password"] != "":
            if request.form["password"] == request.form["confPassword"]:
                newpassword = generate_password_hash(request.form["password"])
                dictupdate = {User.password: newpassword}
                query.filter(User.id == current_user.id).update(dictupdate, synchronize_session=False)
                ses.commit()
            else:
                flash(u'Passwords do not match.', 'error')
        ses.close()
        return redirect(url_for('settings'))
    return render_template('account-settings.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    '''
    A method that allows the user to log into his/her account.
    :return: The log-in screen, or the 2FA screen, depending if the login is successful or not.
    '''
    if request.method == "POST":
        user = User.get_user(request.form['username'])
        if user is not None and user.check_password(request.form['password']):
            session['username'] = request.form['username']
            print("Session username llega aqui" + session['username'])

            return redirect(url_for('login2fa'))
        else:
            flash(u'Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/login2fa', methods=["GET", "POST"])
def login2fa():
    '''
    This URL serves as a 2-factor authentication step that the user will need to take to log in.
    :return: The 2FA screen, containing the key and a form to introduce an one-time password.
    '''
    if request.method == "POST":
        print("Session username llega aqui" + session['username'])
        pyotpKey = request.form.get("pyotpKey")
        otp = int(request.form.get("otp"))
        otp = pyotp.TOTP(pyotpKey).now()
        if pyotp.TOTP(pyotpKey).verify(otp):
            user = User.get_user(session['username'])
            login_user(user)
            return redirect(url_for('carsearch'))
        else:
            flash("You have supplied an invalid 2FA token!", "error")
            return render_template("2fa.html", pyotpKey=pyotpKey)
    pyotpKey = pyotp.random_base32()
    return render_template("2fa.html", pyotpKey=pyotpKey)


@app.route('/listmycar', methods=["GET", "POST"])
@login_required
def listmycar():
    '''
    An URL through which the user will be able to list his car along with certain details, and predict its price.
    :return: A form at which the user will introduce details on the car intended to be sold...
    or the predicted price, depending on if the user has clicked "Predict" or not.
    '''
    models, makes = Model.getDistinctModels()
    fuels = Car.getDistinctFuels()
    types = Car.getDistinctTypes()
    transmissions = Car.getDistinctTransmissions()
    if request.method == "POST":  # Option to include asynchronous developing to predict the cars prices?
        photoFile = request.files.get('file')
        photo = str(base64.b64encode(photoFile.read()).decode())
        heading = request.form['heading']
        price = int(request.form['price'])
        description = request.form['description']
        make = request.form['make']
        model = request.form["model"]
        body_type = request.form['bodyType']
        fuel_type = request.form['fuelType']
        year = int(request.form['year'])
        transmission = request.form['transmission']
        doors = int(request.form['doors'])
        tax = request.form['tax']
        engine_size = request.form['engineSize']
        insuranceGroup = int(request.form['insuranceGroup'])
        emissions = int(request.form['emissions'])
        mileage = int(request.form['mileage'])
        user_id = current_user.id
        tempAddr = current_user.address.split(" ")
        postcode = tempAddr[-2] + " " + tempAddr[-1]
        nomi = pgeocode.Nominatim('gb')
        city = nomi.query_postal_code(postcode)
        if request.form['submit'] == "Finish":
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
                       "tax": tax,
                       "photo_url": photo,
                       "insurance_group": insuranceGroup,
                       "city": city,
                       "engine_size": engine_size,
                       "co2_emission": emissions,
                       "features": description,
                       "user_id": user_id
                       }
            myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
            mydb = myclient["myapp"]
            mycol = mydb["cars"]
            mycol.insert_one(dictCar)
        if request.form['submit'] == "Predict":
            print("pricepredict")
            makeLabel, modelLabel, fuelLabel, transLabel = parseAttributesToLabels(make, model,
                                                                                   fuel_type,
                                                                                   transmission)
            X = [int(year), int(mileage), int(tax), float(engine_size), float(emissions),
                 makeLabel,
                 modelLabel,
                 fuelLabel,
                 transLabel]
            regr = carsModel()
            prediction = regr.predict([X])
            expPrice = np.exp(prediction)
            predPrice = expPrice.astype(int)[0]
            predPriceMin = (predPrice / 1.01941).astype(int)[0]
            predPriceMax = (predPrice * 1.01941).astype(int)[0]
            flash("Price predicted. Note that this price is an approximated value between " + predPriceMin +
                  and + predPriceMax)
            
            return render_template("submit-car.html", makes=makes, models=models, heading=heading, fuels=fuels,
                                   types=types, year=year,
                                   transmissions=transmissions, make=make, model=model, fueltype=fuel_type,
                                   predPrice=predPrice,
                                   mileage=mileage, body=body_type, transmission=transmission, doors=doors, tax=tax,
                                   insuranceGroup=insuranceGroup, engine_size=engine_size, emissions=emissions,
                                   description=description)

    return render_template("submit-car.html", makes=makes, models=models, fuels=fuels, types=types,
                           transmissions=transmissions)


@app.route('/mycars')
@login_required
def mycars():
    '''
    Through this URL, the user will be able to view details on cars listed by him/her.
    :return: The URL containing details on the cars.
    '''
    carsDicts = Car.getCarsByAttribute("user", current_user.id)
    cars = Car.parseDictToCars(carsDicts)
    for car in cars:
        if len(car.description) > 140:
            car.description = car.description[0:140] + "..."
    return render_template("user-cars.html", cars=cars)


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
    app.run(debug=True)
    #app.run(ssl_context=('cert.pem', 'key.pem'), threaded=True)  # SSL is enabled.
