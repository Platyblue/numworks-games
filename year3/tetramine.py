from kandinsky import *
from ion import *
from time import *
from random import randint

col = {
    'bg': (10, 50, 160),
    'grid': (30, 30, 50),
    'placed': (200, 0, 0),
    'taken': (220, 60, 80),
    'vacant': (230, 80, 100),
    'Bgrid': (80, 80, 100),
    'Bplaced': (240, 40, 40),
    'Btaken': (240, 90, 110),
    'Bvacant': (250, 110, 130),
}
H, L = 4, 17
t = 0.1
tetraminoes = {
    1: ((0,0), (1,0), (2,0), (1,1), (3, 2)),
    2: ((0,0), (0,1), (0,2), (0,3), (1, 4)),
    3: ((0, 0), (1, 0), (0, 1), (0, 2), (2, 3)),
    4: ((0, 0), (0, 1), (1, 1), (0, 2), (2, 3)),
    5: ((0, 0), (0, 1), (0, 2), (1, 2), (2, 3)),
    6: ((1, 0), (0, 1), (1, 1), (0, 2), (2, 3)),
    7: ((0, 0), (1, 0), (0, 1), (1, 1), (2, 2)),
    8: ((0, 0), (1, 0), (2, 0), (0, 1), (3, 2)),
    9: ((0, 0), (0, 1), (1, 1), (1, 2), (2, 3)),
    10: ((0, 0), (0, 1), (1, 1), (2, 1), (3, 2)),
    11: ((1, 0), (1, 1), (0, 2), (1, 2), (2, 3)),
    12: ((1, 0), (0, 1), (1, 1), (1, 2), (2, 3)),
    13: ((1, 0), (2, 0), (0, 1), (1, 1), (3, 2)),
    14: ((1, 0), (0, 1), (1, 1), (2, 1), (3, 2)),
    15: ((0, 0), (1, 0), (1, 1), (1, 2), (2, 3)),
    16: ((0, 0), (1, 0), (1, 1), (2, 1), (3, 2)),
    17: ((2, 0), (0, 1), (1, 1), (2, 1), (3, 2)),
    18: ((0, 0), (1, 0), (2, 0), (2, 1), (3, 2)),
    19: ((0, 0), (1, 0), (2, 0), (3, 0), (4, 1))
}

def Rotation(piece, sens=1):
    rotations = ((1,12,14,4),(3,18,11,10),(8,15,17,5),(6,16),(9,13),(2,19))
    number = list(tetraminoes.keys())[list(tetraminoes.values()).index(piece)]
    for type in rotations:
        for i in range(len(type)):
            if type[i] == number: return tetraminoes[type[(i+sens)%len(type)]]

def Mino(x,y, type='placed', scale=20):
    fill_rect(x, y, scale, 3, col['B'+type])
    fill_rect(x, y+3, 3, scale-3, col['B' + type])
    fill_rect(x+3, y+3, scale-3, scale-3, col[type])
def Selector(number):
    global selector
    selector = number
    fill_rect(40, 138, 270, 6, col['bg'])
    fill_rect(40 + 90*number, 138, 60, 6, (250, 200, 0))
    Hologram(Pieces[selector])
def Hologram(piece):
    global grid, cursor
    if cursor[0] + piece[4][0] > len(grid[0]): cursor[0] = len(grid[0]) - piece[4][0]
    if cursor[1] + piece[4][1] > H: cursor[1] = H - piece[4][1]
    for y in range(H):
        for x in range(len(grid[0])):
            if grid[y][x] > 1: grid[y][x] -= 2
    for mino in range(4):
        x = piece[mino][0] + cursor[0]
        y = piece[mino][1] + cursor[1]
        if grid[y][x]==0:
            grid[y][x] = 2
        else:
            grid[y][x] = 3
    show(show_offset)

def show(offset=0):
    for y in range(H):
        for x in range(len(grid[0])-1, -1, -1):
            if grid[y][len(grid[0])-1-x] == 1: Mino(320 - x*20 - offset, y*20 + 45, 'placed')
            elif grid[y][len(grid[0])-1-x] == 2: Mino(320 - x*20 - offset, y*20 + 45, 'vacant')
            elif grid[y][len(grid[0])-1-x] == 3: Mino(320 - x*20 - offset, y * 20 + 45, 'taken')
            else:
                fill_rect(320 - x * 20 - offset, y * 20 + 45, 20, 20, col['Bgrid'])
                fill_rect(321 - x * 20 - offset, y * 20 + 46, 18, 18, col['grid'])

