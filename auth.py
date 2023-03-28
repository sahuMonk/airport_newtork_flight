from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import UserModel,db
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('id')
    password = request.form.get('password')

    user = UserModel.query.filter_by(id=id).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user)
    if current_user.role == 'admin':
        return redirect(url_for('flight_details'))
    else:
        return redirect(url_for('flight_delay_detail'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

