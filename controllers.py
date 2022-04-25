from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import HTTPException
import json
import requests
from datetime import datetime
import random
import os
from flask import current_app as app




@app.route("/",methods=["GET"])
def homepage():
	if request.method=="GET":
		return render_template('homepage.html')

@app.route("/login",methods=["GET","POST"])
def login():
  if request.method=="GET":
    return render_template('loginpage.html')
  if request.method=="POST":
    user_name=request.form.get("u_name")
    password=request.form.get("p_word")
    ans=requests.get("http://127.0.0.1:5000/api/login/{user_name}/{password}".format(user_name=user_name,password=password))
    ans=ans.json()
    if ans==1:
      return redirect('/decks/{user_name}'.format(user_name=user_name))
    elif ans==2:
      return redirect(url_for('notmatching'))
    elif ans==3:
      return redirect(url_for('invalidusername'))
    else:
      raise InternalServerError(status_code=500)

@app.route("/login/invalid_username",methods=["GET"])
def invalidusername():
	if request.method=="GET":
		return render_template('invalidusername.html')

@app.route("/login/notmatching",methods=["GET"])
def notmatching():
	if request.method=="GET":
		return render_template('notmatching.html')

@app.route("/signup",methods=["GET","POST"])
def signup():
  if request.method=="GET":
    return render_template('signup.html')
  if request.method=="POST":
    user_name=request.form.get("u_name")
    password=request.form.get("p_word")
    ans=requests.put("http://127.0.0.1:5000/api/signup/{user_name}/{password}".format(user_name=user_name,password=password))
    ans=ans.json()
    if ans==1:
      return redirect(url_for('accountcreated'))
    elif ans==2:
      return redirect(url_for('useralreadyexist'))
    elif ans==3:
      return render_template('notsufficient.html')
    else:
      raise InternalServerError(status_code=500)

@app.route("/login/accountcreated",methods=["GET","POST"])
def accountcreated():
  if request.method=="GET":
    return render_template('accountcreated.html')

@app.route("/login/useralreadyexist",methods=["GET"])
def useralreadyexist():
  if request.method=="GET":
    return render_template('useralreadyexist.html')

@app.route("/decks/<string:user_name>",methods=["GET"])
def decks(user_name):
  if request.method=="GET":
    url="http://127.0.0.1:5000/api/decks/{user_name}".format(user_name=user_name)
    response=requests.get(url)
    ans=response.json()
    return render_template('deckslist.html',deck=ans,user_name=user_name)

@app.route("/decks/adddeck/<string:user_name>",methods=["GET","POST"])
def adddeck(user_name):
  if request.method=="GET":
    return render_template('adddeck.html',user_name=user_name)
  if request.method=="POST":
    deck_name=request.form.get("deck_name")
    url="http://127.0.0.1:5000/api/decks/adddeck/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    ans=requests.put(url)
    ans=ans.json()
    if ans==1:
      return redirect('/decks/addcard/{user_name}/{deck_name}'.format(user_name=user_name,deck_name=deck_name))
    elif ans==2:
      return redirect("/decks/adddeck/note/{user_name}".format(user_name=user_name))
    else:
      raise InternalServerError(status_code=500)

@app.route("/decks/adddeck/note/<string:user_name>",methods=["GET","POST"])
def deckalreadyexist(user_name):
  if request.method=="GET":
    return render_template('deckalreadyexist.html',user_name=user_name)
  if request.method=="POST":
    deck_name=request.form.get("deck_name")
    url="http://127.0.0.1:5000/api/decks/adddeck/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    ans=requests.put(url)
    ans=ans.json()
    if ans==1:
      return redirect('/decks/addcard/{user_name}/{deck_name}'.format(user_name=user_name,deck_name=deck_name))
    elif ans==2:
      return redirect("/decks/adddeck/note/{user_name}".format(user_name=user_name))
    else:
      raise InternalServerError(status_code=500)

