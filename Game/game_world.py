# #####
# game_world.py: 게임 월드 내 객체를 관리하는 파일
# #####

# objects: 객체를 저장 / depth = 0 ~ 3
objects = [[], [], [], []]

# ---
# add_object(o, depth): 객체 o를 추가한다.
# ---
def add_object(o, depth = 0):
    objects[depth].append(o)

# ---
# update(): 모든 객체를 업데이트한다.
# ---
def update():
    for layer in objects:
        for o in layer:
            o.update()

# ---
# render(): 모든 객체를 그린다.
# ---
def render():
    for layer in objects:
        for o in layer:
            o.draw()

# ---
# remove_object(o): 객체 o를 제거한다.
# ---
def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return