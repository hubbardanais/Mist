import os

from requests import post, get

# import crud

STEAM_WEB_KEY = os.environ['STEAM_WEB_KEY']

IGDB_CLIENT_ID = os.environ['IGDB_CLIENT_ID']
IGDB_TOKEN = os.environ['IGDB_TOKEN']


#Steam calls:
def get_steam_player_summaries(steamid):
    """get steam user info"""

    player_summary = get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_WEB_KEY}&steamids={steamid}')

    return player_summary.json()

# print(get_steam_player_summaries(76561199002632683))
# get_steam_player_summaries(76561199002632683)


# def add_player_summary_to_db(email, password, steamid):
#     """add user to db"""

#     player_summary = get_steam_player_summaries(steamid)

    
#     for info in player_summary['response']['players']:
#         personaname = info['personaname']
#         url = info['profileurl']
#         avatar = info['avatar']
#         avatar_med = info['avatarmedium']

#         crud.create_user(email, password, steamid, personaname, avatar, avatar_med, url)


def get_steam_friend_list(steamid):
    """get steam user's friend list"""

    friend_list = get(f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_WEB_KEY}&steamid={steamid}&relationship=friend')

    return friend_list.json()

# print(get_steam_friend_list(76561199002632683))


# def add_friend_list_to_db(steamid):

#     friend_list = get_steam_friend_list(steamid)

#     for friend in friend_list['friendslist']['friends']:
#        friend_steamid = friend['steamid']
#        print(friend_steamid)
#        print('=======================================')

#        test =  crud.create_friend(steamid, friend_steamid)
#        print(test)

# add_friend_list_to_db(76561199002632683)


def get_steam_owned_games(steamid):
    """get steam user's owned game list"""

    owned_games = get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_WEB_KEY}&steamid={steamid}&format=json&include_appinfo=True&include_played_free_games')

    return owned_games.json()

# print(get_steam_owned_games(76561199002632683))


#IGDB calls:
def get_igdb_game_by_name(name):
    """get igdb game info from the game name"""

    response = post('https://api.igdb.com/v4/games', 
                    **{'headers': {'Client-ID': IGDB_CLIENT_ID, 'Authorization': IGDB_TOKEN},
                       'data': f'fields name, genres, game_modes, summary; where name = "{name}";'})
    
    print(str(response.json()))

# get_igdb_game_by_name("Slime Rancher")