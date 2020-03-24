from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np

#Sql
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session,sessionmaker
#from passlib.hash import sha256_crypt

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template,session,logging,url_for,redirect,flash
from werkzeug.utils import secure_filename


#engine = create_engine("mysql+pymysql://root:2298@localhost/register")
#db=scoped_session(sessionmaker(bind=engine))
app=Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

#register form
@app.route("/register",methods=["GET","POST"])
def register():
	"""if request.method == "POST":
		name=request.form.get("name")
		username=request.form.get("username")
		password=request.form.get("password")
		confirm=request.form.get("confirm")
		secure_password = sha256_crypt.encrypt(str(password))

		if password == confirm:
			db.execute("INSERT INTO users(name,username,password) values(:name,:username,:password)",{"name":name,"username":username,"password":password})
			db.commit()
			flash("You are registred and can Login","success")
			return redirect(url_for('Login'))
		else:
			flash("password does not match","danger")
			return render_template("register.html")"""

	return render_template("register.html")


@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == 'admin'and password=='admin':
            flash("You are logged in","success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect password","danger")
            return render_template("login.html")
				
    return render_template("login.html")

# Model saved with Keras model.save()
MODEL_PATH = 'NewCustomVgg.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')

#img_path='C:\\Users\\Admin\\Example\\example1\\venv\\app\\uploads'
def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    #x = preprocess_input(x, mode='keras')
    import cv2
    preds = model.predict(x)
    return preds

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        pred_class = preds#.argmax()#(axis=-1)            # Simple argmax
        #pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        result = str(pred_class)               # Convert to string
        return result
    return None


if __name__ == '__main__':
	app.secret_key="1234567dailywebcoding"
	app.run(debug=True)