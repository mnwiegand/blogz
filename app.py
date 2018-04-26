from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzy2018@localhost:8889/blogz'
app.config['SQLACHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'bloggzzzy123'