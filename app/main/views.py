from app.models import User, Posts, Comments
from flask import render_template, Blueprint
from flask import render_template, url_for, flash, redirect, request
from sqlalchemy import asc, desc
# from app import get_random_quote

main = Blueprint('main', __name__)


@main.route('/')
def home():
    
    # comm=Comments.query.all()

    # headline=Posts.query.filter_by(id=1).first()
    

    return render_template('index.html')
