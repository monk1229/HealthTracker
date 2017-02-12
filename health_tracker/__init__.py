from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = "Set to some env variable"
app.debug = True
app.config["DEBUG"] = True

db = SQLAlchemy(app)

# import all files needed
from .root import *
