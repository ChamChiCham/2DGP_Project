# #####
# game_world.py: 게임 월드 내 객체를 관리하는 파일
# #####

# objects: 객체를 저장 / depth = 0 ~ 3
objects = [[], [], [], []]

collision_pairs = {}

# ---
# add_object(o, depth): 객체 o를 추가한다.
# ---
def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol

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

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o) # 시각적 월드에서 지운다.
            remove_collision_object(o) # 충돌 그룹에서 삭제
            del o
            return
    raise ValueError('Cannot delete non existing object')

def clear():
    for layer in objects:
        layer.clear()

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

# { 'boy:ball' : [[boy], [ball1, ...]]}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f"New Group {group} Added")
        collision_pairs[group] = [[], []]
    if a: # a가 있을 때, 즉 a가
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
