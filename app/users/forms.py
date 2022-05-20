from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,RadioField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from app.models import User
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class Register(FlaskForm):
    
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])

    submit = SubmitField('Signup')

    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(
                "username already taken")

    def validate_email(self, email):
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "email is already taken!")


class Login(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Subscribe(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')


class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])
     
    picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    Submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("username is taken")

    def validate_email(self, email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("email is taken")
