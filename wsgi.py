from flask import Flask, render_template, request, redirect

import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('properties.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form.get("name"))
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')
	
if __name__ == '__main__':
    app.run()