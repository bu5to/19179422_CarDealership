from base import Base, Session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String
import os
import pymongo

class User(Base, UserMixin):
    __tablename__='user'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    address = Column(String)
    profilePic = Column(String)
    phone = Column(String)

    def __init__(self, id, name, email, password, role, address, profilePic, phone):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.address = address
        self.profilePic = profilePic
        self.phone = phone

    def get_users():
        '''
        An array of the registered users is retrieved in this method.
        :return: The array that contains the information in every user.
        '''
        session_users = Session()
        users = session_users.query(User)
        users = users.all()
        print(users)
        return users

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
            if user.id == username:
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


class Model:
    def __init__(self, make, model): #Another constructor is created with only the make and the model.
        self.make = make
        self.model = model

    def getDistinctModels():
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["models"]
        carslist = []
        makeslist = []
        carsDicts = mycol.find()
        for x in carsDicts:
            car = Model(x['brand'], x['model'])
            carslist.append(car)
            if x['brand'] not in makeslist:
                makeslist.append(x['brand'])
        return carslist, makeslist



class Car:
    def __init__(self, id, make, model, heading, year, mileage, bodyType, fuel, transmission, description, engineSize,
                 color, insuranceGroup, city, emissions, price, images, user_id):
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
        self.user_id = user_id


    def getPriceAndYearRange():
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        minprice = mycol.find_one(sort=[("price", 1)])["price"]
        maxprice = mycol.find_one(sort=[("price", -1)])["price"]
        minyear = mycol.find_one(sort=[("price", 1)])["year"]
        maxyear = mycol.find_one(sort=[("price", -1)])["year"]
        ranges = [minyear, maxyear, minprice, maxprice]
        return ranges


    def parseDictToCars(carsDict):
        carslist = []
        for x in carsDict:
            keyPhoto = "photo_url" #Some cars are not provided with images
            keyColor = "exterior_color"  # Some cars are not provided with images
            if keyPhoto in x and keyColor in x:
                car = Car(x['id'], x['make'], x['model'], x['heading'], x['year'], x['miles'],x['body_type'],x['fuel_type'],
                          x['transmission'], x['features'], x['engine_size'], x['exterior_color'], x['insurance_group'],
                           x['city'], x['co2_emission'], x['price'], x['photo_url'], x['user_id'])
                carslist.append(car) #Provisional solution until dataset is fixed
        return carslist


    def getAllHeadings():
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        carsDicts = mycol.find()
        headings = []
        for x in carsDicts:
            headings.append(x['heading'])
        return headings


    def getAllCardicts():
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        carsDicts = list(mycol.find())
        return carsDicts


    def getAllCars():
        carsDicts = Car.getAllCardicts()
        carslist = Car.parseDictToCars(carsDicts)
        for car in carslist:
            if "w1024h768" in car.images:
                car.images = car.images.replace("w1024h768", "w400h300")
        return carslist


  #  def getLatestCars():
   #     carsDicts = Car.getAllCardicts()
    #    carslist = Car.parseDictToCars(carsDicts)[-2:]
     #   latestCarsCookie = carslist[0].id + ":" + carslist[1].id + ":" + carslist[2].id
      #  return latestCarsCookie


    def getDistinctFuels():
        cars = Car.getAllCars()
        fuels = []
        for car in cars:
            if car.fuel not in fuels:
                fuels.append(car.fuel)
        return fuels

    def getDistinctTransmissions():
        cars = Car.getAllCars()
        transmissions = []
        for car in cars:
            if car.transmission not in transmissions:
                transmissions.append(car.transmission)
        return transmissions

    def getDistinctTypes():
        cars = Car.getAllCars()
        types = []
        for car in cars:
            if car.bodyType not in types:
                types.append(car.bodyType)
        return types

    def getCarById(carId):
        myclient = pymongo.MongoClient(os.environ.get('MONGO_CLIENT'))
        mydb = myclient["myapp"]
        mycol = mydb["cars"]
        cardict = mycol.find_one({"id": int(carId)})
        print(cardict)
        car = Car(cardict['id'], cardict['make'], cardict['model'], cardict['heading'], cardict['year'],
                  cardict['miles'], cardict['body_type'], cardict['fuel_type'],
                  cardict['transmission'], cardict['features'], cardict['engine_size'], cardict['exterior_color'],
                  cardict['insurance_group'],
                  cardict['city'], cardict['co2_emission'], cardict['price'], cardict['photo_url'], cardict['user_id'])
        return car

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
            carsdicts = list(mycol.find({"make": value}))
        if attr == "model":
            carsdicts = list(mycol.find({"model": value}))
        if attr == "miles":
            carsdicts = list(mycol.find({"miles": {"$gte":value[0], "$lte":value[1]}}))
        if attr == "fuel":
            carsdicts = list(mycol.find({"fuel_type": value}))
        if attr == "user":
            carsdicts = list(mycol.find({"user_id": value}))
        if attr == "type":
            carsdicts = list(mycol.find({"body_type": value}))
        if attr == "engine_size":
            carsdicts = list(mycol.find({"engine_size": {"$gte": value[0], "$lte": value[1]}}))
        if attr == "price":
            carsdicts = list(mycol.find({"price": {"$gte": value[0], "$lte": value[1]}}))
        if attr == "year":
            carsdicts = list(mycol.find({"year": {"$gte": value[0], "$lte": value[1]}}))
        if attr == "exterior_color":
            carsdicts = list(mycol.find({"exterior_color": value}))
        if attr == "heading":
            carsdicts = list(mycol.find({"heading": {"$regex" : value}}))
        if attr == "description":
            carsdicts = list(mycol.find({"features": {"$regex" : value}}))

        #carslist = Car.parseDictToCars(carsdicts)
        return carsdicts

