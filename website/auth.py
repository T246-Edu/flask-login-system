from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login.utils import logout_user
from .models import User,Note
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from flask_login import login_required,login_user,current_user
auth  = Blueprint('auth',__name__)

@auth.route('/login',methods = ['GET','POST'])

def login():
    if request.method == "POST":
        email = request.form.get('email')
        passw = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,passw):
                flash("Logged In successfully!",category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password",category="error")
        else:
            flash("User Not Found!",category="error")
    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/sign-up',methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email = email).first()
        if user:
            flash("email already exists",category="error")
        elif len(email) < 4:
            flash("email must be more than 4 charachters.",category="error")
        elif len(first_name) < 4:
            flash("first name must be more than 4 charachters.",category="error")
        elif password1 != password2:
            flash("passwords doesn't match.",category="error")
        elif len(password1) < 7:
            flash("password must be more than 7 charachters.",category="error")
        else:
            new_user = User(email = email,first_name = first_name,password = generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash("Registration Success.",category="success")
            return redirect(url_for('views.home'))
    return render_template('sign_up.html',user=current_user)