from flask import Flask, render_template, request, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger, swag_from
from flask_restful import Resource, Api
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField


app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'Classifier API',
    'uiversion': 3
}
swagger = Swagger(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
