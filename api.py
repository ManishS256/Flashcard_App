from flask import Flask, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import HTTPException
import json
from datetime import datetime
import random
import os

from flask import current_app as app
from db import *
api=None
api=Api(app)

class InternalServerError(HTTPException):
  def __init__(self,status_code):
    self.response=make_response('',status_code)

class LoginAPI(Resource):
  def get(self,user_name,password):
    try:
      user= Login.query.filter_by(user_name=user_name).first()
    except:
      return 4
    if user:
      if user.password==password:
        return 1
      else:
        return 2
    else:
      return 3

class SignupAPI(Resource):
  def put(self,user_name,password):
    try:
      user= Login.query.filter_by(user_name=user_name).first()
    except:
      return 4
    if user:
      return 2 
    else:
      if '/' in user_name or '/' in password or user_name=='' or password=='' or type(user_name)!=str or type(password)!=str :
        return 3
      else: 
        newuser=Login(user_name=user_name,password=password)
        db.session.add(newuser)
        db.session.commit()
        return 1

class DecksAPI(Resource):
  def get(self,user_name):
    try:
      user= Deck.query.filter_by(user_name=user_name)
    except:
      raise InternalServerError(status_code=500)
    l=[]
    for i in user:
      l.append((i.user_name,i.deck_name,i.last_reviewed,i.score))
    return l

class AdddeckAPI(Resource):
  def put(self,user_name,deck_name):
    try:
      de=Deck.query.filter_by(user_name=user_name,deck_name=deck_name).first()
    except:
      return 3
    if de:
      return 2
    else:
      now = datetime.now()
      dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
      ndeck=Deck(user_name=user_name,deck_name=deck_name,last_reviewed=dt_string,score=0)
      db.session.add(ndeck)
      db.session.commit()
      return 1

class CardsAPI(Resource):
  def get(self,user_name,deck_name):
    try:
      user= Card.query.filter_by(user_name=user_name,deck_name=deck_name)
    except:
      raise InternalServerError(status_code=500)
    l=[]
    for i in user:
      l.append((i.user_name,i.deck_name,i.card_name,i.card_remarks))
    return l

class DeletedeckAPI(Resource):
  def delete(self,user_name,deck_name):
    try:
      Card.query.filter_by(user_name=user_name,deck_name=deck_name).delete()
      db.session.commit()
      Deck.query.filter_by(user_name=user_name,deck_name=deck_name).delete()
      db.session.commit()
      return 1 
    except:
      return 2

class RenamedeckAPI(Resource):
  def put(self,user_name,deck_name,newdeck_name):
    try:
      d=Deck.query.filter_by(user_name=user_name,deck_name=newdeck_name).first()
      if d:
        return 2
      else:
        c=Card.query.filter_by(user_name=user_name,deck_name=deck_name)
        for i in c:
          i.deck_name=newdeck_name
          db.session.commit()
        d=Deck.query.filter_by(user_name=user_name,deck_name=deck_name).first()
        d.deck_name=newdeck_name
        db.session.commit()
        return 1
    except:
      return 3

class AddcardaddAPI(Resource):
  def put(self,user_name,deck_name,card_name,card_remarks):
    try:
      a=Card.query.filter_by(user_name=user_name,deck_name=deck_name,card_name=card_name).first()
      if a:
        return(0)
      else:
        cardadd=Card(user_name=user_name,deck_name=deck_name,card_name=card_name,card_remarks=card_remarks)
        db.session.add(cardadd)
        db.session.commit()
        return(1)
    except:
      raise InternalServerError(status_code=500)

class EditcardAPI(Resource):
  def put(self,user_name,deck_name,card_name,newcard_name,newcard_remarks):
    try:
      Card.query.filter_by(user_name=user_name,deck_name=deck_name,card_name=card_name).delete()
      db.session.commit()
      cardadd=Card(user_name=user_name,deck_name=deck_name,card_name=newcard_name,card_remarks=newcard_remarks)
      db.session.add(cardadd)
      db.session.commit()
      return(1)
    except:
      raise InternalServerError(status_code=500)

