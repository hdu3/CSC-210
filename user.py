import sys
import os;
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask import Blueprint
auth = Blueprint('auth', __name__)

from flask import render_template, redirect, request
from flask import url_for, flash
from flask_login import login_user, logout_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


app = Flask(__name__)

appdir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = \
  f"sqlite:///{os.path.join(appdir, 'user.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="ADFGAERTASDFAGT245242WEF"

db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = "Users"
  user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  password = db.Column(db.Unicode(64), nullable=False)
  email = db.Column(db.Unicode(64), nullable=False)
  firstname = db.Column(db.Unicode(64), nullable=False)
  lastname = db.Column(db.Unicode(64), nullable=False)
  age = db.Column(db.Integer(), nullable=False)
  phone = db.Column(db.Unicode(64), nullable=False)
  country = db.Column(db.Unicode(64), nullable=False)
  gender = db.Column(db.Unicode(64), nullable=False)
  tokens = db.relationship("Tokens", backref="user_id")

def add_user (password, email, firstname, lastname, age, phone, ccountry, gender):
	newuser = User(password=generate_password_hash(password), email=email, firstname=firstname, lastname=lastname, age=age, phone=phone,country=country, gender=gender)
	db.session.add(newuser)
	db.session.commit()


@app.route("/")
def home():
  return render_template("index.html")
	
@app.route("/signup", methods=["GET","POST"])
def signup():
  if request.method == 'POST':
    try:
      email = request.form['email']
      password = request.form['password']
      add_user(email, password)
      return redirect(url_for("home"))
    return render_template("signup.html")
  else:
    return render_template("signup.html")

	
@app.route("/login", methods=["GET","POST"])
def login():
  if request.method == 'POST':
    try:
      email = request.form['email']
      user = User.query.filter_by(email=form.email.data).first()
      if user is not None and user.verify_password(request.form['password']):
        login_user(user)
        flash("Logged in!")
        return redirect(url_for("home"))
      return render_template("login")
    return render_template("login")
  else:
    return render_template("login.html")
  

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))

def verify_password(self, password):
  return check_password_hash(self.password, password)

