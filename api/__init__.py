from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
ma = Marshmallow(app)




from . import views


