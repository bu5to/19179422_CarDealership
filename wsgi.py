from flask import Flask, render_template

import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('properties.html')

@app.route('/register')
def register():
    return render_template('register.html')
	
if __name__ == '__main__':
    app.run()