from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, logout_user, login_user

from website import db, bcrypt, login_manager
from website.models.users import User


auth = Blueprint('auth', __name__)

@auth.route ('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)

@auth.route("/logout")
@login_required
def logout():
    try:
        logout_user()
    except Exception as err:
        print (err)
        return 'error'

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        krestni = request.form.get("krestni_jmeno")
        prijmeni = request.form.get("prijmeni")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
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

    return render_template("sign_up.html")


@auth.route('/', methods= ['GET'])
def stuff():
    stahp = "1"
    return jsonify(stahp)