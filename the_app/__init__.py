from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from the_app import routes