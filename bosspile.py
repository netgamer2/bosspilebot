# B stands for Blue diamonds
# O stands for Orange diamonds
# N stands for Orange Big Diamonds
# C stands for Crown
#
# W stands for cloud (waiting) [ removed from this implementation]
# U stands for arrow up
# I stands for Inactive
GAMES = {}

class Game():

    def __init__(self, name = '', channel_id = 0):
        self.name = name
        self.bosspile = {}
        self.channel_id = channel_id
        self.map = {}

    def make_map(self):
        bosspile = self.bosspile

        for p in bosspile.values():
            n = p.position
            self.map[n] = p

    
class Player():

    def __init__(self, name='', prefixes='', suffixes='', position=0, facing=''):
        self.name = name
        self.prefixes = prefixes
        self.suffixes = suffixes
        self.position = position
        self.facing = facing


def set_up_games(names, ids):
    global GAMES

    for name, id_ in zip(names, ids):
        GAMES[name] = (Game(name, id_))

def set_up_bosspile(game, players):
    """players is a tuple of names,prefixes, suffixes, positions"""
    bosspile = game.bosspile

    for args in players:
        player = Player(*args)

        bosspile[args[0]] = player # name

    game.make_map()

def victory(game, victor, loser):
    victor, loser = game.bosspile[victor], game.bosspile[loser]
    p1, p2 = victor.position, loser.position

    if victor.facing != loser.name:
        print('errroooor')
        assert(0)

    if p2 != 0 and p1 != 0:
        modify_fix(victor, 'U') # handles ups
        modify_fix(loser, 'U', add=False)
    elif p2 == 0:
        modify_fix(victor, 'C', suffix=False) # handles crowns
        modify_fix(loser, 'C', add=False, suffix=False)     
        modify_fix(victor, 'U', add=False)  
    elif p1 == 0:
        diamonds = victor.prefixes.count('O')
        if diamonds == 4:
            blue = victor.prefixes.count('B')
            n = victor.prefixes.count('N') + 1
            victor.prefixes = 'C' + 'B' * blue + 'N' * n
        else:
           victor.prefixes += 'O'    
        modify_fix(loser, 'U', add=False)            
    # last player is always active       

    # handles the new positioning

    # if the victor is already higher on the standings, do not modify them.
    
    if p1 > p2: # if the victor is lower, however. there are two cases:
        if p1 - p2 == 1:
            victor.position = p2
            loser.position = p1
            if p2 == 0:
                s = loser.prefixes
                drops = s.count('O') + 1000000 * s.count('N')
                current = p1
                for x in range(current+1, len(game.map)):
                    if not drops:
                        break
                    replacer = game.map[x]
                    replacer.position = current
                    loser.position = current + 1
                    current += 1
                    drops -= 1
                s.replace('N', 'B')    

            game.make_map()

        elif p1 - p2 == 2:
            victor.position = p2
            loser.position = p2 + 1
            middle = game.map[p2 - 1]
            middle.position = p2 + 2
            if p2 == 0:
                s = loser.prefixes
                drops = s.count('O') + 1000000 * s.count('N')
                current = p2 + 1
                for x in range(current+1, len(game.map)):
                    if not drops:
                        break
                    replacer = game.map[x]
                    replacer.position = current
                    loser.position = current + 1
                    current += 1      
                    drops -= 1 
                s.replace('N', 'B')          
            game.make_map()
           

    # handles who faces who        

    victor.facing = ''
    loser.facing = ''

    p2 = loser.position
    for pos in range(p2+1, len(game.bosspile)):
        p = game.map[pos]
        if 'I' not in p.suffixes:
            break
    else:
        modify_fix(loser, 'U') 

    new_face(game)

def new_face(game):
    for pos in sorted(game.map.keys()):
        player = game.map[pos]
        if 'U' in player.suffixes:
            above = pos - 1
            while True:
                above_p = game.map[above]
                suf = above_p.suffixes
                if 'I' in suf:
                    above -= 1
                    continue
                elif 'U' in suf or above_p.facing:
                    break

                above_p.facing = player.name
                player.facing = above_p.name

