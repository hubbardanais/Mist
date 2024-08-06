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
    # elif user_steamid:
    #     flash("Cannot create an account with that SteamID. Try again.")
    elif user_steamid and user_steamid.password != "temporary": 
        flash("Cannot create an account with that SteamID. Try again.")
    else:
        #User Info:
        player_summary = helper.get_steam_player_summaries(steamid)

        for info in player_summary['response']['players']:
            personaname = info['personaname']
            url = info['profileurl']
            avatar = info['avatar']
            avatar_med = info['avatarmedium']
            if user_steamid and user_steamid.password == "temporary":
                updated_user = crud.update_existing_user(email=email, password=password, steamid=steamid)
                add_and_commit(updated_user)
            else:
                user = crud.create_user(email, password, steamid, personaname, avatar, avatar_med, url)
                add_and_commit(user)

        ################
        # Beginning game creation loop
        ################################
        
        owned_games = helper.get_steam_owned_games(steamid)
        # print(f"owned_games: {owned_games}")

        if owned_games['response']:

            for game in owned_games['response']['games']:
                appid = game['appid']
                # print(f"appid: {appid}")
                game_name = game['name']
                # print(game_name)
                img_hash = game['img_icon_url']
                img_url = crud.create_img_url(appid, img_hash)
                game_url = crud.create_steam_game_urls(appid, game_name)

                igdb_game_info = helper.get_igdb_game_by_name(game_name)

                # print(f"igdb_game_info: {igdb_game_info}")
                # check to see if len(igdb_game_info) > 1 ==> iterate through using while loop ==> check which one has game_modes AND genres keys, once that one found, add the attributes
                
                # check here if igdb_game_info returned None
                if igdb_game_info == None:
                    continue

                if len(igdb_game_info) == 1:
                    
                    for game_info in igdb_game_info:
                        id = game_info['id']
                        # print(f"id: {id}")
                        if game_info.get('game_modes'):
                            game_modes = game_info['game_modes']
                            # print(f"game_modes: {game_modes}")
                            string_game_modes = []
                            for mode in game_modes:
                                string_game_modes.append(str(mode))
                            string_game_modes = ", ".join(string_game_modes)
                            # print(f"string_game_modes: {string_game_modes}")
                        else:
                            string_game_modes = ""

                        if game_info.get('genres'):
                            genres = game_info['genres']
                            # print(f"genres: {genres}")
                            string_genres = []
                            for genre in genres:
                                string_genres.append(str(genre))
                            string_genres = ', '.join(string_genres)
                            # print(f"string_genres: {string_genres}")
                        else:
                            string_genres = ""

                        summary = game_info.get('summary', "Seems like the summary on this game is Top Secret!")

                
                    db_game = crud.get_game_by_name(game_name)

                    if not db_game:
                        db_game = crud.create_game(id=id, game_modes=string_game_modes,
                                                    genres=string_genres, name=game_name, 
                                                    summary=summary, appid=appid, img_icon_url=img_url, game_url=game_url)
                        add_and_commit(db_game)

                    is_game_in_user_library = crud.check_for_game_in_user_library(steamid, db_game.name)

                    if not is_game_in_user_library:
                        add_to_game_library = crud.create_user_library(steamid, db_game.name)
                        add_and_commit(add_to_game_library)


                elif len(igdb_game_info) > 1:

                    for game_info in igdb_game_info:
                        if 'game_modes' in game_info and 'genres' in game_info:
                            id = game_info['id']
                            # print(f"id: {id}")
                            if game_info['game_modes']:
                                game_modes = game_info['game_modes']
                                # print(f"game_modes: {game_modes}")
                                string_game_modes = []
                                for mode in game_modes:
                                    string_game_modes.append(str(mode))
                                string_game_modes = ", ".join(string_game_modes)
                                # print(f"string_game_modes: {string_game_modes}")
                            else:
                                string_game_modes = None

                            if game_info['genres']:
                                genres = game_info['genres']
                                # print(f"genres: {genres}")
                                string_genres = []
                                for genre in genres:
                                    string_genres.append(str(genre))
                                string_genres = ', '.join(string_genres)
                                # print(f"string_genres: {string_genres}")
                            else:
                                string_genres = None

                            summary = game_info.get('summary')
                 

                            db_game = crud.get_game_by_name(game_name)

                            if not db_game:
                                db_game = crud.create_game(id=id, game_modes=string_game_modes,
                                                        genres=string_genres, name=game_name, 
                                                        summary=summary, appid=appid, img_icon_url=img_url, game_url=game_url)
                                add_and_commit(db_game)

                            is_game_in_user_library = crud.check_for_game_in_user_library(steamid, db_game.name)

                            if not is_game_in_user_library:
                                add_to_game_library = crud.create_user_library(steamid, db_game.name)
                                add_and_commit(add_to_game_library)

                            break                           


        ################
        # Beginning friend creation loop
        ################################

        friend_list = helper.get_steam_friend_list(steamid)

        if friend_list:

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
                        

                        friend_owned_games = helper.get_steam_owned_games(friend_steamid)
                        # print(f"owned_games: {owned_games}")

                        if friend_owned_games['response']:

                            for friend_game in friend_owned_games['response']['games']:
                                f_appid = friend_game['appid']
                                # print(f"appid: {appid}")
                                f_game_name = friend_game['name']
                                # print(game_name)
                                f_img_hash = friend_game['img_icon_url']
                                f_img_url = crud.create_img_url(f_appid, f_img_hash)
                                f_game_url = crud.create_steam_game_urls(f_appid, f_game_name)

                                friend_igdb_game_info = helper.get_igdb_game_by_name(f_game_name)

                                if friend_igdb_game_info == None:
                                    continue

                                # checking if id is in response, skipping if not in resp
                                # TODO - if issue persisits, add to other game info checks below
                                # and friend_game_info.get('id')
                                if len(friend_igdb_game_info) == 1:
                                    
                                    for friend_game_info in friend_igdb_game_info:
                                        print(friend_igdb_game_info)
                                        f_id = friend_game_info['id']
                                        # print(f"id: {id}")
                                        if friend_game_info.get('game_modes'):
                                            f_game_modes = friend_game_info['game_modes']
                                            # print(f"game_modes: {game_modes}")
                                            f_string_game_modes = []
                                            for f_mode in f_game_modes:
                                                f_string_game_modes.append(str(f_mode))
                                            f_string_game_modes = ", ".join(f_string_game_modes)
                                            # print(f"string_game_modes: {string_game_modes}")
                                        else:
                                            f_string_game_modes = ""

                                        if friend_game_info.get('genres'):
                                            f_genres = friend_game_info['genres']
                                            # print(f"genres: {genres}")
                                            f_string_genres = []
                                            for f_genre in f_genres:
                                                f_string_genres.append(str(f_genre))
                                            f_string_genres = ', '.join(f_string_genres)
                                            # print(f"string_genres: {string_genres}")
                                        else:
                                            f_string_genres = ""

                                        f_summary = friend_game_info.get('summary', "Seems like the summary on this game is Top Secret!")

                                
                                    f_db_game = crud.get_game_by_name(f_game_name)

                                    if not f_db_game:
                                        f_db_game = crud.create_game(id=f_id, game_modes=f_string_game_modes,
                                                                    genres=f_string_genres, name=f_game_name, 
                                                                    summary=f_summary, appid=f_appid, img_icon_url=f_img_url, game_url=f_game_url)
                                        add_and_commit(f_db_game)
                                        print("added new game and committed")

                                    f_is_game_in_user_library = crud.check_for_game_in_user_library(friend_steamid, f_db_game.name)
                                    print(f_db_game.name)
                                    print(f_db_game.id)
                                    print(f_db_game)
                                    print(f_is_game_in_user_library)
                                    if not f_is_game_in_user_library:
                                        f_add_to_game_library = crud.create_user_library(friend_steamid, f_db_game.name)
                                        print(f_add_to_game_library.steamid)
                                        print(f_add_to_game_library.name)
                                        add_and_commit(f_add_to_game_library)


                                elif len(friend_igdb_game_info) > 1:

                                    for f_game_info in friend_igdb_game_info:
                                        if 'game_modes' in f_game_info and 'genres' in f_game_info:
                                            f_id = f_game_info['id']
                                            # print(f"id: {id}")
                                            if f_game_info['game_modes']:
                                                f_game_modes = f_game_info['game_modes']
                                                # print(f"game_modes: {game_modes}")
                                                f_string_game_modes = []
                                                for f_mode in f_game_modes:
                                                    f_string_game_modes.append(str(f_mode))
                                                f_string_game_modes = ", ".join(f_string_game_modes)
                                                # print(f"string_game_modes: {string_game_modes}")
                                            else:
                                                f_string_game_modes = None

                                            if f_game_info['genres']:
                                                f_genres = f_game_info['genres']
                                                # print(f"genres: {genres}")
                                                f_string_genres = []
                                                for f_genre in f_genres:
                                                    f_string_genres.append(str(f_genre))
                                                f_string_genres = ', '.join(f_string_genres)
                                                # print(f"string_genres: {string_genres}")
                                            else:
                                                f_string_genres = None

                                            f_summary = f_game_info.get('summary', "Seems like the summary on this game is Top Secret!")
                                

                                            f_db_game = crud.get_game_by_name(f_game_name) # return the object OR None
                                            print(f_db_game)

                                            if not f_db_game:
                                                f_db_game = crud.create_game(id=f_id, game_modes=f_string_game_modes,
                                                                            genres=f_string_genres, name=f_game_name, 
                                                                            summary=f_summary, appid=f_appid, img_icon_url=f_img_url, game_url=f_game_url)
                                                add_and_commit(f_db_game)

                                            f_is_game_in_user_library = crud.check_for_game_in_user_library(friend_steamid, f_db_game.name)

                                            if not f_is_game_in_user_library:
                                                f_add_to_game_library = crud.create_user_library(friend_steamid, f_db_game.name)
                                                add_and_commit(f_add_to_game_library)

                                            break

        
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
    # os.system('dropdb my_database')
    # os.system('createdb my_database')

    connect_to_db(app)
    # db.create_all()
    
    app.run(host="0.0.0.0", debug=True, port=6060)