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

# print(get_steam_player_summaries(76561199090892473))


def get_steam_friend_list(steamid):
    """get steam user's friend list"""

    friend_list = get(f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_WEB_KEY}&steamid={steamid}&relationship=friend')

    return friend_list.json()

# print(get_steam_friend_list(76561197988750660))

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
    
    json_resp = response.json()

    if json_resp:
        if json_resp[0].get('status'): # does this key exist in the returned dict
            # print(json_resp[0])
            return
        else: 
            return json_resp

print(get_igdb_game_by_name("Ring of Elysium")) #<- Steam
#Yeah! You Want "Those Games", Right? So Here You Go! Now, Let's See You Clear Them! < - IGDB

# if test[0]['title'] == 'Syntax Error':
#     print("yes")
# print(get_igdb_game_by_name("Living In A Brothel"))
