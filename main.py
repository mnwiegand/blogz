from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Blog, User
#from hashutils import make_pw_hash
import cgi

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')
    else:
        new_title = request.form['b_title']
        new_body = request.form['b_body']
        if new_title == "" or new_body == "":
            if new_title == "":
                flash("Title was left blank")
                #return redirect('/newpost')
            if new_body == "":
                flash("Body was left blank")
            return redirect('/newpost')

        else:
            new_post = Blog(title = new_title, body = new_body, owner_id = session['user'])
            db.session.add(new_post)
            db.session.commit()
            flash("Congrats, your blog post was successful!")
            new_id = str(new_post.id)
            return redirect('/singleblog?id=' + new_id)

@app.route('/blog', methods = ['GET', 'POST'])
def blog():
    if request.method == 'GET':
    #user query parameter
        posts = Blog.query.filter_by(owner_id=session['user']).all()
        return render_template('singleUser.html', posts = posts, pgtitle="Your Blog Posts")
    if request.method == 'POST':
        return render_template('blog.html')
    
@app.route('/singleblog', methods = ['GET'])
def singleblog():
    singleblog_id = request.args.get('id')
    blog_object = Blog.query.filter_by(id = singleblog_id).first()
    return render_template('singleblog.html', pgtitle = "Individual Blog Post", title = blog_object.title, body = blog_object.body)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.username
                flash('welcome back, '+ user.username)
                return redirect("/")
        flash('bad username or password')
        return redirect("/login")

@app.route('/logout', methods=['POST'])
def logout():
    #delete username from the session
    del session['user']
    return redirect('/blog')

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
                user_val = username)
        if errors == "":
        # direct to welcome page displaying "Welcome, [username]!"
        # return render_template('welcome.html', username_html = username)
        # put collected info into the database
            user = User(username = username, password = passphrase) 
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            return redirect("/")
    else:
        return render_template('signup.html', pgtitle="Sign Up!")

endpoints_without_login = ['login', 'signup', 'index']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/signup")

if __name__ == '__main__':
    app.run()
