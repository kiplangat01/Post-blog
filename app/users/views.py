from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from app.users.forms import Register, Login,UpdateAccountForm
from app import db,mail
from flask_mail import  Message
from werkzeug.security import generate_password_hash,check_password_hash
from app.models import Posts, User


users = Blueprint('users', __name__)

@users.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    form = Register()
    if form.validate_on_submit():
      hashed_password = generate_password_hash(form.password.data).decode('utf8')
      user=User(username=form.username.data,email=form.email.data,password=hashed_password)
      db.session.add(user)
      db.session.commit()
      flash('Account Successfully Created! ','success')
      return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['POST', 'GET'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username.title()} !! ', 'success')
            # args is a dict
            # get returns none if the next key does not exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('posts.home'))

# @users.route('/subscribe', methods=['POST', 'GET'])
# def subscribe():
#     form=Subscribe()
#     if form.validate_on_submit():
        
        
#         db.session.add(sub)
#         db.session.commit()
#         msg=Message("WELCOME",sender="apollolibrary99@gmail.com",recipients=[sub.email])
#         msg.body = "Welcome to H&J's Blog you Have Subscribed News Letter we will loop you on all newly updates"
#         mail.send(msg)
     
#         flash('Your  Has Joined H&J Blog Subscription  ','success')
#         return redirect(url_for('main.home'))


#     return render_template('subscribe.html',form=form)

@users.route('/account',methods=['POST', 'GET'])
@login_required
def account():
    """
    """
    post= Posts.query.filter_by(user_id=current_user.id)
    form=UpdateAccountForm()
    if form.validate_on_submit():

        current_user.username=form.username.data
        current_user.email=form.email.data

        db.session.commit()
        flash('Your Account Has been updated!','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':

        form.username.data=current_user.username
        form.email.data=current_user.email
    
   
    return render_template('account.html', title='Account',form=form,post=post )
