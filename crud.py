"""CRUD operations."""

from datetime import datetime

from model import db, User, Friend, UserLibrary, Game, GameModes, Genres, UserGroups, Groups, GroupWishlist, Event, EventAttendees, connect_to_db


# Functions start here!

def add_and_commit(inst):
    """a faster way to add and commit everything to the db"""
    db.session.add(inst)
    db.session.commit()


def create_user(email, password, steamid, personaname, avatar=None,
                 avatarmedium=None, profileurl=None):
    """Create and return a new user."""

    user = User(email=email,
                password=password,
                steamid=steamid,
                personaname=personaname,
                avatar=avatar,
                avatarmedium=avatarmedium,
                profileurl=profileurl
                )
    
    add_and_commit(user)
    return user


def get_user_by_steamid(steamid):
    """return a user by steamid"""

    return User.query.filter(User.steamid == steamid).first()


def get_user_by_email(email):
    """return a user by email"""

    return User.query.filter(User.email == email).first()


def get_user_by_personaname(personaname):
    """return a user by personaname"""

    return User.query.filter(User.personaname == personaname).first()


def create_friend(primary_user_steamid, friend_steamid):
    """create and return a friendship"""

    friend = Friend(primary_user_steamid=primary_user_steamid,
                    friend_steamid=friend_steamid
                    )
    
    add_and_commit(friend)
    return friend


def create_game(id, game_modes, genres, name, summary=None, appid=None,
                img_icon_url=None, game_url=None):
    """create and return a game"""

    game = Game(id=id,
                game_modes=game_modes,
                genres=genres,
                name=name,
                summary=summary,
                appid=appid,
                img_icon_url=img_icon_url,
                game_url=game_url
                )
    
    add_and_commit(game)
    return game


def create_user_library(steamid, name):
    """create and return an association between a user and game"""

    user_library = UserLibrary(steamid=steamid,
                               name=name)

    add_and_commit(user_library)
    return user_library


def get_all_user_games_by_steamid(steamid):
    """return list of all owned games from user"""

    user_games = UserLibrary.query.filter(UserLibrary.steamid == steamid).all()

    return user_games


def create_game_modes(id, name):
    """create and return a comma seperated string of game modes"""

    game_modes = GameModes(id=id, name=name)

    add_and_commit(game_modes)
    return game_modes


def create_genres(id, name):
    """create and return a comma seperated string of game modes"""

    genres = Genres(id=id, name=name)

    add_and_commit(genres)
    return genres


def get_genre(id):
    """return genre by id"""

    genre = Genres.query.filter(Genres.id == id).first()

    return genre


def convert_genre_str_to_list(genres_str):
    """take a string of a list of genres, and turn it into a list of ints"""

    split_string = genres_str.split(", ")

    for i, genre in enumerate(split_string):
        split_string[i] = int(genre)

    return split_string


def create_user_groups(steamid, group_id):
    """create and return an association between a user and a group"""

    user_groups = UserGroups(steamid=steamid, group_id=group_id)

    add_and_commit(user_groups)
    return user_groups


def create_groups(group_name, group_img):
    """create and return a group"""

    group = Groups(group_name=group_name,
                   group_img=group_img)

    add_and_commit(group)
    return group


def create_group_wishlist(game_id, group_id):
    """create and return a games associated with a group"""

    group_wishlist = GroupWishlist(game_id=game_id,group_id=group_id)

    add_and_commit(group_wishlist)
    return group_wishlist


def create_event(group_id, proposed_datetime, description, 
                 if_game_selected=False, game_id=None):
    """create and return an event"""

    format_string = "%Y-%m-%d %H:%M"
    datetime_object = datetime.strptime(proposed_datetime, format_string)

    event = Event(group_id=group_id,
                  proposed_datetime=datetime_object,
                  description=description,
                  if_game_selected=if_game_selected,
                  game_id=game_id)

    add_and_commit(event)
    return event


def create_event_attendees(steamid, event_id, is_attending):
    """create and return a user associated with an event"""

    event_attendees = EventAttendees(steamid=steamid,
                                     event_id=event_id,
                                     is_attending=is_attending,
                                     )

    add_and_commit(event_attendees)
    return event_attendees


#create functions to create img urls and steam game urls
def create_img_url(appid, img_icon_url):
    """create and return an img url for a game with steam's info"""

    #appid is an int, img_icon_url is a str
    return f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{img_icon_url}.jpg"


def create_steam_game_urls(appid, name):
    """create and return a steam game url"""

    name_with_underline = ""

    for char in name:
        if char == " ":
            name_with_underline += "_"
        else:
            name_with_underline += char
    
    return f"http://store.steampowered.com/app/{appid}/{name_with_underline}/"



if __name__ == '__main__':
    from server import app
    connect_to_db(app)