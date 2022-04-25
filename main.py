from flask import Flask

app=None
app =Flask(__name__,template_folder='templates',static_folder='static')
app.app_context().push()

from db import *
from api import *
from controllers import *

if __name__ =="__main__":
  app.debug=True
  app.run(host='0.0.0.0',port='5000')