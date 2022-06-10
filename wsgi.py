from flask import Flask

import base64

app = Flask(__name__)


def index():
    return render_template('index.html')
	
if __name__ == '__main__':
    app.run()