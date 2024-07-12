"""CRUD operations."""

from model import db, User, Friend, UserLibrary, Game, GameModes, Genres, UserGroups, Groups, GroupWishlist, Event, EventAttendees, connect_to_db


# Functions start here!
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

    return user

def create_friend(primary_user_steamid, friend_steamid):
    """create and return a friendship"""

    friend = Friend(primary_user_steamid=primary_user_steamid,
                    friend_steamid=friend_steamid
                    )
    
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
    
    return game


def create_user_library(steamid, name):
    """create and return an association between a user and game"""

    user_library = UserLibrary(steamid=steamid,
                               name=name)

    return user_library

def create_game_modes(id, name):
    """create and return a comma seperated string of game modes"""

    game_modes = GameModes(id=id, name=name)

    return game_modes

def create_genres(id, name):
    """create and return a comma seperated string of game modes"""

    genres = GameModes(id=id, name=name)

    return genres

def create_user_groups(steamid, group_id):
    """create and return an association between a user and a group"""

    user_groups = UserGroups(steamid=steamid, group_id=group_id)

    return user_groups

def create_groups(group_name, group_img):
    """create and return a group"""

    group = Groups(group_name=group_name,
                   group_img=group_img)

    return group

def create_group_wishlist(game_id, group_id):
    """create and return a games associated with a group"""

    group_wishlist = GroupWishlist(game_id=game_id,group_id=group_id)

    return group_wishlist

def create_event(group_id, proposed_datetime, description, 
                 if_game_selected=False, game_id=None):
    """create and return an event"""

    event = Event(group_id=group_id,
                  proposed_datetime=proposed_datetime,
                  description=description,
                  if_game_selected=if_game_selected,
                  game_id=game_id)

    return event

def create_event_attendees(steamid, event_id, is_attending):
    """create and return a user associated with an event"""

    event_attendees = EventAttendees(steamid=steamid,
                                     event_id=event_id,
                                     is_attending=is_attending,
                                     )

    return event_attendees




if __name__ == '__main__':
    from server import app
    connect_to_db(app)