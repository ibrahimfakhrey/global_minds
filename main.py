import json
import os
from datetime import datetime


from flask import Flask, render_template, redirect, url_for, flash, abort, request, current_app, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import uuid

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = User.query.get(int(user_id))
    if user:
        return user
    # If not, check if user is in free_user table

    # If user is not in either table, return None
    return None

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        email = db.Column(db.String(100))
    db.create_all()


class MyModelView(ModelView):
        def is_accessible(self):
            return True


admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
@app.route("/")
def start():
    return render_template("index.html")
@app.route("/dash")
def dash():
    return render_template("profile.html",now=datetime.now())
@app.route("/book")
def book():
    return render_template("book.html")
@app.route("/game")
def game():
    return render_template("page2.html")
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)