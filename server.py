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

    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def log_in():
    """Log user into apps"""

    #email vs. steam id as the key in session?
    # email = request.form['email']
    steamid = request.form['steamid']
    password = request.form['password']

    if password == 'let-me-in':   # FIXME
        session['current_user'] = steamid
        flash(f'Logged in as {steamid}')
        return redirect('/')

    else:
        flash('Wrong password!')
        return redirect('/login')

    # return render_template('login.html')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)