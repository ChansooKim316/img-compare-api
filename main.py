from functools import wraps
from flask import Flask
from flask import flash
from flask import Flask, session, redirect, url_for, escape, request, Response
import random
import shutil 
import requests
from PIL import Image
import urllib.request, imagehash



'''
DEBUG MODE

$ export FLASK_ENV=development
$ export FLASK_APP=main
$ flask run

'''



app = Flask(__name__)
app.secret_key = 'secret'
# API Key
api_key = '1234567890'
# Mock-up Database for sessions
db_tokens = []


# def compare_page():
#    return '''
#          <h1>COMPARE</h1>
#          '''

def auth_required(func):
   @wraps(func)
   def verify(*args, **kwargs):
      if (session and session['token'] in db_tokens):
         return func(*args, **kwargs)
      else:
         return redirect(url_for("/"))
   return verify


def verify_api_key(key):
   if key == api_key:
      return True 
   else:
      return False 


def set_token():
   token = random.getrandbits(128)
   # store token in DB
   db_tokens.append(token)
   # Store token in session
   session['token'] = token
   return


# @app.route("/")
# def index():
#    return "the server is running"


@app.route("/", methods = ['GET', 'POST'])
def index():
   if request.method == 'POST':
      # Verify the api key
      if(verify_api_key(request.form['api_key'])):
         # Store the session
         set_token()
         return redirect(url_for('compare'))
      else:
         # When the api key is not valid
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
@auth_required
def compare():
   
   default_url_1 = 'https://static01.nyt.com/images/2019/06/17/science/17DOGS/17DOGS-mobileMasterAt3x-v2.jpg'
   default_url_2 = 'https://i.guim.co.uk/img/media/684c9d087dab923db1ce4057903f03293b07deac/205_132_1915_1150/master/1915.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=14a95b5026c1567b823629ba35c40aa0'

   # Get images from given URLs
   if request.method == 'POST':
      url1 = request.form['url1']
      url2 = request.form['url2']
      image1 = requests.get(url1, stream = True) 
      image2 = requests.get(url2, stream = True) 
      # print('got URLs')
   

      if image1.status_code == 200 and image2.status_code == 200:
         # To avoid image file's size being zero
         image1.raw.decode_content = True
         image2.raw.decode_content = True
         with open('images/image1','wb') as f:
            shutil.copyfileobj(image1.raw, f)
         with open('images/image2','wb') as f:
            shutil.copyfileobj(image2.raw, f)
      # print('downloaded images')
      
      # Read images
      try:
         img1 = Image.open('images/image1')
         img2 = Image.open('images/image2')
      except Exception as err:
         return "<h3>Something went wrong... Please try other URLs.</h3> \n"
      # print('read images')

      # Calculate similarity
      hash1 = imagehash.average_hash(img1)
      hash2 = imagehash.average_hash(img2)
      similarity = 100 - (hash1 - hash2)
      # print('similarity :')
      # print(similarity)

      return '''
            <h1>Similarity : {}%</h1>
            <form action="http://localhost:5000/compare">
               <input type="submit" value="Go back" />
            </form>
            '''.format(similarity)

   return '''
            <form action = "" method = "post">
               <h3>Please enter URLs to compare<h3>
               <p>URL 1 : <input type=text name=url1 value={} size="50"/></p>
               <p>URL 2 : <input type=text name=url2 value={} size="50"/></p>
               <p><input type=submit value=Submit /></p>
            </form>	
         '''.format(default_url_1, default_url_2)
   
