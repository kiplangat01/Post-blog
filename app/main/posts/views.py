from email.mime import image
from pdb import main
from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.main.posts.forms import CommentsForm, Post
from app.models import Posts,Comments
from werkzeug.utils import secure_filename
from app import db, mail
from flask_mail import  Message
from flask import render_template, url_for, flash, redirect, request
posts= Blueprint('posts',__name__)


@posts.route('/')
def home():
    
    # comm=Comments.query.all()
    posts = Posts.query.order_by(Posts.date_created.desc())

    # headline=Posts.query.filter_by(id=1).first()
    

    return render_template('index.html', posts = posts )



@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = Post()
    if form.validate_on_submit():
    
        post = Posts(title=form.title.data,content=form.content.data,description=form.description.data, user_id=current_user.id)

        db.session.add(post)  
        db.session.commit()

        return redirect(url_for('posts.home'))

    else:
          flash('blog not added','danger')
          
    return render_template('post.html', form=form, title='Blog Post')

@login_required
@posts.route('/post/edit/<postid>',methods=['POST', 'GET'])
def post_edit(postid):
    form = Post()

    edites= Posts.query.filter_by(id=postid).first()
    
    if form.validate_on_submit():
        edites.title = form.title.data
        edites.content=form.content.data
        
        edites.description=form.description.data

        db.session.add(edites)
        db.session.commit()
        flash('thanks for your post','success')
        return redirect(url_for("main.home"))
    else:
        form.title.data=edites.title
        form.content.data=edites.content
        
        form.description.data=edites.description
    return render_template('editpost.html',form=form)

@posts.route('/post/delete/<postid>')
def post_delete(postid):
    post = Posts.query.get(postid)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.home'))

@posts.route('/post/<postid>')
def reads(postid):

    reads= Posts.query.get(postid)

    

    return render_template('reads.html', posts=reads)
    

@posts.route('/comments/<id>',methods=['POST', 'GET'])
def comments(id):
    form = CommentsForm()
    posts = Posts.query.filter_by(id=id).first()
    if form.validate_on_submit():
        comment=Comments(comment=form.content.data,post_id=posts.id)
        # posts.comments+=form.content.data + '~'
        db.session.add(comment)
        db.session.commit()
        flash('comment added successfully','success')
        
        return redirect(url_for('posts.home'))
    form.content.data = ""
    return render_template('comments.html', form=form , posts=posts)


@posts.route('/comment/delete/<id>')
def comment_delete(id):
    comm = Comments.query.filter_by(id=id).first()
    
    db.session.delete(comm)
    db.session.commit()
    flash(' comment  deleted successfully','success')

    return redirect(url_for('posts.home'))