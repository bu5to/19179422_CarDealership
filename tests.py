import pytest
import pymongo
import time
import random
from base import Session
from models import User
from wsgi import app


@pytest.fixture
def client():
    app.secret_key = 'thisisasecretkey'
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
   # query = session.query(User)
   # query = query.filter(User.id == username).first()
   # session.delete(query)
   # session.commit()
    session.close()
    assert (end - start < 3 and response.status_code == 200)


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
