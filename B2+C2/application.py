from flask import Flask, render_template,request,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import os

app = Flask(__name__)

engine = create_engine("postgres://bjkgewndzendmj:8e75c4f5331dbd372a4d8339f505b0f481713a9658820f4526f7259545aff383@ec2-54-225-89-156.compute-1.amazonaws.com:5432/d44ast3pp7of22")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	members = db.execute("SELECT * FROM members")
	return render_template("index.html", members = members)

@app.route("/add_member",methods=["POST"])
def add_member():
	name = request.form.get("name")
	age = request.form.get("age")
	db.execute("INSERT INTO members (name,age) VALUES (:name,:age)",{"name":name,"age":age})
	db.commit()
	members = db.execute("SELECT * FROM members")
	return redirect(url_for("index"))

@app.route("/remove",methods=["POST"])
def remove():
	for key in request.form:
		btn_name = key
	db.execute("DELETE FROM members WHERE sno = :btn_name",{"btn_name":btn_name})
	db.commit()
	return redirect(url_for("index"))

if __name__ == '__main__':
	os.system("start \"\" http://127.0.0.1:5000/")
	app.run()

