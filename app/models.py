from datetime import datetime
from flask_login import UserMixin
from app import db,login_manager
from app.main.views import comments



@login_manager.user_loader
def login_manager(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    
    # table for the User in the database.
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile = db.Column(db.String, nullable=False, default='anon.png')
    blogs = db.relationship('Blog', backref='author', lazy=True)
    otp = db.relationship('Otp', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='author', lazy=True)



    def __repr__(self):
        return f"id: {self.id} , username: {self.username} "


class Blog(db.Model):
   
    # table for blogs

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f"id: {self.id} , title: {self.title}"

class Otp(db.Model):
    
    
    # Otp table holds the otp sent to user 
    
    id = db.Column(db.Integer, primary_key=True)
    otp=db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comments (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    
