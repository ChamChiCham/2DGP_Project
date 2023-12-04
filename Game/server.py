from pico2d import load_font

# object
buttons = []
balls = []

cue = None
player = None
winner = None
guide = False

def clear():
    global buttons, balls, cue, player, winner

    buttons.clear()
    balls.clear()

    cue = None
    player = None
    winner = None
    guide = False


# common data
player_count = None
target_score = 10