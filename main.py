from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Blog, User
#TODO: PW hashing!!!
#from hashutils import make_pw_hash
import cgi

#function to ID user in session
def logged_in_blogger():
    blogger = User.query.filter_by(username=session['username']).first()
    return blogger

#function to produce blogs by a certain user in session
def get_blog_list(X):
    blog_list = Blog.query.filter_by(owner_id=X).all
    return blog_list

def author(Y):
    all_authors = User.query.all()
    author = User.query.filter_by(y).all
    return author

@app.route('/', methods = ['POST', 'GET'])
def index():
    all_authors = User.query.all()
    return render_template('index.html', authors= all_authors, pgtitle="Home Page")

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html', pgtitle="What's up?")
    elif request.method == 'POST':
        new_title = request.form['b_title']
        new_body = request.form['b_body']
        if new_title == "" or new_body == "":
            if new_title == "":
                flash("Title was left blank")
            if new_body == "":
                flash("Body was left blank")
            return redirect('/newpost')

        else:
            new_post = Blog(title = new_title, body = new_body, owner_id = logged_in_blogger().id)
            db.session.add(new_post)
            db.session.commit()
            flash("Congrats, your blog post was successful!")
            new_id = str(new_post.id)
            return redirect('/singleblog?id=' + new_id)

@app.route('/blog', methods = ['GET', 'POST'])
def blog():
    #if ('username' in session):
    #    blogger = request.args.get('user')
    #    if blogger:
    #    names_object = User.query.filter_by(id=blogger).first()
    #    name = names_object.username
    #    posts_by_user = Blog.query.filter_by(owner_id=blogger).all()
    #    return render_template('singleUser.html', posts = posts_by_user, pgtitle="All posts by {0}".format(name), authored_by="Written by: {0}".format(name))
    #
    #    else:
    all_posts = Blog.query.all()
    names_object = User.query.all()
    return render_template('singleUser.html', posts = all_posts, pgtitle="All posts")
    #else:
    #    return render_template('singleUser.html', posts = "", pgtitle="Log in to see posts.")

@app.route('/singleblog', methods = ['GET'])
def singleblog():
    singleblog_id = request.args.get('id')
    blog_object = Blog.query.filter_by(id = singleblog_id).first()
    return render_template('singleblog.html', pgtitle = "Individual Blog Post", post = blog_object)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', pgtitle="Log in!")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 0:
            flash('Username "{0}" does not exist yet.' .format(username))
            return redirect("/login")
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['username'] = user.username
                flash('welcome back, '+ user.username)
                return redirect("/")
        flash('bad username or password')
        return redirect("/login")

#Directions asked for a GET request using href... but
@app.route("/logout", methods=['GET'])#'POST' not allowed...
def logout():
    del session['username']
    return redirect("/blog")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['user_name_entry']
        passphrase = request.form['pass_entry1']
        passconfirmation = request.form['pass_entry2']
# this portion checks the username field
        ptag_error1_py=""
        if username == "":
            ptag_error1_py = "This field may not be left blank."
        if not 3 <= len(username) <= 20:
            ptag_error1_py = ptag_error1_py + "Username must be between 3 and 20 characters. "
        if " " in username:
            ptag_error1_py = ptag_error1_py + "Username may not have any spaces. "
        users = User.query.filter_by(username=username)
        if users.count() != 0: #or if any username = any banned name
            ptag_error1_py = ptag_error1_py + "Username taken, please pick a different username."
#this portion checks the password & password verification fields
        ptag_error2_py=""
        if passphrase == "":
            ptag_error2_py = "This field may not be left blank. "
        if not 3 <= len(passphrase) <= 20:
            ptag_error2_py = ptag_error2_py + "Password must be between 3 and 20 characters. "
        if " " in passphrase:
            ptag_error2_py = ptag_error2_py + "Password may not have any spaces. "
        ptag_error3_py=""
        if passconfirmation == "":
            ptag_error3_py = "This field may not be left blank. "
        if not 3 <= len(passconfirmation) <= 20:
            ptag_error3_py = ptag_error3_py + "Password must be between 3 and 20 characters. "
        if passconfirmation != "":
            if " " in passconfirmation:
                ptag_error3_py = ptag_error3_py + "Password may not have any spaces. "
        if passphrase != passconfirmation:
        #redir_error = redir_error + "password entries do not match"
            ptag_error3_py = ptag_error3_py + "Password entries must match. "

        errors = ptag_error1_py + ptag_error2_py + ptag_error3_py

        if errors != "":
        # return redirect("/?error=" + redir_error)
            return render_template('signup.html', methods= ('post'), ptag_error1_html = ptag_error1_py,
                ptag_error2_html = ptag_error2_py, ptag_error3_html = ptag_error3_py,
                user_val = username, pgtitle="Sign Up!")
        if errors == "":
        # direct to welcome page displaying "Welcome, [username]!"
        # return render_template('welcome.html', username_html = username)
        # put collected info into the database
            user = User(username = username, password = passphrase) 
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            return redirect("/newpost")
    else:
        return render_template('signup.html', pgtitle="Sign Up!")

endpoints_without_login = ['login', 'signup', 'index', 'blog', 'singleblog']

@app.before_request
def require_login():
    if not ('username' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

app.secret_key = 'Aas?jdhdguqwy$ag^ajhv!b/vbjhbvj'


if __name__ == '__main__':
    app.run()
