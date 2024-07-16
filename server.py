"""Server for finding games owned in common"""

from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


#   ... your routes, view functions, and everything else can come later ...
@app.route('/')
def homepage():
    """View homepage."""

    if 'steamid' in session:
        return render_template('homepage.html')
    else:
        return redirect('/login')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")
    

@app.route('/login', methods=['POST'])
def log_in():
    """Log user into apps"""

    steamid = request.form.get('steamid')
    password = request.form.get('password')

    user = crud.get_user_by_steamid(steamid)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return render_template('/login.html')
    else:
        # Log in user by storing the user's email in session
        session['steamid'] = user.steamid
        session['personaname'] = user.personaname
        # flash(f"Welcome back, {user.personaname}!")
        return redirect('/')


@app.route("/create_account", methods=["GET"])
def show_create_account():
    """Show create account form."""

    return render_template("createaccount.html")


@app.route("/create_account", methods=["POST"])
def register_user():
    """Create a new user."""

    steamid = request.form.get("steamid")
    email = request.form.get("email")
    password = request.form.get("password")
    print(email)
    print("=================================")

    user_email = crud.get_user_by_email(email)
    user_steamid = crud.get_user_by_steamid(steamid)
    print(user_email)
    print("=================================")

    if user_email:
        flash("Cannot create an account with that email. Try again.")
    elif user_steamid:
        flash("Cannot create an account with that SteamID. Try again.")
    else:
        crud.create_user(email=email, password=password, steamid=steamid, personaname="Test User")
        flash("Account created! Please log in.")
        return redirect("/")

    return render_template("createaccount.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)