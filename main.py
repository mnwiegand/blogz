from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bloggy456@localhost:8889/build-a-blog'
app.config['SQLACHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'bloggy@123'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    #blogpost_time = db.Column(db.Date)
    #owner_id = db.Column(db.Integer, db.ForeignKey('blogger.id'))

#    def __init__(self, title, blogpost):
#        self.title = title
#        self.body = body

#    def __repr__(self):
#            return '<Blogpost %r' %self.title

#class Blogger(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    email = db.Column(db.String(120), unique = True)
#    password = db.Column(db.String(120))
    #body = db.relationship('Blog', backref= 'owner')

#    def __init__(self, email, password):
#        self.email = email
#        self.password = password

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('base.html')

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')
    else:
        new_title = request.form['b_title']
        if new_title == "":
            flash("Title was left blank")
            #return redirect('/newpost')

        new_body = request.form['b_body']
        if new_body == "":
            flash("Body was left blank")
            return redirect('/newpost')

        else:
            new_post = Blog(title = new_title, body = new_body )
            db.session.add(new_post)
            db.session.commit()
            flash("Congrats, your blog post was successful!")
            new_id = str(new_post.id)
            return redirect('/singleblog?id=' + new_id)

@app.route('/blog', methods = ['GET'])
def blog():
    posts = Blog.query.all()
    return render_template('blog.html', posts = posts)
    #, blogtitle= Blogpost.blogtitle, blogpost = Blogpost.blogpost)

@app.route('/singleblog', methods = ['GET'])
def singleblog():
    singleblog_id = request.args.get('id')
    blog_object = Blog.query.filter_by(id = singleblog_id).first()

    #return render_template('welcome.html', methods = ('post'), username_html = name)
    return render_template('singleblog.html', title = blog_object.title, body = blog_object.body)

if __name__ == '__main__':
    app.run()
