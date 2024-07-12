"""CRUD operations."""

from model import db, User, Friend, UserLibrary, Game, GameModes, Genres, UserGroups, Groups, GroupWishlist, Event, EventAttendees, connect_to_db


# Functions start here!


if __name__ == '__main__':
    from server import app
    connect_to_db(app)