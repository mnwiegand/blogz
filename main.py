from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bloggy456@localhost:8889/build-a-blog'
app.config['SQLACHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'bloggy@123'

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blogtitle = db.Column(db.String(120))
    blogpost = db.Column(db.String(400))
    #blogpost_time = db.Column(db.Date)
    #owner_id = db.Column(db.Integer, db.ForeignKey('blogger.id'))

#    def __init__(self, blogtitle, blogpost):
#        self.blogtitle = blogtitle
#        self.blogpost = blogpost

#    def __repr__(self):
#            return '<Blogpost %r' %self.blogtitle

#class Blogger(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    email = db.Column(db.String(120), unique = True)
#    password = db.Column(db.String(120))
    #blogposts = db.relationship('BlogPost', backref= 'owner')

#    def __init__(self, email, password):
#        self.email = email
#        self.password = password

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('newpost.html')

@app.route('/newpost', methods = ['POST'])
def newpost():
    new_title = request.form['b_title']
    new_body = request.form['b_body']
    new_post = Blogpost(blogtitle = new_title, blogpost = new_body )
    db.session.add(new_post)
    db.session.commit()
    return render_template('confirm_new_post.html')

@app.route('/blog', methods = ['POST', 'GET'])
def blog():
    posts = Blogpost.query.all()
    return render_template('blog.html', posts = posts)
    #, blogtitle= Blogpost.blogtitle, blogpost = Blogpost.blogpost)

#privacy settings for certain blog posts?
#@app.before_request
#def require_login():
#   allowed_routes = ['login', 'register']
#   if request.endpoint not in allowed_routes and 'email' not in session:
#       return redirect('/login')






if __name__ == '__main__':
    app.run()
