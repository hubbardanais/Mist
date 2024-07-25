"""Server for finding games owned in common"""
import os

from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db
import crud
import helper

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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

    user_email = crud.get_user_by_email(email)
    user_steamid = crud.get_user_by_steamid(steamid)


    if user_email:
        flash("Cannot create an account with that email. Try again.")
    elif user_steamid:
        flash("Cannot create an account with that SteamID. Try again.")
    else:
        #User Info:
        player_summary = helper.get_steam_player_summaries(steamid)

        for info in player_summary['response']['players']:
            personaname = info['personaname']
            url = info['profileurl']
            avatar = info['avatar']
            avatar_med = info['avatarmedium']

            user = crud.create_user(email, password, steamid, personaname, avatar, avatar_med, url)
            add_and_commit(user)


        friend_list = helper.get_steam_friend_list(steamid)

        for friend in friend_list['friendslist']['friends']:
            friend_steamid = friend['steamid']

            users_friends =  crud.create_friend(steamid, friend_steamid)
            add_and_commit(users_friends)

            check_if_friend_in_db = crud.get_user_by_steamid(friend_steamid)

            #Friend Info:
            if not check_if_friend_in_db:
                friend_summary = helper.get_steam_player_summaries(friend_steamid)

                for info in friend_summary['response']['players']:
                    personaname = info['personaname']
                    url = info['profileurl']
                    avatar = info['avatar']
                    avatar_med = info['avatarmedium']

                    friend_user = crud.create_user(email=friend_steamid, password="temporary",
                                                steamid=friend_steamid, personaname=personaname, 
                                                avatar=avatar, avatarmedium=avatar_med, profileurl=url)
                    add_and_commit(friend_user)

        
        flash("Account created! Please log in.")
        return redirect("/login")
    # else:
    #     user = crud.create_user(email=email, password=password, steamid=steamid, personaname="Test User")
    #     add_and_commit(user)
    #     flash("Account created! Please log in.")
    #     return redirect("/login")

    return render_template("createaccount.html")


@app.route("/log_out")
def log_out():
    """Remove user from session"""

    session.clear()

    return redirect('/')


@app.route("/user/<personaname>")
def user_profile(personaname):
    """view user profile"""

    user = crud.get_user_by_personaname(personaname)

    return render_template('user_profile.html', user=user)


@app.route("/games")
def game_page():
    """view games"""

    user_library = crud.get_all_user_games_by_steamid(session['steamid'])

    return render_template('games.html', user_library=user_library)
    

@app.route("/friends")
def friends_list():
    """view all friends a user has"""

    friends = crud.get_list_of_friends_as_users(session['steamid'])

    return render_template('friends.html', friends=friends)


@app.route("/compare_games")
def compare_games_with_friends():
    """view list of games shared between friends"""

    friends = crud.get_list_of_friends_as_users(session['steamid'])

    return render_template('compare_games.html', friends=friends)


@app.route("/compare_games", methods=["POST"])
def get_selected_friends_to_compare():
    """view list of games shared between friends"""

    #Get all users selected from compare_games checkbox form
    selected_users_to_compare_games = request.form.keys() 

    #Get a set of all the games the user in session has
    user_games = crud.get_all_games_by_steamid(session['steamid'])

    friends_games = []

    #for each friend selected, get the set of their games and add to list
    for user in selected_users_to_compare_games:
        friends_games.append(crud.get_all_games_by_steamid(user))

    if friends_games:
        common_games = user_games
        
        for friend in friends_games:
            common_games = common_games & friend

        return render_template('returned_shared_games.html', friends_games=common_games)
    
    else:
        flash("Please select a friend to find shared games with")
        return redirect('/compare_games')


# @app.route("/X")
# def X():
#     """"""

#     return


def add_and_commit(inst):
    """a faster way to add and commit everything to the db"""
    db.session.add(inst)
    db.session.commit()


if __name__ == "__main__":
    os.system('dropdb my_database')
    os.system('createdb my_database')

    connect_to_db(app)
    db.create_all()
    
    app.run(host="0.0.0.0", debug=True, port=6060)