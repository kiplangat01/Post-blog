from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from .forms import Register, Login, ResetPassword, UpdateAccountForm, VerifyOtp, ForgotPassword
from app import db, bcrypt, mail
from app.main.forms import BlogForm, CommentsForm
from flask_mail import Message
import random
import math
from app.models import *


posts = Blueprint('posts', __name__)
main = Blueprint('main', __name__)


@main.route('/')
def home():
    # blog = Blog.query.all()

    return render_template('index.html')


users = Blueprint('Users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account Has been Created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/authentification/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username.title()} !! ', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('incorect email or password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():

    blog = Blog.query.filter_by(user_id=current_user.id)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your Account Has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profiles/'+current_user.profile)
    return render_template('account.html', title='Account', image_file=image_file, form=form, blog=blog)


@users.route('/forgot/password', methods=['POST', 'GET'])
def forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = generate_token(6)
        otp = Otp(otp=token, user_id=user.id)
        db.session.add(otp)
        db.session.commit()
        if user:
            msg = Message(
                "Hello", sender="apollolibrary99@gmail.com", recipients=[user.email])
            msg.body = token
            mail.send(msg)
            flash('check your')
            return redirect(url_for('users.verify_otp', userid=user.id))

    return render_template('recover.html', form=form)


@users.route('/otp-verify/<userid>', methods=['POST', 'GET'])
def verify_otp(userid):
    form = VerifyOtp()
    user = User.query.filter_by(id=userid).first()
    token = Otp.query.filter_by(user_id=userid).first()

    if form.validate_on_submit():

        if form.otp.data != token.otp:
            flash('InCorrect otp')
        else:
            flash('Correct otp')
            u = db.session.get(Otp, 1)
            db.session.delete(u)
            db.session.commit()
            return redirect(url_for('users.reset', userid=user.id))

    return render_template('verify.html', form=form)


def generate_token(length):
    digits = [i for i in range(0, 10)]

    token = ""
    for i in range(length):
        index = math.floor(random.random()*10)
        token += str(digits[index])
    return token


@users.route('/reset_password/<userid>', methods=['POST', 'GET'])
def reset(userid):
    form = ResetPassword()
    user = User.query.filter_by(id=userid).first()

    if form.validate_on_submit():
        if user.password != form.password.data:
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('passwords cannot be the same as old')
    return render_template('reset.html', form=form)


@posts.route('/comments/<id>', methods=['POST', 'GET'])
@login_required
def comments(id):
    form = CommentsForm()
    blog = Blog.query.filter_by(id=id).first()
    if form.validate_on_submit():
        blog.comments += form.content.data + '~'
        db.session.commit()
        flash('thanks for your reaction')
        db.session.commit()

    form.content.data = "Your comment"
    return render_template('comments.html', form=form, blog=blog)


# Endpoint for deleting a record
@posts.route("/Blog/<id>", methods=["DELETE"])
def guide_delete(id):
    form = Blog.query.filter_by(id=id).first()
    db.session.delete(Blog)
    if form.validate_on_submit():
        db.session.commit()

    return redirect(url_for('main.home'))