def modify_fix(player, newfix, add=True, suffix=True):
    # if add == False, then remove it instead
    # if suffix == False, it is a prefix
    fix = player.suffixes if suffix else player.prefixes

    if add:

        if newfix in fix:
            return 1
        
        if suffix:
            player.suffixes += newfix
        else:
            player.prefixes += newfix

    if not add:

        if newfix not in fix:
            return 1

        new_suf = ''

        for x in fix:
            if x == newfix:
                continue
            new_suf += x

        if suffix:
            player.suffixes = new_suf
        else:
            player.prefixes = new_suf

def stringify(game, defo=''):
    map_ = game.map

    z = ''

    for pos in range(len(map_)):
        player = map_[pos]
        suffixes = player.suffixes
        prefixes = player.prefixes
        facing = player.facing
        name = player.name

        z += ' '.join((prefixes, name, suffixes, 'facing' if facing else defo, facing)) +'\n'

    return z   

def print_all(game):
    print(stringify(game))

def return_discord(game):
    z = stringify(game, 'facing')

    z = z.replace('C', ':crown:')
    z = z.replace('O', ':small_orange_diamond:')
    z = z.replace('N', ':large_orange_diamond:')
    z = z.replace('B', ':large_blue_diamond:')
    z = z.replace('U', ':arrow_double_up:')
    z = z.replace('I', ':timer:')

    return z

    # need to handle facing

def read_from(z, game_name, game_id):
    """ 
    passes a string that can be returned from return_discord
    makes players, game 
    adds them to the global GAMES
    biggest problem is facing, which could be taken from some other post
    """
    global GAMES

    prefixes_map = {
    ':crown:':'C'
    ,':small_orange_diamond:':'O'
    ,':large_orange_diamond:':'N'
    ,':large_blue_diamond:':'B'}
    suffixes_map = {':arrow_double_up:':'U', ':timer:':'I'}   

    players = []

    for position, player in enumerate(z.split('\n')):
        if player == '':
            continue
        perm = player
        suffixes = ''
        prefixes = ''
        facing = ''

        index = 0
        met = False
        record = ''

        reverse = perm[::-1]

        i = reverse.find('gnicaf')

        super_index = len(perm) - i - 6

        while True:
            char = perm[index]

            if char == ':' and not record: 
                met = not met
            elif char == ':' and record or index == super_index:

                break   
            elif not met:
                if not record and char == ' ':
                    pass
                else:
                    record += char
            index += 1 
        

        name = record.rstrip()

        for prefix in prefixes_map:
            prefixes += perm.count(prefix) * prefixes_map[prefix]
            player = player.replace(prefixes_map[prefix], prefix)
        for suffix in suffixes_map:
            suffixes += perm.count(suffix) * suffixes_map[suffix] 
            player = player.replace(suffixes_map[suffix], suffix)



        if i == -1:
            facing = ''
        else:
            facing = perm[super_index+7:]

        players.append((name, prefixes, suffixes, position, facing))


    if game_name in GAMES:
       del GAMES[game_name]
   
    set_up_games((game_name,), (game_id,))

    set_up_bosspile(GAMES[game_name], players) 

    return GAMES[game_name]       

                 

            






def set_up():
    players = [
    ('norge03', 'O', '', 2, 'n i 6 t e a k'),
    ('xobxela', '', '', 1, ''),
    ('andycupid', 'C', '', 0, ''),
    ('n i 6 t e a k', '', 'U', 3, 'noreg03'),
    ('nmego', '', 'U', 4, ''),
    ('DerylG12', 'O', 'I', 5, ''),
    ('turtler7', 'BOO', 'I', 6, '')
    ]       

    game = 'stone_age'

    set_up_games((game,), (0,))

    game = GAMES[game]

    set_up_bosspile(GAMES[game.name], players)# experimental

if __name__ == '__main__':
    set_up()
