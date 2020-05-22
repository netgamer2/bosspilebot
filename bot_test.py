from bosspile import *
set_up()

s = GAMES['stone_age']

def test():
    victory(s, 'norge03', 'n i 6 t e a k')
    victory(s, 'nmego', 'n i 6 t e a k')
    victory(s, 'xobxela', 'norge03')
    victory(s, 'andycupid', 'xobxela')
    victory(s, 'norge03', 'nmego')
    victory(s, 'norge03', 'xobxela')

    print_all(s)
    read_from(return_discord(s), s.name, s.channel_id)
    print()
    print()
    print_all(s)
    print()
    print()
    print()
    victory(s, 'norge03', 'andycupid')
    print_all(s)
    read_from(return_discord(s), s.name, s.channel_id)
    print()
    print()
    print_all(s)
    import pyperclip
    pyperclip.copy(return_discord(s))

def get_pile():
    victory(s, 'norge03', 'n i 6 t e a k')
    victory(s, 'nmego', 'n i 6 t e a k')
    victory(s, 'xobxela', 'norge03')
    victory(s, 'andycupid', 'xobxela')
    victory(s, 'norge03', 'nmego')
    victory(s, 'norge03', 'xobxela')
    read_from(return_discord(s), s.name, s.channel_id)
    victory(s, 'norge03', 'andycupid')
    read_from(return_discord(s), s.name, s.channel_id)
    return s