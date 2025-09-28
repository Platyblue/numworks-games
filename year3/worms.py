from kandinsky import *
from ion import *
from time import *
from random import randint

col={
    'dirt': (150, 90, 30),
    'worm': (230, 90, 130),
    'stripe': (210, 70, 110),
    'apple': (250, 0, 0),
    'portal': (70, 10, 130),
    'grass': (0,200,20),
}
c1, c2 = col['grass'], col['dirt']

def show(object, pos, rot=None):
    if object == 'apple':
        fill_rect(15*pos[0] + 2, 15*pos[1] + 3, 11, 11, col['apple'])
        fill_rect(15 * pos[0] + 4, 15 * pos[1], 4, 3, (0,250,0))
    elif object == 'portal':
        fill_rect(15*pos[0], 15*pos[1], 15, 15, col['portal'])
    else:
        if object == 'head':
            coords = coords_rotation([[2,0,11,12,], [2,12,11,3], [3,2,3,3], [9,2,3,3],[4,2,2,2],[9,2,2,2]], rot)
            cols= (col['worm'],col['stripe'], (250,250,250), (250, 250, 250),(0,0,0),(0,0,0))
        elif object == 'cornerR':
            coords = coords_rotation([[2, 0,11,13], [13, 2,2,11], [10,2,3,11]], rot)
            cols=(col['worm'],col['worm'],col['stripe'])
        elif object == 'cornerL':
            coords = coords_rotation([[2, 0,11,13], [0, 2,2,11], [2,2,3,11]], rot)
            cols = (col['worm'], col['worm'], col['stripe'])
        elif object == 'straight':
            coords = coords_rotation([[2, 0,11,12], [2,12,11,3]], rot)
            cols = (col['worm'], col['stripe'])
        elif object == 'enter_straight':
            coords = coords_rotation([[2, 5,11,7], [2,12,11,3]], rot)
            cols = (col['worm'], col['stripe'])
        elif object == 'exit_head':
            coords = coords_rotation([[2, 0, 11, 12], [3,2,3,3], [9,2,3,3],[4,2,2,2],[9,2,2,2]], rot)
            cols = (col['worm'], (250, 250, 250), (250, 250, 250),(0,0,0),(0,0,0))
        elif object == 'exit_straight':
            coords = coords_rotation([[2, 0, 11, 12]], rot)
            cols = [col['worm']]
        for i in range(len(coords)):
            fill_rect(15*pos[0] + coords[i][0], 15*pos[1] + coords[i][1], coords[i][2], coords[i][3], cols[i])

def coords_rotation(coords, rot):
    if rot == (0,1):
        for i in range(len(coords)):
            coords[i][1] = 15-coords[i][1]
            coords[i][0] = 15 - coords[i][0]
            coords[i][2] = -coords[i][2]
            coords[i][3] = -coords[i][3]
    elif rot == (-1,0):
        for i in range(len(coords)):
            coords[i][0], coords[i][1] = coords[i][1], 15-coords[i][0]
            coords[i][2], coords[i][3] = coords[i][3], -coords[i][2]
    elif rot == (1,0):
        for i in range(len(coords)):
            coords[i][0], coords[i][1] = 15-coords[i][1], coords[i][0]
            coords[i][2], coords[i][3] = -coords[i][3], coords[i][2]
    return coords

def generate(H,W,worm,portals):
    grid = [(x,y) for x in range(W) for y in range(H)]
    spawnable = [i for i in grid if (i not in worm and i not in portals)]
    if len(spawnable)>1:
        a = spawnable.pop(randint(0,len(spawnable)-1))
        return [a, spawnable[randint(0,len(spawnable)-1)]]

