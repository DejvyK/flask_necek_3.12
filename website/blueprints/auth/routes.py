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
        print (email)
        print (password)
        if curr_user and bcrypt.check_password_hash(curr_user.password, password):
            login_user(curr_user, remember=True)
            flash ('success')
            if curr_user.admin==1:
                next_page = request.args.get('next')
                return redirect(url_for('main.admin'))
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
        krestni = request.form.get("krestni_jmeno")
        prijmeni = request.form.get("prijmeni")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        admincode = request.form.get("admincode")

        if len(email) < 4:
            flash("email musí mít alespoň 4 znaky",category="chyba")
        elif len(krestni) < 2:
            flash("křestní jméno musí mít alespoň 2 znaky",category="chyba")
        elif password1 != password2:
            flash("hesla se navzájem neshodují",category="chyba")
        elif len(password1) < 7:
            flash("heslo je příliš krátké",category="chyba")
        else:
            flash("přidat uživatele do databáze",category="uspech")

        mdict = {
            "email" : email,
            "fname" : krestni,
            "lname" : prijmeni,
            "password" : bcrypt.generate_password_hash(password1).decode('utf8'),
            "admin" : 0,
        }

        check_admin_code = AdminCode.get(by="code", value=admincode)

        print (check_admin_code)
        if (check_admin_code):
            mdict['admin'] = 1

    
        new_user = User(mdict)

        try:
            User.add(new_user)
            flash ('successful!')
            return jsonify({'status' : 'successful'})
        except Exception as err:
            flash ('sorry something went wrong')
            print (err)
            return jsonify({'status' : 'error'})
