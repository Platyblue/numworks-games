from kandinsky import *
from ion import *
from time import *
from random import *

colors = {
    "bg": (35, 35, 45),
    "black": (0, 0, 0),
    "white": (230, 230, 230),
    "red": (230, 0, 0),
    "yel": (230, 230, 0)
}
score_red = 0
score_yel = 0


class Game:
    def __init__(self):
        global score_yel, score_red

        fill_rect(0, 0, 320, 225, colors["bg"])
        for points in range(1, score_yel+1):
            fill_rect(15, 215 - 30*points, 25, 25, colors["yel"])
        for points in range(1, score_red+1):
            fill_rect(275, 215 - 30 * points, 25, 25, colors["red"])

        self.board = [[0] * 7 for _ in range(6)]
        self.selection = 3
        self.last = []
        self.last_type = 0
        self.player = choice(["red", "yel"])
        display(self)
        fill_rect(self.selection * 30 + 55, 5, 25, 25, colors[self.player])

    def update(self):
        global score_yel, score_red
        for i in range(6):
            if not self.board[5 - i][self.selection]:
                if self.player == "red":
                    self.falling_animation(self.selection*30+55, 5 - i)
                    self.board[5 - i][self.selection] = -1
                    self.last_type = -1
                    self.last = [5 - i, self.selection]
                else:
                    self.falling_animation(self.selection * 30 + 55, 5 - i)
                    self.board[5 - i][self.selection] = 1
                    self.last = [5 - i, self.selection]
                    self.last_type = 1
                break

        if self.player == "red": self.player = "yel"
        else: self.player = "red"
        self.selection = 3
        display(self)

        if self.check_victory(self.board, self.last[1], self.last[0]):
            if self.player == "red":
                draw_string("Yellow wins! PRESS OK", 55, 10, colors["white"], colors["bg"])
                score_yel += 1
            else:
                draw_string("Red wins! PRESS OK", 55, 10, colors["white"], colors["bg"])
                score_red += 1
            restart()
        else:
            fill_rect(self.selection * 30 + 55, 5, 25, 25, colors[self.player])

    def falling_animation(self, posx, height):
        for i in range(height + 1):
            fill_rect(posx, 35 + i * 30, 25, 25, colors[self.player])
            sleep(1 / ((i+1)*5))
            if i == height: break
            fill_rect(posx, 35 + i * 30, 25, 25, colors["white"])

    def check_victory(self, board, x, y):
        #vertical
        row = 0
        for i in range(7):
            if 6 > y-3+i >= 0:
                if board[y-3+i][x] == self.last_type: row += 1
                else: row = 0
                if row == 4: return True
            else: row = 0
        # horizontal
        row = 0
        for i in range(7):
            if 7 > x-3+i >= 0:
                if board[y][x-3+i] == self.last_type: row += 1
                else: row = 0
                if row == 4: return True
            else: row = 0
        # diagonal up-left down-right
        row = 0
        for i in range(7):
            if 6 > y-3+i >= 0 and 7 > x-3+i >= 0:
                if board[y-3+i][x-3+i] == self.last_type: row += 1
                else: row = 0
                if row == 4: return True
            else: row = 0
        # diagonal up-right down-left
        for i in range(7):
            if 6 > y-3+i >= 0 and 7 > x+3-i >= 0:
                if board[y-3+i][x+3-i] == self.last_type: row += 1
                else: row = 0
                if row == 4: return True
            else: row = 0


def display(game):
    # display grid
    case_y = 35
    for cases in game.board:
        case_x = 55
        for case in cases:
            if case == 0:
                fill_rect(case_x, case_y, 25, 25, colors["white"])
            elif case == 1:
                fill_rect(case_x, case_y, 25, 25, colors["yel"])
            else:
                fill_rect(case_x, case_y, 25, 25, colors["red"])
            case_x += 30
        case_y += 30


def restart():
    global game, run, score_red, score_yel
    while not keydown(KEY_OK):
        sleep(0.1)
    # clearing animation
    for i in range(5):
        game.board.insert(0, [0] * 7)
        del game.board[6]
        display(game)
        sleep(0.15)
    # check victory
    if score_yel == 6:
        fill_rect(0, 0, 320, 225, (200, 200, 50))
        draw_string("YELLOW WINS " + str(score_yel) + " to " + str(score_red), 70, 100, colors["black"],
                    (200, 200, 50))
        run = False
    elif score_red == 6:
        fill_rect(0, 0, 320, 225, (200, 50, 50))
        draw_string("RED WINS " + str(score_red) + " to " + str(score_yel), 95, 100, colors["black"], (200, 50, 50))
        run = False
    else:
        game = Game()


game = Game()
run = True

while run:
    if keydown(KEY_RIGHT) and game.selection<6:
        fill_rect(game.selection * 30 + 55, 5, 25, 25, colors["bg"])
        game.selection += 1
        fill_rect(game.selection*30+55, 5, 25, 25, colors[game.player])
        sleep(0.15)
    elif keydown(KEY_LEFT) and game.selection>0:
        fill_rect(game.selection * 30 + 55, 5, 25, 25, colors["bg"])
        game.selection -= 1
        fill_rect(game.selection*30+55, 5, 25, 25, colors[game.player])
        sleep(0.15)
    elif keydown(KEY_OK) and not game.board[0][game.selection]:
        fill_rect(game.selection * 30 + 55, 5, 25, 25, colors["bg"])
        game.update()


# Noé G
