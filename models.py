from app import db
#from hashutils import make_pw_hash

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    #blogpost_time = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id

    def __repr__(self):
        return '<Blog %r' %self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blahblahblogz = db.relationship('Blog', backref= 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.hash = make_pw_hash(password)

    def __repr__(self):
        return self.username