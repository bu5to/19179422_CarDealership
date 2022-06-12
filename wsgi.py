from flask import Flask, render_template, request, redirect
from base import Session, engine, Base
from models import User, Car

import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('properties.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(request.form["username"],request.form["name"],request.form["email"],
                        request.form["password"],request.form["role"],request.form["address"],
                        request.form["profilePic"],request.form["phone"])
        session.add(new_user)
        session.commit()
        session.expunge_all()
        session.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')
	
if __name__ == '__main__':
    app.run()