@app.route("/decks/deletedeck/<string:user_name>/<string:deck_name>",methods=["GET"])
def deletedeck(user_name,deck_name):
  if request.method=="GET":
    ans=requests.delete('http://127.0.0.1:5000/api/decks/deletedeck/{user_name}/{deck_name}'.format(user_name=user_name,deck_name=deck_name))
    ans=ans.json()
    if ans==1:
      return redirect('/decks/{user_name}'.format(user_name=user_name))
    else:
      raise InternalServerError(status_code=500)

@app.route("/decks/addcard/<string:user_name>/<string:deck_name>",methods=["GET"])
def addcard(user_name,deck_name):
  if request.method=="GET":
    url="http://127.0.0.1:5000/api/decks/addcard/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    response=requests.get(url)
    ans=response.json()
    return render_template('cardslist.html',card=ans,user_name=user_name,deck_name=deck_name)

@app.route("/decks/renamedeck/<string:user_name>/<string:deck_name>",methods=["GET","POST"])
def renamedeck(user_name,deck_name):
  if request.method=="GET":
    return render_template('renamedeck.html',user_name=user_name,deck_name=deck_name)
  if request.method=="POST":
    newdeck_name=request.form.get("newdeck_name")
    url="http://127.0.0.1:5000/api/decks/renamedeck/{user_name}/{deck_name}/{newdeck_name}".format(user_name=user_name,deck_name=deck_name,newdeck_name=newdeck_name)
    ans=requests.put(url)
    ans=ans.json()
    if ans==1:
      return redirect('/decks/{user_name}'.format(user_name=user_name))
    elif ans==2:
      return redirect('/decks/renamedeck/note/{user_name}/{deck_name}'.format(user_name=user_name,deck_name=deck_name))
    else:
      raise InternalServerError(status_code=500)

@app.route("/decks/renamedeck/note/<string:user_name>/<string:deck_name>",methods=["GET","POST"])
def decknamealreayexist(user_name,deck_name):
  if request.method=="GET":
    return render_template('decknamealreadyexist.html',user_name=user_name,deck_name=deck_name)
  if request.method=="POST":
    newdeck_name=request.form.get("newdeck_name")
    url="http://127.0.0.1:5000/api/decks/renamedeck/{user_name}/{deck_name}/{newdeck_name}".format(user_name=user_name,deck_name=deck_name,newdeck_name=newdeck_name)
    ans=requests.put(url)
    ans=ans.json()
    if ans==1:
      return redirect('/decks/{user_name}'.format(user_name=user_name))
    elif ans==2:
      return redirect('/decks/renamedeck/note/{user_name}/{deck_name}'.format(user_name=user_name,deck_name=deck_name))
    else:
      raise InternalServerError(status_code=500)

@app.route("/decks/addcard/add/<string:user_name>/<string:deck_name>",methods=["GET","POST"])
def addcardadd(user_name,deck_name):
  if request.method=="GET":
    return render_template('addcardadd.html',user_name=user_name,deck_name=deck_name)
  if request.method=="POST":
    card_name=request.form.get("card_name")
    card_remarks=request.form.get("card_remarks")
    url="http://127.0.0.1:5000/api/decks/addcard/add/{user_name}/{deck_name}/{card_name}/{card_remarks}".format(user_name=user_name,deck_name=deck_name,card_name=card_name,card_remarks=card_remarks)
    ans=requests.put(url)
    output=ans.json()
    if output==0:
      return redirect('')
    if output==1:
      url="http://127.0.0.1:5000/api/decks/addcard/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
      response=requests.get(url)
      ans=response.json()
      return render_template('cardslist.html',card=ans,user_name=user_name,deck_name=deck_name)

@app.route("/decks/editdeck/<string:user_name>/<string:deck_name>",methods=["GET"])
def editdeckpage(user_name,deck_name):
  if request.method=="GET":
    url="http://127.0.0.1:5000/api/decks/addcard/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    response=requests.get(url)
    ans=response.json()
    return render_template('cardslist.html',card=ans,user_name=user_name,deck_name=deck_name)
    
