from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///deck.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy()
db.init_app(app)

class Login(db.Model):
    __tablename__='login'
    user_name=db.Column(db.String, primary_key=True, nullable=False, unique=True)
    password=db.Column(db.String, nullable=False)

class Deck(db.Model):
  __tablename__='deck'
  user_name=db.Column(db.String, db.ForeignKey("login.user_name"), primary_key=True, nullable=False)
  deck_name=db.Column(db.String, primary_key=True, nullable=False)
  last_reviewed=db.Column(db.String)
  score=db.Column(db.String)

class Card(db.Model):
  __tablename__='card'
  user_name=db.Column(db.String, primary_key=True, nullable=False)
  deck_name=db.Column(db.String, primary_key=True, nullable=False)
  card_name=db.Column(db.String, primary_key=True, nullable=False)
  card_remarks=db.Column(db.String)