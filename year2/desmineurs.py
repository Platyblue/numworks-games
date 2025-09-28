from kandinsky import *
from ion import *
from time import *
from random import *

def reveal(x,y):
    global revealed
    if revealed[y][x]==1:
        return
    fill_rect(x*20+21, y*20+41, 18, 18, col["brown"])
    value = grid[y][x]
    revealed[y][x] = 1
    if value=='b':
        fill_rect(x * 20 + 26, y * 20 + 42, 8, 4, (250,50,0))
        fill_rect(x * 20 + 27, y * 20 + 43, 6, 4, (250, 150, 50))
        fill_rect(x * 20 + 25, y * 20 + 46, 10, 10, col["black"])
        fill_rect(x * 20 + 28, y * 20 + 44, 4, 2, col["black"])
        end(False)
    elif value=='0':
        for i in range(3):
            for j in range(3):
                if 0<=i+y-1<dimensions[0] and 0<=j+x-1<dimensions[1]:
                    if revealed[i+y-1][j+x-1]!=1:
                        reveal(x+j-1,y+i-1)
    else:
        draw_string(str(value),x*20+24,y*20+41,col[str(value)],get_pixel(x*20+24,y*20+42))
    if sum(x.count('0') for x in revealed)==bomb_number: end(True)

def end(win):
    sleep(2)
    fill_rect(0,0,320,225,col["bg"])
    if win:
        draw_string("GOOD GAME!", 110, 70, col["gray"], col["bg"])
    else:
        draw_string("GAME OVER", 115, 70, col["gray"], col["bg"])
    draw_string("FINAL TIME: " + time + "s", 85, 90, col["gray"], col["bg"])
    draw_string("OK to PLAY", 110, 110, col["gray"], col["bg"])
    while not keydown(KEY_OK):
        pass
    sleep(0.3)
    generate()

def input():
    global cursorX,cursorY,flags,flags_left
    if keydown(KEY_OK) and not flags[cursorY][cursorX]:
        reveal(cursorX,cursorY)
        sleep(0.1)
    if keydown(KEY_BACKSPACE):
        if not flags[cursorY][cursorX]:
            flags_left-=1
            fill_rect(cursorX * 20 + 25, cursorY * 20 + 43, 10, 8, col["flag"])
            fill_rect(cursorX * 20 + 32, cursorY * 20 + 47, 3, 10, col["flag"])
            flags[cursorY][cursorX] = 1
        else:
            flags_left+=1
            fill_rect(cursorX * 20 + 25, cursorY * 20 + 43, 10, 14, get_pixel(cursorX*20+24,cursorY*20+42))
            flags[cursorY][cursorX] = 0
        fill_rect(150,12,25,20,col["bg"])
        draw_string(str(flags_left), 170-len(str(flags_left))*10, 12, col["gray"], col["bg"])
        sleep(0.1)
    if keydown(KEY_UP) and cursorY>0:
        unrender_cursor(cursorX,cursorY)
        cursorY -= 1
        render_cursor(cursorX,cursorY)
    if keydown(KEY_DOWN) and cursorY<dimensions[0]-1:
        unrender_cursor(cursorX, cursorY)
        cursorY += 1
        render_cursor(cursorX, cursorY)
    if keydown(KEY_LEFT) and cursorX>0:
        unrender_cursor(cursorX, cursorY)
        cursorX -= 1
        render_cursor(cursorX, cursorY)
    if keydown(KEY_RIGHT) and cursorX<dimensions[1]-1:
        unrender_cursor(cursorX, cursorY)
        cursorX += 1
        render_cursor(cursorX, cursorY)

def unrender_cursor(x,y):
    fill_rect(x * 20 + 19, y * 20 + 39, 2, 22, col["bg"])
    fill_rect(x * 20 + 39, y * 20 + 39, 2, 22, col["bg"])
    fill_rect(x * 20 + 21, y * 20 + 39, 18, 2, col["bg"])
    fill_rect(x * 20 + 21, y * 20 + 59, 18, 2, col["bg"])

def render_cursor(x,y):
    fill_rect(x*20+19,y*20+39,2,22,col["gray"])
    fill_rect(x * 20 + 39, y * 20 + 39, 2, 22, col["gray"])
    fill_rect(x * 20 + 21, y * 20 + 39, 18, 2, col["gray"])
    fill_rect(x * 20 + 21, y * 20 + 59, 18, 2, col["gray"])
    sleep(0.05)

def generate():
    global cursorX, cursorY, grid, revealed, flags, flags_left, start_time
    start_time = monotonic()
    cursorX = (dimensions[1]-1)//2
    cursorY = (dimensions[0]-1)//2
    grid = [['0' for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    revealed= [['0' for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    flags=[[0 for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    flags_left=bomb_number
    # Terrain and bombs generating
    pair=True
    fill_rect(0,0,320,225,col["bg"])
    fill_rect(175,14, 10, 8, col["flag"])
    fill_rect(182,18, 3, 10, col["flag"])
    draw_string(str(bomb_number), 150, 12, col["gray"], col["bg"])
    for y in range(40,dimensions[0]*20+40,20):
        pair = not pair
        for x in range(20,dimensions[1]*20+20,20):
            pair = not pair
            if pair: fill_rect(x+1,y+1,18,18,col["green1"])
            else: fill_rect(x+1,y+1,18,18,col["green2"])
    indices = set()
    while len(indices) < 10:
        index = randint(0, len(grid) * len(grid[0]) - 1)
        indices.add(index)
    for index in indices:
        grid[index // len(grid[0])][index % len(grid[0])] = "b"
    # Calculate number of adjacents bombs
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if grid[i][j] != 'b':
                count = 0
                for x in range(max(0, i-1), min(dimensions[0], i+2)):
                    for y in range(max(0, j-1), min(dimensions[1], j+2)):
                        if grid[x][y] == 'b':
                            count += 1
                grid[i][j] = str(count)
    render_cursor(cursorX, cursorY)

col={
    "bg":(70,40,30),
    "green1":(60,240,60),
    "green2":(90,250,90),
    "brown":(235, 166, 87),
    "1":(0,50,200),
    "2":(0,180,50),
    "3":(200,0,50),
    "4":(0,0,150),
    "5":(200,50,200),
    "6": (0, 0, 0),
    "7": (0, 0, 0),
    "8": (0, 0, 0),
    "gray":(230,230,230),
    "flag":(200,10,10),
    "black":(0,0,0),
}
dimensions = (8,10)
bomb_number = 10
time=0
generate()
while True:
    if time != str(round(monotonic()-start_time)):
        time=str(round(monotonic()-start_time))
        draw_string("time: "+time+"s", 20, 12, col["gray"],col["bg"])
    input()
    sleep(0.05)

