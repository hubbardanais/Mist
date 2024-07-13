"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system('dropdb my_database')
os.system('createdb my_database')

connect_to_db(app)
app.app_context().push()
db.create_all()

#open json files for game_Modes and genres
# crud.create_game_modes(id, name)


# crud.create_genres(id, name)


#make one/two test info for everything
ani = crud.create_user(email="anitest@test.com", password="password", 
                steamid="76561199002632683", personaname="Tiny Titan",
                avatar="https://avatars.steamstatic.com/e4c5e2ab869df41657cb2108f0d01723d0ba7ba7.jpg",
                avatarmedium="https://avatars.steamstatic.com/e4c5e2ab869df41657cb2108f0d01723d0ba7ba7_medium.jpg", 
                profileurl="https://steamcommunity.com/id/mapleleafthief/")

izzie = crud.create_user(email="izzietest@test.com", password="passwordo", 
                steamid="76561198043449106", personaname="Noble Fox",
                avatar="https://avatars.steamstatic.com/6a92bfcd37aedd8d9d6d024d5dc97e0225215e91.jpg",
                avatarmedium="https://avatars.steamstatic.com/6a92bfcd37aedd8d9d6d024d5dc97e0225215e91_medium.jpg", 
                profileurl="https://steamcommunity.com/id/m0y0/")

barry = crud.create_user(email="barrytest@test.com", password="passwordi", 
                steamid="76561198244990238", personaname="Villainous aesthetic",
                avatar="https://avatars.steamstatic.com/6330c0531c83e7262767b52a29728f6801bcc289.jpg",
                avatarmedium="https://avatars.steamstatic.com/6330c0531c83e7262767b52a29728f6801bcc289_medium.jpg", 
                profileurl="https://steamcommunity.com/profiles/76561198244990238/")


ani_izzie = crud.create_friend(primary_user_steamid=76561199002632683,
                friend_steamid=76561198043449106)
ani_barry = crud.create_friend(primary_user_steamid=76561199002632683,
                friend_steamid=76561198244990238)
 

stardew = crud.create_game(id=17000, game_modes="1,2,3", genres="12, 13, 15, 32", name="Stardew Valley", 
                           summary="Stardew Valley is an open-ended country-life RPG! You’ve inherited your grandfather’s old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life. Can you learn to live off the land and turn these overgrown fields into a thriving home? It won’t be easy. Ever since Joja Corporation came to town, the old ways of life have all but disappeared. The community center, once the town’s most vibrant hub of activity, now lies in shambles. But the valley seems full of opportunity. With a little dedication, you might just be the one to restore Stardew Valley to greatness!",
                           appid=413150,
                           img_icon_url="http://media.steampowered.com/steamcommunity/public/images/apps/413150/35d1377200084a4034238c05b0c8930451e2fb40.jpg", 
                           game_url="https://store.steampowered.com/app/413150/Stardew_Valley/")

destiny_2 = crud.create_game(id=25657, game_modes="1,2,3,5", genres="5, 12, 31", name="Destiny 2", 
                           summary="Dive into the world of Destiny 2 to explore the mysteries of the solar system and experience responsive first-person shooter combat. Unlock powerful elemental abilities and collect unique gear to customize your Guardian's look and playstyle. Enjoy Destiny 2’s cinematic story, challenging co-op missions, and a variety of PvP modes alone or with friends. Download for free today and write your legend in the stars.",
                           appid=1085660,
                           img_icon_url="http://media.steampowered.com/steamcommunity/public/images/apps/1085660/fce050d63f0a2f8eb51b603c7f30bfca2a301549.jpg", 
                           game_url="https://store.steampowered.com/app/1085660/Destiny_2/")

cyberpunk_2077 = crud.create_game(id=1877, game_modes="1", genres="5, 12, 31", name="Cyberpunk 2077", 
                           summary="Cyberpunk 2077 is an open-world, action-adventure story set in Night City, a megalopolis obsessed with power, glamour and body modification. You play as V, a mercenary outlaw going after a one-of-a-kind implant that is the key to immortality. You can customize your character’s cyberware, skillset and playstyle, and explore a vast city where the choices you make shape the story and the world around you.",
                           appid=1091500,
                           img_icon_url="http://media.steampowered.com/steamcommunity/public/images/apps/1091500/15ba5f5437473a1b4d628b3b87223e84f4cfdf38.jpg", 
                           game_url="https://store.steampowered.com/app/1091500/Cyberpunk_2077/")

laika = crud.create_game(id=146088, game_modes="1", genres="8, 31, 32, 33", name="Laika: Aged Through Blood", 
                           summary="Laika: Aged Through Blood is a western-inspired motorvania set in a post-apocalyptic desert. It is the story about a tribe oppressed by occupant forces, and the personal story of a mother coyote warrior who descends on an endless path of vengeance to take back what her people lost.",
                           )


ani_stardew = crud.create_user_library(steamid="76561199002632683", name="Stardew Valley")
ani_destiny_2 = crud.create_user_library(steamid="76561199002632683", name="Destiny 2")
ani_cyberpunk_2077 = crud.create_user_library(steamid="76561199002632683", name="Cyberpunk 2077")

izzie_destiny_2 = crud.create_user_library(steamid="76561198043449106", name="Destiny 2")
izzie_cyberpunk_2077 = crud.create_user_library(steamid="76561198043449106", name="Cyberpunk 2077")

barry_destiny_2 = crud.create_user_library(steamid="76561198244990238", name="Destiny 2")
barry_stardew = crud.create_user_library(steamid="76561198244990238", name="Stardew Valley")


destineers = crud.create_groups(group_name="Destineers", group_img="irondestineer.jpeg")

ani_destineers = crud.create_user_groups(steamid="76561199002632683", group_id=1)
izzie_destineers = crud.create_user_groups(steamid="76561198043449106", group_id=1)
barry_destineers = crud.create_user_groups(steamid="76561198244990238", group_id=1)

destineers_laika = crud.create_group_wishlist(game_id=146088, group_id=1)


# crud.create_event(group_id, proposed_datetime, description, 
#                  if_game_selected=False, game_id=None)

# crud.create_event_attendees(steamid, event_id, is_attending)
 