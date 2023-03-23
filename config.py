#configs or settings are here
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)

app.secret_key = 'hello'