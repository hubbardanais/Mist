"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system('dropdb ratings')
os.system('createdb ratings')

connect_to_db(app)
app.app_context().push()
db.create_all()

#open json files for game_Modes and genres

#make one/two test info for everything