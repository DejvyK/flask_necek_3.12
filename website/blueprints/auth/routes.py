from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, logout_user, login_user

from website import bcrypt, login_manager
from website.models.users import User
from website.models.admincode import AdminCode
import json


auth = Blueprint('auth', __name__)

@auth.route ('/authorize_user', methods=['GET', 'POST'])
def authorize_user():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        curr_user = User.get(by="email", value=email)
        if curr_user and bcrypt.check_password_hash(curr_user.password, password):
            login_user(curr_user, remember=True)
            if curr_user.admin==1:
                next_page = request.args.get('next')
                return redirect(url_for('admin.home'))
            return redirect(url_for('main.home'))
        flash ('wrong email or password')
        return redirect(url_for('main.login'))


@auth.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        next_page = request.args.get('next')
        return redirect(url_for('main.home'))
    except Exception as err:
        print (err)
        return redirect(url_for('main.login'))

@auth.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password = request.form.get("password")
        admincode = request.form.get("admincode")

        mdict = {
            "email" : email,
            "fname" : fname,
            "lname" : lname,
            "password" : bcrypt.generate_password_hash(password).decode('utf8'),
            "admin" : 0,
        }

        check_admin_code = AdminCode.get(by="code", value=admincode)

        if (check_admin_code):
            mdict['admin'] = 1

        new_user = User(mdict)

        try:
            User.add(new_user)
            login_user(new_user, remember=True)
            next_page = request.args.get('next')
            flash ('successful!')
            if new_user.admin==1:
                return redirect(url_for('admin.home'))
            else:
                return redirect(url_for('main.home'))

        except Exception as err:
            flash ('something went wrong!')
            next_page = request.args.get('next')
            return redirect(url_for('main.signup'))
