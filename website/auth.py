from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route ('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return '<p> logout </p>'

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


@app.route('/', methods= ['GET'])
def stuff():
    stahp = "1"
    return jsonify(stahp)