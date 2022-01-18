from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Custom_model(db.Model):
    def migrate(self):
        pass

class Screen(Custom_model):
    PAGE = 0
    SURVEY = 1
    CAROUSEL = 2
    TYPE = {
        PAGE: 'page',
        SURVEY: 'survey',
        CAROUSEL: 'carousel',
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    text = db.Column(db.String(255), unique=True)
    link = db.Column(db.String(255), unique=True)
    custom_view = db.Column(db.Boolean, default=False, nullable=False)
    def_name = db.Column(db.String(500), unique=False)
    buttons = db.Column(JSON)
    type = db.Column(db.SmallInteger, default=TYPE)

    def __init__(self, username, email):
        # self.email = email
        pass

    def __repr__(self):
        return '<Screen %r>' % self.name