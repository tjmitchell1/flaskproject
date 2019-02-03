from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'probably not very secure'
db = SQLAlchemy(app)

from src import routes, models
