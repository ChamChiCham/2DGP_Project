
# object
buttons = []
balls = []

cue = None
player = None

def clear():
    global buttons, balls, cue, player

    buttons.clear()
    balls.clear()

    cue = None
    player = None

# common data
player_count = None
target_score = 10