def newPieces():
    pieces=[None, None, None]
    randlist = list(range(1,20))
    fill_rect(25, 125, 270, 100, col['bg'])
    for i in range(3):
        r = randint(0, len(randlist)-1)
        pieces[i] = tetraminoes[randlist[r]]
        del randlist[r]
        for mino in range(4):
            Mino(int((pieces[i][mino][0] - pieces[i][4][0]/2)*16 + 90*i + 70), int((pieces[i][mino][1] - pieces[i][4][1]/2)*16 + 180), scale=16)
    return pieces

fill_rect(0, 0, 320, 225, col['bg'])
draw_string('PRESS OK TO PLAY !', 70, 95, (255,255,255), col['bg'])
while 1:
    while not keydown(KEY_OK):
        sleep(0.05)
    grid = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    dead = False
    speed = 80
    lastMove = 0
    selector = 0
    cursor = [0, 0]
    show_offset = 0
    score = 0
    c = 0
    last_rot = -2
    fill_rect(0, 0, 320, 225, col['bg'])
    draw_string('TETRAMINE', 0, 0, (250, 180, 50), col['bg'])
    draw_string('SCORE : 0', 100, 25, (255, 255, 255), col['bg'])
    Pieces = newPieces()
    Selector(0)
    show()
    Hologram(Pieces[selector])
    T = monotonic() + 0.5
    while not dead:
        if monotonic() > T:
            T += t
            lastMove += 1
            c += 1
            if speed > 40: speed = round(80 - c*0.07)
            if keydown(KEY_ALPHA) and selector!=0 and bool(Pieces[0]): Selector(0)
            elif keydown(KEY_XNT) and selector!=1 and bool(Pieces[1]): Selector(1)
            elif keydown(KEY_VAR) and selector!=2 and bool(Pieces[2]): Selector(2)
            if keydown(KEY_SHIFT) and Pieces[selector][4]!=(2, 2) and c-last_rot>1:
                Pieces[selector] = Rotation(Pieces[selector], -1)
                Hologram(Pieces[selector])
                last_rot = c
            elif (keydown(KEY_TOOLBOX) or keydown(KEY_BACKSPACE)) and Pieces[selector][4]!=(2, 2) and c-last_rot>1:
                Pieces[selector] = Rotation(Pieces[selector])
                Hologram(Pieces[selector])
                last_rot = c
            if not (keydown(KEY_SHIFT) or keydown(KEY_TOOLBOX) or keydown(KEY_BACKSPACE)): last_rot=-2
            if keydown(KEY_DOWN) and cursor[1]+Pieces[selector][4][1]<4:
                cursor[1]+=1
                Hologram(Pieces[selector])
            if keydown(KEY_UP) and cursor[1] > 0:
                cursor[1] -= 1
                Hologram(Pieces[selector])
            if keydown(KEY_RIGHT) and cursor[0]+Pieces[selector][4][0] < len(grid[0]):
                cursor[0] += 1
                Hologram(Pieces[selector])
            if keydown(KEY_LEFT) and cursor[0] > 0:
                cursor[0] -= 1
                Hologram(Pieces[selector])
            if keydown(KEY_OK) and max(list(map(max, grid)))==2:
                for y in range(H):
                    for x in range(len(grid[0])):
                        if grid[y][x] == 2: grid[y][x] = 1
                Pieces[selector] = None
                fill_rect(25+90*selector, 125, 90, 100, col['bg'])
                if Pieces == [None, None, None]:
                    Pieces = newPieces()
                    Selector(0)
                else: Selector(min([0,1,2], key=lambda x: x if bool(Pieces[x]) else 10))
            if lastMove == speed or lastMove == round(80 - (c-1)*0.07): #move
                lastMove = 0
                if grid[0][0] and grid[1][0] and grid[2][0] and grid[3][0] and len(grid[0])==L:
                    for i in range(4):
                        del grid[i][0]
                        grid[i].append(0)
                        score += 1
                        draw_string('SCORE : ' + str(score), 100, 25, (255,255,255), col['bg'])
                elif len(grid[0])<L:
                    for i in range(4): grid[i].append(0)
                else: dead = True
                show_offset = 0
                show()
            elif c%2==0:
                show_offset = round((20*lastMove)/speed)
                show(show_offset)
    draw_string('GAME OVER '+str(score), 90, 25, (255,255,255), col['bg'])
    sleep(0.5)
    draw_string('PRESS OK TO PLAY AGAIN!', 40, 76, (255,255,255), col['grid'])
