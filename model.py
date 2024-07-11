"""Models for finding games owned in common"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#Info from Steam
class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)

    steamid = db.Column(db.String, nullable=False, unique=True)
    personaname = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    avatarmedium = db.Column(db.String)
    profileurl = db.Column(db.String)

    # friends = db.relationship('Friend', back_populates="users")
    # TODO REVIEW
    library = db.relationship('UserLibrary', back_populates="user")
    # User.library => [<UserLibrary>, <UserLibrary>]

    def __repr__(self):
        return f'<User id={self.id} personaname={self.personaname} steamid={self.steamid}>'
    

#Info from Steam
class Friend(db.Model):
    """A friend connection between to users"""

    __tablename__ = "friends"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    primary_user_steamid = db.Column(db.Integer, db.ForeignKey('users.steamid'), nullable=False)
    friend_steamid = db.Column(db.Integer, nullable=False)
    
    # user1 = db.Column(db.Integer, db.ForeignKey('users.steamid'), nullable=False)
    # user2 = db.Column(db.Integer, db.ForeignKey('users.steamid'), nullable=False)

    # users = db.relationship('User', back_populates="friends")

    def __repr__(self):
        return f'<Friend id={self.id} user1={self.primary_user_steamid} user2={self.friend_steamid}>'
    

#Info from Steam
class UserLibrary(db.Model): # middle table UserGame ==> tying a user/steamid to a game name/id
    """A dictionary of games"""

    __tablename__ = "user_library"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    steamid = db.Column(db.String, db.ForeignKey('users.steamid'), nullable=False, unique=True)
    appid = db.Column(db.Integer)
    name = db.Column(db.String, db.ForeignKey('games.name'), nullable=False)
    img_icon_url = db.Column(db.String)
    #this info isn't given, I need to make it like: http://store.steampowered.com/app/{appid}/{name}/
    #ex: https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/
    # for names with whitespace, just replace with _
    game_url = db.Column(db.String)

    # TODO REVIEW
    user = db.relationship('User', back_populates="library")

    def __repr__(self):
        return f'<UserLibrary id={self.id} steamid={self.steamid}>'


#Info from IGDB
class Game(db.Model):
    """A game"""

    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    # TODO - game can have multiple genres, multiple game modes
    game_modes = db.Column(db.Integer, db.ForeignKey('game_modes.name'))
    genres = db.Column(db.Integer, db.ForeignKey('genres.name'))
    #########

    name = db.Column(db.String)
    summary = db.Column(db.String)

    # TODO REVIEW ==> review the db.relationship? .game_genres?

    # TODO - maybe add .wishlists ?

    
    def __repr__(self):
        return f'<Game id={self.id} name={self.name}>'


#Info from IGDB
class GameModes(db.Model):
    """The type of multiplayer mode"""

    __tablename__ = "game_modes"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<GameModes id={self.id} name={self.name}>'


#Info from IGDB
class Genres(db.Model):
    """The type of multiplayer mode"""

    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Genres id={self.id} name={self.name}>'



class UserGroups(db.Model):
    """Associate table for User and Groups"""

    __tablename__ = "usergroups"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    steamid = db.Column(db.Integer, db.ForeignKey('users.steamid'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return f'<Class id={self.id} user_id={self.steamid} group_id={self.group_id}>'
    

class Groups(db.Model):
    """a group of users"""

    __tablename__ = "groups"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    group_name = db.Column(db.String)
    group_img = db.Column(db.String)

    def __repr__(self):
        return f'<Class id={self.id} group_name={self.group_name}>'
    

class GroupWishlist(db.Model):
    """a list of games associated with a group"""

    __tablename__ = "group_wishlists"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    # TODO - maybe add .game
    # TODO - maybe add .group

    def __repr__(self):
        return f'<Class id={self.id} game_id={self.game_id} group_id={self.group_id}>'
    

class Event(db.Model):
    """A scheduled playtime together"""

    __tablename__ = "events"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    proposed_datetime = db.Column(db.DateTime)
    description = db.Column(db.String)
    if_game_selected = db.Column(db.Boolean)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=True)

    def __repr__(self):
        return f'<Class id={self.id} description={self.description}>'
    

class EventAttendance(db.Model):
    """users who will or won't join the playtime"""

    __tablename__ = "event_attendance"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    steamid = db.Column(db.Integer, db.ForeignKey('users.steamid'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    is_attending = db.Column(db.Boolean)


    def __repr__(self):
        return f'<Class id={self.id} event_id={self.event_id}>'
    





#ANI, ADJUST THE URI TO THE NAME OF THE DATABASE
def connect_to_db(flask_app, db_uri="postgresql:///XXXXXXXX", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.