@app.route("/decks/editcard/<string:user_name>/<string:deck_name>/<string:card_name>/<string:card_remarks>",methods=["GET","POST"])
def editcard(user_name,deck_name,card_name,card_remarks):
  if request.method=="GET":
    return render_template('editcard.html',user_name=user_name,deck_name=deck_name,card_name=card_name,card_remarks=card_remarks)
  if request.method=="POST":
    newcard_name=request.form.get("newcard_name")
    newcard_remarks=request.form.get("newcard_remarks")
    url="http://127.0.0.1:5000/api/editcard/{user_name}/{deck_name}/{card_name}/{newcard_name}/{newcard_remarks}".format(user_name=user_name,deck_name=deck_name,card_name=card_name,newcard_name=newcard_name,newcard_remarks=newcard_remarks)
    a1=requests.put(url)
    url1="http://127.0.0.1:5000/api/decks/addcard/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    response=requests.get(url1)
    ans=response.json()
    return render_template('cardslist.html',card=ans,user_name=user_name,deck_name=deck_name)

@app.route("/decks/play/<string:user_name>/<string:deck_name>",methods=["GET","POST"])
def play(user_name,deck_name):
  if request.method=="GET":
    url2="http://127.0.0.1:5000/api/decks/play/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    ans=requests.get(url2)
    answ=ans.json()
    if answ==0:
      return redirect("/decks/editdeck/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name))
    else:
      card_name=answ[0]
      card_remarks=answ[1]
      return render_template('flipcard.html',user_name=user_name,deck_name=deck_name,card_name=card_name,card_remarks=card_remarks)
  if request.method=="POST":
    value=request.form.get("Radio")
    if value=="1":
      score=2
    if value=="2":
      score=1
    if value=="3":
      score=0
    url="http://127.0.0.1:5000/api/decks/play/addscore/{user_name}/{deck_name}/{score}".format(user_name=user_name,deck_name=deck_name,score=score)
    ans=requests.put(url)
    return(redirect("/decks/play/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)))

@app.route("/decks/deletecard/<string:user_name>/<string:deck_name>/<string:card_name>",methods=["GET"])
def deletecard(user_name,deck_name,card_name):
  if request.method=="GET":
    url3="http://127.0.0.1:5000/api/decks/deletecard/{user_name}/{deck_name}/{card_name}".format(user_name=user_name,deck_name=deck_name,card_name=card_name)
    output=requests.delete(url3)
    return redirect("/decks/editdeck/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name))

@app.route("/decks/playback/<string:user_name>/<string:deck_name>/<string:card_name>/<string:card_remarks>",methods=["GET"])
def playback(user_name,deck_name,card_name,card_remarks):
  if request.method=="GET":
    return render_template('flipcardback.html',user_name=user_name,deck_name=deck_name,card_name=card_name,card_remarks=card_remarks)

@app.route("/decks/play/<string:user_name>/<string:deck_name>/<string:card_name>/<string:card_remarks>",methods=["GET"])
def playback1(user_name,deck_name,card_name,card_remarks):
  if request.method=="GET":
    return render_template('flipcard.html',user_name=user_name,deck_name=deck_name,card_name=card_name,card_remarks=card_remarks)

@app.route("/decks/import/<string:user_name>",methods=["GET","POST"])
def importdeck(user_name):
  if request.method=="GET":
    return render_template('import.html',user_name=user_name)
  if request.method=="POST":
    try:
      f = request.files['filecsv']
      f.save(os.path.join(os.getcwd(),'static/import.csv'))
      url="http://127.0.0.1:5000/api/decks/import/{user_name}".format(user_name=user_name)
      ans=requests.put(url)
      return redirect("/decks/{user_name}".format(user_name=user_name))
    except:
      raise InternalServerError(status_code=500)


@app.route("/decks/export/<string:user_name>/<string:deck_name>",methods=["GET","POST"])
def exportdeck(user_name,deck_name):
  if request.method=="GET":
    url="http://127.0.0.1:5000/api/decks/export/{user_name}/{deck_name}".format(user_name=user_name,deck_name=deck_name)
    ans=requests.get(url)
    return send_from_directory(os.path.join(os.getcwd(),'static'),'export.csv')