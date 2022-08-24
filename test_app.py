import pytest
import base64
import pymongo
import time
import os
import random
from flask_login import login_user
from base import Session
from models import User
from wsgi import app


@pytest.fixture
def client():
    app.secret_key = 'thisisasecretkey'
    app.config["MONGO_CLIENT"] = os.environ.get('MONGO_CLIENT')
    client = app.test_client()
    # with client.session_transaction(subdomain='blue') as session:
    #   session['user'] = 19179422
    return client


def test_register(client):
    '''
    QR-PE-01: Registering
    After having submitted the form, the registering process should not take longer than 5 seconds.
    :param client:
    :return:
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
    }, follow_redirects = True)
    end = time.time()
    session = Session()
    query = session.query(User)
    query = query.filter(User.email == "sampleuser@gmail.com").first()
    session.delete(query)
    session.commit()
    session.close()
    assert (end - start < 3 and response.status_code == 200)


def test_login(client):
    '''
    QR-PE-02: Logging in
    The logging-in process should not take longer than 2 seconds.
    :param client:
    :return:
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
    }, follow_redirects = True)
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
    :param client:
    :return:
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
    :param client:
    :return:
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
    :param client:
    :return:
    '''
    start = time.time()
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
    end = time.time()
    assert (end - start < 5 and response.status_code == 200)


def test_alterAd(client):
    #QR-PE-07: Altering an advertisement: The process of changing certain information on an ad should not take longer than 2 seconds.
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
        "features": "Adjustable Steering Column/Wheel|Alloy Wheels (17in)|Air-Conditioning (Automatic)|Body Coloured Bumpers|Computer (Driver Information System)|Mirrors External (Electric Folding)|Cruise Control||Electric Windows (Front/Rear)||In Car Entertainment (Radio/CD)||Mirrors Internal||Seat Height Adjustment||Speakers||Steering Wheel Mounted Controls||Upholstery Cloth/Leather||Air Bag Driver|Air Bag Passenger|Air Bag Side|Central Door Locking|Centre Rear Seat Belt|Front Fog Lights|Head Air Bags|Head Restraints|Immobiliser|Parking Aid (Rear)|Power-Assisted Steering|Seat - ISOFIX Anchorage Point (Two Seats - Rear)|Traction Control System",
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
    #QR-PE-06: Deleting an advertisement: The process of deleting an ad should not take longer than 2 seconds.
    start = time.time()
    response = client.get("/delete/1999999999", follow_redirects=True)
    end = time.time()
    assert end - start < 2 and response.status_code == 200