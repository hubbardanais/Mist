
## Hello, and welcome!
My friends and I love to play video games together and a common question I hear during game night is, "Uh... what games do you have?" which is why I created Mist! 
Mist is the solution for gamers who want to quickly and easily find common games to play with friends. 
Now you no longer need to endlessly scroll through your game library or message your friends to ask what they own — Mist does all the work for you! 
All you need to do is create an account with your SteamID, select the friends you want to play with, and Mist will instantly generate a list of games that you all have in common. 
Say goodbye to wasted time and hello to more gaming fun with Mist, your go-to tool for seamless group gaming experiences.



<br/><br/>

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [General Info](#gen-info)
<br/><br/>


## <a name="installation"></a>Installation

#### Prerequisites

To use Mist, you need to have both a [Steam key](https://steamcommunity.com/dev/apikey) and an [IGDB key](https://api-docs.igdb.com/#getting-started). 

- To qualify for a Steam key you need to have a Steam account with at least one purchased game (adding free games to your library doesn't count unfortunately), as well as have their app installed with two factor authentication enabled
- To qualify for an IGDB key you need to have a Twitch account, two factor authentication enabled, and register in the Twitch Developer portal

Once you have both keys, go ahead and clone the repository **`git clone https://github.com/hubbardanais/Mist.git`**

And create a secrets.sh file to hold your keys. Go ahead and copy and paste this code, and replace the asterisks with your keys!
```
export IGDB_CLIENT_ID='******************************'
export IGDB_TOKEN='Bearer ***************************'

export STEAM_WEB_KEY='****************************'
```

Make sure to keep "Bearer " in your IGDB token, otherwise IGDB won't understand what you're talking about.

#### Set up

Now that we have everything we need, it's time to set up a virtual environment and install the requirements. To learn more about Python's virtualenv tool, [read the documentation](https://virtualenv.pypa.io/en/stable/).

Initiate a virtualenv:

```sh
$ virtualenv env
```

Source the virtualenv:

```sh
$ source env/bin/activate
```

Install requirements:

```sh
(env)$ pip3 install -r requirements.txt
```

Now to source our secrets.sh

```sh
(env)$ source secrets.sh
```

Create a PostgreSQL database named `my_database`, and build the model:

```sh
(env)$ createdb my_database
(env)$ python3 -i model.py
>>> db.create_all()
```

Then, run the application with ```python3 server.py```:

```sh
(env)$ python3 server.py
 * ...
 * Running on http://172.30.43.236:6060/ (Press CTRL+C to quit)
 * Restarting with stat
 * Connected to the db!
```

You should see similar success messages in the console. If you have any issues feel free to reach me via GitHub!
<br/><br/>

## <a name="usage"></a>Usage
Yay! We have it all set up and we can finally play around with Mist! BUT FIRST!

#### ⭐ Steam does not share information if a user's account privacy information is set to private, or friends only. For Mist to work, the users you want to add need to have their privacy settings for games and friends set to public ⭐


[VIEW DEMO ON YOUTUBE](https://youtu.be/qUuXAuNiWYA)


<br/><br/>

## <a name="gen-info"></a>General Information

#### Tech Stack

* [Python3](https://www.python.org/downloads/)
* [HTML5](https://developer.mozilla.org/en-US/docs/Glossary/HTML5) and [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
* [PostgresSQL](https://www.postgresql.org/)
* [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
* [Bootstrap](https://getbootstrap.com/)
* [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API)
* [IGDB API](https://api-docs.igdb.com/#getting-started)

#### Author

Anais Hubbard

##### Future Development

1.  Adjust the connection between APIs for more reliablility
2.  Create checks so a user's information is always up to date
3.  Add in the ability to create saved friend groups you can quickly compare games with
4.  Add in the ability to create a firend group game wishlist, and poll for which game to play next
5.  Add in the ability to schedule a game night
6.  Create a discord bot that can auto-update about upcoming game nights, and if a friend in a group needs to get a game
7.  Game suggestions based on group activity


##### Deployment

This application has not been deployed at this time.

##### Permissions

Contact the author for permissions.
