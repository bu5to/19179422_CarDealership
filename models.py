from base import Base, Session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Boolean
import os

class User(Base, UserMixin):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    address = Column(String)
    profilePic = Column(String)
    phone = Column(Integer)
    def __init__(self, id, name, email, password, role, address, profilePic, phone):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.address = address
        self.profilePic = profilePic
        self.phone = phone
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_user(username):
        '''
        In this method, the data of the user is retrieved given its username.
        :param username: The username of the user whose information is being retrieved.
        :return: The user as an object with all of its details.
        '''
        users = User.get_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(id):
        '''
        This method follows the same structure as the one before.
        However, here, the ID is the parameter that will be used to search the user.
        :param id: The ID of the user whose information is being retrieved.
        :return: The user as an object with all of its details.
        '''
        users = User.get_users()
        for user in users:
            if user.id == id:
                return user
        return None

    def get_user_by_email(email):
        '''
        This method follows the same structure as the one before.
        However, here, the email is the parameter that will be used to search the user.
        :param email: The email of the user whose information is being retrieved.
        :return: The user as an object with all of its details.
        '''
        users = User.get_users()
        for user in users:
            if user.email == email:
                return user
        return None

class Car:
    def __init__(self, id, make, model, heading, year, mileage, bodyType, fuel, transmission, description, engineSize,
                 color, insuranceGroup, city, emissions, price, images):
        self.id = id
        self.make = make
        self.model = model
        self.heading = heading
        self.year = year
        self.mileage = mileage
        self.bodyType = bodyType
        self.fuel = fuel
        self.transmission = transmission
        self.description = description
        self.engineSize = engineSize
        self.color = color
        self.insuranceGroup = insuranceGroup
        self.city = city
        self.emissions = emissions
        self.price = price
        self.images = images

    def __init__(self, make, model): #Another constructor is created with only the make and the model.
        self.make = make
        self.model = model

    def parseDictToCars(carsDict):
        carslist = []
        for x in carsDict:
            car = Car(x['id'], x['make'], x['model'], x['year'], x['miles'],x['body_type'],x['fuel_type'],
                      x['transmission'], x['features'], x['engine_size'], x['exterior_color'], x['insurance_group'],
                       x['city'], x['co2_emission'], x['price'], x['photo_url'])
            carslist.append(car)
        return carslist

    def getAllCars():
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        carsDicts = mycol.find()
        carslist = Car.parseDictToCars(carsDicts)
        return carslist

    def getCarsByAttribute(attr, value):
        '''
        The aim of this method is to search the cars in the database given a certain attribute and a certain value.
        In order to save several lines of code, it has been decided to build a method that merges all the possible
        search criteria, instead of developing different methods for each attribute.
        :param attr: The attribute that is willing to be searched.
        :param value: The value of the attribute itself.
        :return: The list of cars given the criteria.
        '''
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        if attr == "make":
            carsdicts = mycol.find({"make": value})
        if attr == "model":
            carsdicts = mycol.find({"model": value})
        if attr == "miles":
            carsdicts = mycol.find({"miles": {"$gte":value[0], "$lte":value[1]}})
        if attr == "fuel":
            carsdicts = mycol.find({"fuel": value})
        if attr == "type":
            carsdicts = mycol.find({"type": value})
        if attr == "engine_size":
            carsdicts = mycol.find({"engine_size": {"$gte": value[0], "$lte": value[1]}})
        if attr == "price":
            carsdicts = mycol.find({"price": {"$gte": value[0], "$lte": value[1]}})
        if attr == "year":
            carsdicts = mycol.find({"year": value})
        if attr == "exterior_color":
            carsdicts = mycol.find({"exterior_color": value})
        if attr == "heading":
            carsdicts = mycol.find({"heading": {"$regex" : value}})

        carslist = Car.parseDictToCars(carsdicts)
        return carslist

    def getDistinctModels():
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["models"]
        carslist = []
        carsDicts = mycol.find()
        for x in carsDicts:
            car = Car(x['make'], x['model'])
            carslist.append(car)
        return carslist
