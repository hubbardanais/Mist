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


def get_steam_friend_list(steamid):
    """get steam user's friend list"""

    friend_list = get(f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_WEB_KEY}&steamid={steamid}&relationship=friend')

    return friend_list.json()

# print(get_steam_friend_list(76561199002632683))

# test = get_steam_friend_list(76561198043449106)

# if not test:
#     print("yes")

# else:
#     print("no")


def get_steam_owned_games(steamid):
    """get steam user's owned game list"""

    owned_games = get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_WEB_KEY}&steamid={steamid}&format=json&include_appinfo=True&include_played_free_games')

    return owned_games.json()

# print(get_steam_owned_games(76561199002632683))

# test = get_steam_owned_games(76561198043449106)

# if  not test['response']:
#     print("yes")

# else: 
#     print("no")


#IGDB calls:
def get_igdb_game_by_name(name):
    """get igdb game info from the game name"""

    response = post('https://api.igdb.com/v4/games', 
                    **{'headers': {'Client-ID': IGDB_CLIENT_ID, 'Authorization': IGDB_TOKEN},
                       'data': f'fields name, genres, game_modes, summary; where name = "{name}";'})
    
    return response.json()

# print(get_igdb_game_by_name("Mass Effect Legendary Edition"))
