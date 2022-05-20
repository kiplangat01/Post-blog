from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import table

from app import db,login_manager

@login_manager.user_loader
def login_manager(user_id):
  return User.query.get(int(user_id))

class User(db.Model,UserMixin):
  __tablename__= 'users'
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String,nullable=False,unique=True)
  email=db.Column(db.String,nullable=False,unique=True)
  password=db.Column(db.String,nullable=False)
  post = db.relationship('Posts', backref='author', lazy=True)

  def __repr__(self):
      return f"id: {self.id} , username: {self.username} , email: {self.email} "

class Posts(db.Model):
  
  __tablename__ = 'posts'

  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String)
  description=db.Column(db.String)
  content=db.Column(db.String)
  blog_image=db.Column(db.String)
  category= db.Column(db.String,nullable=False)
  date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  comments = db.relationship('Comments',backref = 'posts',lazy = True)
  def __repr__(self):
      return f"id: {self.id} , title: {self.title}"

class Comments(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  comment=db.Column(db.String)
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

  def __repr__(self):
      return f"id: {self.id} , title: {self.comment}"