def game(H=15,W=18,delay=30):
    global col
    fill_rect(0,0,320,225,col['grass'])
    score = 0
    head = (W//2,H-2)
    dir, dir1, key = (0, -1), (0, -1), 'up'
    worm = [head, (head[0],head[1]+1)]
    portals = [(-1,-1), (-1,-1)]
    apples = generate(H,W,worm,portals)
    dead = False
    fill_rect(0,0,W*15,H*15, col['dirt'])
    draw_string("SCORE:", 270, 60, (30, 30, 30), col['grass'])
    draw_string('0', 290, 80, (30, 30, 30), col['grass'])
    show('head', head, dir)
    show('straight', worm[1], dir)
    show('apple', apples[0])
    show('apple', apples[1])
    t = monotonic() + 1 + delay
    while not dead:
        #delay
        k=None
        sleep((delay>5)*0.1)
        while t>monotonic() and (delay<5 or not k):
            sleep(0.05)
            if keydown(KEY_UP) and (dir!=(0,1) or worm[0] in portals): k='up'
            elif keydown(KEY_DOWN) and (dir!=(0,-1) or worm[0] in portals): k='down'
            elif keydown(KEY_RIGHT) and (dir!=(-1,0) or worm[0] in portals): k='right'
            elif keydown(KEY_LEFT) and (dir!=(1,0) or worm[0] in portals): k='left'
        t = monotonic() + delay
        if k!= None: key=k

        #movement: /////////////Credits à/to Noé le boss/////////////////
        tail = worm.pop()
        if key=='up': dir1 = (0,-1)
        elif key=='down': dir1 = (0,1)
        elif  key=='right': dir1 = (1,0)
        elif key=='left': dir1 = (-1,0)
        if worm[0] in portals:
            fill_rect(worm[0][0] * 15, worm[0][1] * 15, 15, 15, col['portal'])
            show('exit_straight', worm[0], dir1)
        elif dir!=dir1:
            fill_rect(worm[0][0] * 15, worm[0][1] * 15, 15, 15, col['dirt'])
            if (dir,dir1) in (((-1,0),(0,-1)), ((0,-1),(1,0)), ((1,0),(0,1)), ((0,1),(-1,0))):
                show('cornerR', worm[0], dir1)
            else:
                show('cornerL', worm[0], dir1)
        else: show('straight', worm[0], dir)
        head = (head[0]+dir1[0],head[1]+dir1[1])
        dir = dir1

        #position checks
        if head in apples:
            score+=1
            draw_string("SCORE:",270, 60, (30,30,30), col['grass'])
            draw_string(str(score), (5-len(str(score)))*5 + 270, 80, (30,30,30), col['grass'])
            p = (head==apples[0])
            portals = [apples[p],apples[not p]]
            col["portal"] = (randint(5,25)*5,randint(5,15)*5,randint(5,45)*5)
            generation_output = generate(H,W,worm,portals)
            if generation_output:
                fill_rect(tail[0] * 15, tail[1] * 15, 15, 15, col['dirt'])
                apples = generation_output
            else: dead = "False but victory"
            for i in range(2):
                show('apple', apples[i])
                show('portal', portals[i])
            worm.insert(0,head)
            show('enter_straight', head, dir)
            head = portals[0]
            show('exit_head', head, dir)
        else:
            fill_rect(tail[0] * 15, tail[1] * 15, 15, 15, col['dirt'])
            show('head', head, dir)
        if head[0] not in range(W) or head[1] not in range(H) or head in worm: dead = "yes"
        worm.insert(0,head)
    if dead=="yes":
        draw_string('YOU DEAD',100,82,(0,250,200),(250,50,200))
        draw_string('OK to play again', 60, 100, (0, 0, 0), col['dirt'])
        print("You died.\nApples eaten: ", score)
    else:
        draw_string('YOU FAT BUT NOT DEAD',45,82,(250,50,200),(0,250,200))
        draw_string('OK to play again', 60, 100, (0, 0, 0), col['dirt'])
        print("You won: ", score)

L=input("LENGTH : ")
delay=input("DELAY : ")
while 1:
    try:
        game(int(L),int(L),float(delay))
    except:
        game(15, 18, 0.2)
    while not keydown(KEY_OK):
        sleep(0.2)
        c1, c2 = c2, c1
        draw_string('OK to play again', 60, 100, c2, c1)