class PlayAPI(Resource):
  def get(self,user_name,deck_name):
    try:
      ca=Card.query.filter_by(user_name=user_name,deck_name=deck_name).all()
      leng=len(ca)
      if leng > 0:
        rn=random.randint(0,leng-1)
        playcard_name=ca[rn].card_name
        playcard_remarks=ca[rn].card_remarks
        return ([playcard_name, playcard_remarks])
      else:
        return 0
    except:
        raise InternalServerError(status_code=500)

class DeletecardAPI(Resource):
  def delete(self,user_name,deck_name,card_name):
    try:
      Card.query.filter_by(user_name=user_name,deck_name=deck_name,card_name=card_name).delete()
      db.session.commit()
      return 1
    except:
      raise InternalServerError(status_code=500)

class AddscoreAPI(Resource):
  def put(self,user_name,deck_name,score):
    try:
      de=Deck.query.filter_by(user_name=user_name,deck_name=deck_name).first()
      oldscore=de.score
      newscore=oldscore+int(score)
      de.score=newscore
      db.session.commit()
      now = datetime.now()
      dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
      de1=Deck.query.filter_by(user_name=user_name,deck_name=deck_name).first()
      de1.last_reviewed=dt_string
      db.session.commit()
      return 1
    except:
      raise InternalServerError(status_code=500)

class ImportAPI(Resource):
  def put(self,user_name):
    try:
      fi=open(os.path.join(os.getcwd(),'static/import.csv'),'r')
      fline=fi.readline().strip()
      now = datetime.now()
      dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
      odeck=Deck.query.filter_by(user_name=user_name,deck_name=fline).first()
      if odeck:
        fi.close()
        os.remove(os.path.join(os.getcwd(),'static/import.csv'))
        raise InternalServerError(status_code=406)
      else:
        ndeck=Deck(user_name=user_name,deck_name=fline,last_reviewed=dt_string,score=0)
        db.session.add(ndeck)
        db.session.commit()
        cline=fi.readline()
        while cline!=None:
          l=cline.strip().split(',')
          ncard=Card(user_name=user_name,deck_name=fline,card_name=l[0],card_remarks=l[1])
          db.session.add(ncard)
          db.session.commit()
          cline=fi.readline()
        fi.close()
        os.remove(os.path.join(os.getcwd(),'static/import.csv'))
        return 1
    except:
      raise InternalServerError(status_code=500)

class ExportAPI(Resource):
  def get(self,user_name,deck_name):
    try:
      f=open(os.path.join(os.getcwd(),'static/export.csv'),'w')
      f.write(deck_name+"\n")
      crd=Card.query.filter_by(user_name=user_name,deck_name=deck_name)
      for i in crd:
        f.write("{card_name},{card_remarks}\n".format(card_name=i.card_name,card_remarks=i.card_remarks))
      f.close()
      return 1
    except:
      raise InternalServerError(status_code=500)

api.add_resource(LoginAPI,"/api/login/<string:user_name>/<string:password>")
api.add_resource(SignupAPI,"/api/signup/<string:user_name>/<string:password>")
api.add_resource(DecksAPI,"/api/decks/<string:user_name>")
api.add_resource(AdddeckAPI,"/api/decks/adddeck/<string:user_name>/<string:deck_name>")
api.add_resource(DeletedeckAPI,"/api/decks/deletedeck/<string:user_name>/<string:deck_name>")
api.add_resource(CardsAPI,"/api/decks/addcard/<string:user_name>/<string:deck_name>")
api.add_resource(RenamedeckAPI,"/api/decks/renamedeck/<string:user_name>/<string:deck_name>/<string:newdeck_name>")
api.add_resource(AddcardaddAPI,"/api/decks/addcard/add/<string:user_name>/<string:deck_name>/<string:card_name>/<string:card_remarks>")
api.add_resource(EditcardAPI,"/api/editcard/<string:user_name>/<string:deck_name>/<string:card_name>/<string:newcard_name>/<string:newcard_remarks>")
api.add_resource(PlayAPI,"/api/decks/play/<string:user_name>/<string:deck_name>")
api.add_resource(DeletecardAPI,"/api/decks/deletecard/<string:user_name>/<string:deck_name>/<string:card_name>")
api.add_resource(AddscoreAPI,"/api/decks/play/addscore/<string:user_name>/<string:deck_name>/<int:score>")
api.add_resource(ImportAPI,"/api/decks/import/<string:user_name>")
api.add_resource(ExportAPI,"/api/decks/export/<string:user_name>/<string:deck_name>")