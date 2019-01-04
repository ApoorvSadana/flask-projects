from flask import Flask, render_template,request,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

app = Flask(__name__)

engine = create_engine("postgres://bjkgewndzendmj:8e75c4f5331dbd372a4d8339f505b0f481713a9658820f4526f7259545aff383@ec2-54-225-89-156.compute-1.amazonaws.com:5432/d44ast3pp7of22")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form.get("Username")
	password = request.form.get("Password")
	if db.execute("SELECT * FROM users WHERE username=:username", 
		{"username": username}).rowcount == 0:
		return render_template("message_layout.html",message="Not Registered!")
	elif db.execute("SELECT * FROM users WHERE username=:username AND password=:password", 
		{"username": username,"password":password}).rowcount == 0:
		return render_template("message_layout.html",message="Wrong Password!")
	else:
		return render_template("message_layout.html",message="Succesfuly Logged In!")

	

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/add", methods=["POST"])
def add():
	username = request.form.get("Username")
	password = request.form.get("Password")
	if db.execute("SELECT * FROM users WHERE username=:username", {"username": username}).rowcount != 0:
		return render_template("message_layout.html",message="Already Registered wih this Name!")
	db.execute("INSERT INTO users (username,password) VALUES (:username,:password)", 
		{"username": username, "password": password})
	db.commit()
	return render_template("message_layout.html",message="Succesfuly Registered!")

if __name__ == '__main__':
	os.system("start \"\" http://127.0.0.1:5000/")
	app.run()