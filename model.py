"""Models for finding games owned in common"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



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
    
    
class Friend(db.Model):
    """a friend connection between to users"""

    __tablename__ = "friends"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey, nullable=False)
    user2 = db.Column(db.Integer, db.ForeignKey, nullable=False)

    # users = db.relationship('User', back_populates="friends")

    def __repr__(self):
        return f'<Friend id={self.id} user1={self.user1} user2={self.user2}>'
    


    

# class Movie(db.Model):
#     """A movie"""    
    
#     __tablename__ = "movies"

#     movie_id = db.Column(db.Integer,
#                         autoincrement= True,
#                         primary_key= True)
#     title = db.Column(db.String)
#     overview = db.Column(db.Text)
#     release_date = db.Column(db.DateTime)
#     poster_path = db.Column(db.String)

#     ratings = db.relationship("Rating", back_populates="movie")

#     def __repr__(self):
#         return f'<Movie movie_id={self.movie_id} title={self.title}>'
    
# class Rating(db.Model):
#     """A rating"""

#     __tablename__ = "ratings"

#     rating_id = db.Column(db.Integer,
#                           autoincrement= True,
#                           primary_key= True)
#     score = db.Column(db.Integer)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

#     movie = db.relationship("Movie", back_populates="ratings")
#     user = db.relationship("User", back_populates="ratings")

#     def __repr__(self):
#         return f'<Rating rating_id={self.rating_id} score={self.score}>'


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app


    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
