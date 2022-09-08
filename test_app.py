import pytest
import base64
import pymongo
import time
import os
import random
from base import Session
from models import User, Car
from wsgi import app


@pytest.fixture
def client():
    app.secret_key = 'thisisasecretkey'
    app.config["MONGO_CLIENT"] = os.environ.get('MONGO_CLIENT')
    client = app.test_client()
    return client


def test_register(client):
    '''
    QR-PE-01: Registering
    After having submitted the form, the registration process should not take longer than 5 seconds.
    :param client: The app client.
    '''
    username = random.randint(1000000000, 9999999999)
    password = random.randint(100000, 999999)

    start = time.time()
    response = client.post("/register", data={
        "username": username,
        "name": "Sample user",
        "email": "sampleuser@gmail.com",
        "file": open('static/assets/img/testuser.jpg', 'rb'),
        "password": password,
        "role": "Dealership",
        "phone": 34600000000,
        "address": "Headington Rd, Headington, Oxford OX3 0BP, United Kingdom",
    }, follow_redirects=True)
    end = time.time()
    session = Session()
    query = session.query(User)
    query = query.filter(User.email == "sampleuser@gmail.com").first()
    session.delete(query)
    session.commit()
    session.close()
    assert (end - start < 5 and response.status_code == 200)


def test_login(client):
    '''
    QR-PE-02: Logging in
    The logging-in process should not take longer than 2 seconds.
    :param client: The app client.
    '''
    username = random.randint(1000000000, 9999999999)
    password = random.randint(100000, 999999)

    response = client.post("/register", data={
        "username": username,
        "name": "Sample user",
        "email": "sampleuser@gmail.com",
        "file": open('static/assets/img/testuser.jpg', 'rb'),
        "password": password,
        "role": "Dealership",
        "phone": 34600000000,
        "address": "Headington Rd, Headington, Oxford OX3 0BP, United Kingdom",
    }, follow_redirects=True)
    start = time.time()
    response = client.post("/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)
    end = time.time()
    session = Session()
    query = session.query(User)
    query = query.filter(User.email == "sampleuser@gmail.com").first()
    session.delete(query)
    session.commit()
    session.close()
    assert (end - start < 2 and response.status_code == 200)


def test_image_encoding():
    '''
    QR-PE-03: Image encoding
    The application will not be provided with a file system to store the cars’ images.
    Alternatively, the submitted files will be converted to a Base64 string.
    This conversion process should not take more than 2 seconds.
    :param client: The app client.
    '''
    start = time.time()
    with open("static/assets/img/testuser.jpg", "rb") as image_file:
        encodedImg = base64.b64encode(image_file.read())
    end = time.time()
    assert (end - start < 2 and encodedImg != "")


def test_image_decoding(client):
    '''
    QR-PE-04: Image decoding
    The Base64 string containing the image will be decompressed when displaying the image in the front end.
    This process of painting the image in the front end should take less than 3 seconds.
    :param client: The app client.
    '''
    start = time.time()
    response = client.get("/photo/19179422")
    end = time.time()
    assert (end - start < 3 and response.status_code == 200)


def test_custom_search(client):
    '''
    QR-PE-05: Custom search
    Certain search tasks will be performed following criteria defined by the user in a form.
    Processing the information, filtering it according to the criteria established, and returning the given search
    in the front-end should not take more than 5 seconds.
    :param client: The app client.
    '''
    response = client.post("/", data={
        "make": "Audi",
        "fuel": "Petrol",
        "keyword": "",
        "model": "",
        "minPrice": 2000,
        "maxPrice": 7000,
        "minYear": 1999,
        "maxYear": 2014,
        "body": ""
    }, follow_redirects=True)
    assert (response.status_code == 200)


def test_alterAd(client):
    '''
    QR-PE-07: Altering an advertisement: The process of changing certain information on an ad should not take longer
    than 2 seconds.
    :param client: The app client.
    '''
    myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
    mydb = myclient["myapp"]
    mycol = mydb["cars"]
    dictcar = {
        "id": 1999999999,
        "heading": "BMW 3 Series 2.0 318d M Sport 4dr",
        "price": 2500,
        "currency_indicator": "GBP",
        "miles": 115950,
        "miles_indicator": "KM",
        "year": 2007,
        "make": "BMW",
        "model": "3 Series",
        "body_type": "Saloon",
        "fuel_type": "Diesel",
        "transmission": "Manual",
        "doors": 4,
        "exterior_color": "Grey",
        "seller_name": "Range Motor",
        "street": "Whitton Road, Hounslow",
        "city": "Hounslow",
        "zip": "TW3 2EB",
        "country": "UK",
        "photo_url": "https://m.atcdn.co.uk/a/media/w1024h768/c7f181b534714dbb8a4521fc92466faa.jpg",
        "insurance_group": "24E",
        "engine_size": 2,
        "co2_emission": 150,
        "features": "Some sample features",
        "photo_links": "https://m.atcdn.co.uk/a/media/w1024h768/c7f181b534714dbb8a4521fc92466faa.jpg",
        "vdp_url": "https://www.rangemotor.co.uk/used-cars/bmw-3-series-2-0-318d-m-sport-4dr-hounslow-202104291983455",
        "user_id": "19179422",
        "tax": 145
    }
    mycol.insert_one(dictcar)
    start = time.time()
    response = client.post("/edit/1999999999", data={
        "file": "",
        "heading": "Petrol",
        "price": 2222,
        "description": "",
        "make": "Make",
        "model": "3 Series",
        "bodyType": "Hatchback",
        "fuelType": "Diesel",
        "year": 2014,
        "transmission": "Manual",
        "doors": 3,
        "tax": 3,
        "engine_size": 3,
        "insuranceGroup": 3,
        "emissions": 3,
        "mileage": 3

    }, follow_redirects=True)
    end = time.time()
    assert end - start < 2 and response.status_code == 200


def test_deleteAd(client):
    # QR-PE-06: Deleting an advertisement: The process of deleting an ad should not take longer than 2 seconds.
    start = time.time()
    response = client.get("/delete/1999999999", follow_redirects=True)
    end = time.time()
    assert end - start < 2 and response.status_code == 200


def test_carMatchesId():
    # Test to verify that the car retrieved from the database matches the car ID.
    carId = 908848246
    car = Car.getCarById(carId)
    assert (car.id == carId)


def test_carMatchesMake():
    # Test to verify that the cars retrieved from the database matches the specified make.
    carsdict = Car.getCarsByAttribute("make", "Audi")
    cars = [x for x in carsdict]
    assert (car.make == "Audi" for car in cars)


def test_carMatchesModel():
    # Test to verify that the cars retrieved from the database match the specified model.
    carsdict = Car.getCarsByAttribute("model", "Fabia")
    cars = [x for x in carsdict]
    assert (car.model == "Fabia" for car in cars)


def test_carMatchesFuelType():
    # Test to verify that the cars retrieved from the database given a fuel type match the specified fuel type.
    carsdict = Car.getCarsByAttribute("fuel", "Diesel")
    cars = [x for x in carsdict]
    assert (car.fuel == "Diesel" for car in cars)


def test_carMatchesPriceRange():
    # Test to verify that the cars retrieved from the database given a price range match the established price range.
    carsdict = Car.getCarsByAttribute("price", [2000, 10000])
    cars = [x for x in carsdict]
    assert (car.price >= 2000 and car.price <= 10000 for car in cars)


def test_carMatchesYearRange():
    # Test to verify that the cars retrieved from the database given a year range match the established year range.
    carsdict = Car.getCarsByAttribute("year", [2010, 2017])
    cars = [x for x in carsdict]
    assert (car.year >= 2010 and car.year <= 2017 for car in cars)


def test_carMatchesMilesRange():
    # Test to verify that the cars retrieved from the database given a mileage range match the established miles range.
    carsdict = Car.getCarsByAttribute("miles", [10000, 40000])
    cars = [x for x in carsdict]
    assert (car.mileage >= 10000 and car.mileage <= 40000 for car in cars)


def test_user_email():
    # Test to verify that the retrieved user given a certain email matches the expected user.
    email = "19179422@brookes.ac.uk"
    user = User.get_user_by_email(email)
    assert user.email == email


def test_username():
    # Test to verify that the retrieved user given a certain ID matches the expected user.
    username = "19179422"
    user = User.get_user(username)
    assert user.id == username
