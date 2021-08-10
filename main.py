from functools import wraps
from flask import Flask
from flask import flash
from flask import Flask, session, redirect, url_for, escape, request
import random

'''
$ export FLASK_APP=main
$ flask run

'''



app = Flask(__name__)
app.secret_key = 'secret-key'
# API Key
api_key = '1234567890'
# Mock-up Database
db_tokens = []


def login(f):
   @wraps(f)
   def verify():
      if(session and session['token'] in db_tokens):
         pass
      else:
         print('auth required')
         return redirect(url_for('auth'))
   return verify



def require_auth():
   # Check if token is exist
   print('all sessions')
   print(session)
   if(session):
      if(session['token'] in db_tokens):
         return True
   else:
      print('auth required')
      return False


def verify_api_key(key):
   #
   if key == api_key:
      return True 
   else:
      return False 


def set_token():
   token = random.getrandbits(128)
   # store token in DB
   db_tokens.append(token)
   # Store token in Cookie
   session['token'] = token
   return


@app.route("/")
def index():
   return "the server is running"


@app.route("/auth", methods = ['GET', 'POST'])
def auth():
   if request.method == 'POST':
      # Verify the api key
      if(verify_api_key(request.form['api_key'])):
         # Store the session
         set_token()
         return redirect(url_for('compare'))
      else:
         return '''
               <form action = "" method = "post">
                  <h3 style="color:red;">Invalid api key. Please try again.</h3>
                  <p>Username : user1</p>
                  <p>API Key : <input type = text name = api_key value='1234567890' /></p>
                  <p><input type = submit value = Login /></p>
               </form>	
                '''

   return '''
            <form action = "" method = "post">
               <h3>Please enter the API Key<h3>
               <p>Username : user1</p>
               <p>API Key : <input type = text name = api_key value='1234567890' /></p>
               <p><input type = submit value = Login /></p>
            </form>	
         '''


@app.route("/compare", methods = ['GET', 'POST'])
@login
def compare():
   print('all sessions')
   print(session)
   return 'logged-in'
   #  return '''
   #          <form action = "" method = "post">
   #             <h3>URLs<h3>
   #             <p>images</p>
   #             <p>URL 1 : <input type = text name = url1 value='some url' /></p>
   #             <p>URL 2 : <input type = text name = url2 value='some url' /></p>
   #             <p><input type = submit value = Login /></p>
   #          </form>	
   #       '''