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

    friends = db.relationship('Friend', back_populates="users")

    def __repr__(self):
        return f'<User id={self.id} personaname={self.personaname} steamid={self.steamid}>'
    

#Info from Steam
class Friend(db.Model):
    """A friend connection between to users"""

    __tablename__ = "friends"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('users.steamid'), nullable=False)
    user2 = db.Column(db.Integer, db.ForeignKey('users.steamid'), nullable=False)

    # users = db.relationship('User', back_populates="friends")

    def __repr__(self):
        return f'<Friend id={self.id} user1={self.user1} user2={self.user2}>'
    

#Info from Steam
class UserLibrary(db.Model):
    """A dictionary of games"""

    __tablename__ = "user_library"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    steamid = db.Column(db.String, db.ForeignKey('users.steamid'), nullable=False, unique=True)
    appid = db.Column(db.Integer)
    name = db.Column(db.String, db.ForeignKey('games.name'), nullable=False)
    img_icon_url = db.Column(db.String)
    #this info isn't given, I need to make it like: http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg
    #ex: https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/
    #for names with whitespace, just replace with _
    game_url = db.Column(db.String)

    def __repr__(self):
        return f'<UserLibrary id={self.id} steamid={self.steamid}>'


#Info from IGDB
class Game(db.Model):
    """A game"""

    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    game_modes = db.Column(db.Integer, db.ForeignKey('game_modes.name'))
    genres = db.Column(db.Integer, db.ForeignKey('genres.name'))
    name = db.Column(db.String)
    summary = db.Column(db.String)

    
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