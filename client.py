import os
import discord
from dotenv import load_dotenv

import bot_test
import bosspile as b

save = ''


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 630394016663470101

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild.name, guild.id)

@client.event
async def on_message(message):
    global save
    save = ''
    m = message.content.split(';')
    print(m)
    if m[0][0] == '!':
        if m[0][1:] == 'victory' and len(m) == 3:
            victory(m[1], m[2])
        elif m[0][1:] == 'remove' and len(m) == 2:
            remove(m[1])        
        elif m[0][1:] == 'add' and len(m) == 2:
            add(m[1]) 
        elif m[0][1:] == 'inactive' and len(m) == 2:
            inactive(m[1])
        elif m[0][1:] == 'active' and len(m) == 2:
            active(m[1])
        elif m[0][1:] == 'print':
            await message.channel.send(print_bosspile())
        print('hi')    


    if save:
            chn = client.get_channel(CHANNEL_ID)
            await chn.send(save)

           




# start bosspile with initial state 
# also send the matches

# register victory
def victory(victor, loser):
    game = load_bosspile()

    b.victory(game, victor, loser)

    save_bosspile(game)

# remove player from bosspile
def remove(name):
    game = load_bosspile()
    player = game.bosspile[name]
    position = player.position

    del game.bosspile[name]

    names = []

    for i in range(position, len(game.bosspile)):
        names.append(game.map[i]) 

    for name in names:
        name.position -= 1    

    game.make_map()
    b.new_face(game)

    save_bosspile(game)

# add player to bosspile
def add(name):
    game = load_bosspile()

    position = len(game.bosspile)
    
    player = b.Player(name, '', '', position)

    game.bosspile[name] = player
    game.make_map()
    b.new_face(game)

    save_bosspile(game)

# make a player inactive
def inactive(name):
    game = load_bosspile()
    player = game.bosspile[name]
    b.modify_fix(player, 'I')
    save_bosspile(game)

# make a player active
def active(name):
    game = load_bosspile()
    player = game.bosspile[name]
    b.modify_fix(player, 'I', add='False')
    save_bosspile(game)

# print bosspile
def print_bosspile():
    bosspile = load_bosspile()
    return b.return_discord(bosspile)


    
# a function that is called by everything that loads the bosspile from the discord
def load_bosspile():
    chn = client.get_channel(CHANNEL_ID)
    last = chn.last_message
    print(last)
    if last is None:
        last = """:small_orange_diamond::crown: norge03  facing 
xobxela  facing 
:small_orange_diamond: andycupid  facing 
nmego  facing n i 6 t e a k
n i 6 t e a k :arrow_double_up: facing nmego
:small_orange_diamond: DerylG12 :timer: facing 
:large_blue_diamond::small_orange_diamond::small_orange_diamond: turtler7 :timer: facing"""

    else:
        last = last.content
    return b.read_from(last, 'stoneage', 4)


def save_bosspile(bosspile):
    pile = b.return_discord(bosspile)
    global save
    save = pile




client.run(token)    
