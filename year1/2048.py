from kandinsky import *
from ion import *
from time import*
from random import *

colors={
    0:(255,255,255),
    "black":(0,0,0),
    "gray":(20,20,20),
    2:(255,255,100),
    4:(255,255,50),
    8:(255,150,50),
    16:(250,130,0),
    32:(250,50,50),
    64:(250,0,0),
    128:(150,0,0),
    256:(100,0,0),
    512:(150,0,75),
    1024:(100,0,100),
    2048:(50,0,50)
}

class Game():
    def __init__(self,size):
        print("initialization")
        
        self.size=size
        self.case=215//self.size
        self.board=[[0]*self.size for _ in range(self.size)]
        self.newCase()
        self.drawScreen()
        #initializing the board
    
    def drawScreen(self):
        fill_rect(0,0,320,225,colors["gray"])
        chunk_y=10
        for y in self.board:
            chunk_x=10
            for x in y:
                fill_rect(chunk_x,chunk_y,self.case-5,self.case-5,colors[x])
                if x!=0:draw_string(str(x),chunk_x+5,chunk_y+15,colors["black"],colors[x])
                chunk_x+=self.case
            chunk_y+=self.case
           
    def horizontal(self,dir):
        print("")
        for i  in range(self.size-1):
            for index_y,cases in enumerate(self.board):
                for index_x,case in enumerate(cases):
                    #check border
                    if self.size-1==index_x and dir==1:continue
                    elif index_x==0 and dir==-1:continue
                    #check if can move
                    if self.board[index_y][index_x+dir]==0:
                        self.board[index_y][index_x+dir]=case
                        self.board[index_y][index_x]=0
                    #check if can fusion
                    elif self.board[index_y][index_x+dir]==case:
                        self.board[index_y][index_x+dir]=2*case
                        self.board[index_y][index_x]=0
            print(self.board)
        self.update()
            
    def vertical(self,dir):
        print("")
        for i  in range(self.size-1):
            for index_y,cases in enumerate(self.board):
                #check border
                if self.size-1==index_y and dir==1:continue
                elif index_y==0 and dir==-1:continue
                for index_x,case in enumerate(cases):
                    #check if can move
                    if self.board[index_y+dir][index_x]==0:
                        self.board[index_y+dir][index_x]=case
                        self.board[index_y][index_x]=0
                    #check if can fusion
                    elif self.board[index_y+dir][index_x]==case:
                        self.board[index_y+dir][index_x]=2*case
                        self.board[index_y][index_x]=0
                        print("fusion")
            print(self.board)
        self.update()
    
    def endScreen(self,game):
        global run
        draw_string(game,225,80,(255,255,255),(20,20,20))
        draw_string("Press OK",225,100,(255,255,255),(20,20,20))
        while not keydown(KEY_OK):
            pass
        run="start"
        start_page=StartPage()
        start_page.drawScreen()
        
    def newCase(self):
        #get every empty cases
        empty_cases=[]
        for index_y,cases in enumerate(self.board):
            for index_x,case in enumerate(cases):
                if case==0:empty_cases.append([index_y,index_x])
                elif case==2048: #check if reached 2048 =>  victory
                    self.endScreen("Victoire!")
                    return 0       
        if not empty_cases:      #check if no empty case => Game Over
            self.endScreen("Game Over")
            return 0
        #spawn a "2" or "4" case
        empty_case = choice(empty_cases)
        self.board[empty_case[0]][empty_case[1]] = choice([2,4])
        print("empty cases :",empty_cases, "choosen case :",empty_case)
        print(self.board)
    
    def update(self):
        self.newCase()
        self.drawScreen()

class StartPage():
    def __init__(self):
        self.level=4
        self.drawScreen()
            
    def drawScreen(self):
        fill_rect(0,0,320,225,(255,255,255))
        draw_string("Choisir une taille:",70,50)  
        if self.level==3:
            draw_string("  5x5  ",130,80)
            draw_string("  4x4  ",130,110)
            draw_string("< 3x3 >",130,140,(250,150,0))
        elif self.level==5:
            draw_string("< 5x5 >",130,80,(250,150,0))
            draw_string("  4x4  ",130,110)
            draw_string("  3x3  ",130,140)
        elif self.level==4:
            draw_string("  5x5  ",130,80)
            draw_string("< 4x4 >",130,110,(250,150,0))
            draw_string("  3x3  ",130,140)
           
    def move_up(self):
        self.drawScreen()
        if self.level<5:
            self.level+=1
            self.drawScreen()
            sleep(0.2)
                
    def move_down(self):
        self.drawScreen()
        if self.level>3:
            self.level-=1
            self.drawScreen()
            sleep(0.2)
            
def main():
    while True:
        global run
        while run=="start":
            if keydown(KEY_UP):start_page.move_up()
            elif keydown(KEY_DOWN):start_page.move_down()
            elif keydown(KEY_OK):
                game=Game(start_page.level)
                run="game"
        while run=="game":
            #check key presses
            if keydown(KEY_UP):
                game.vertical(-1)
                sleep(0.2)
                print("up!")
            elif keydown(KEY_DOWN):
                game.vertical(1)
                sleep(0.2)
                print("down...")
            elif keydown(KEY_RIGHT):
                game.horizontal(1)
                sleep(0.2)
                print("that's right")
            elif keydown(KEY_LEFT):
                game.horizontal(-1)
                sleep(0.2)
                print("I left")

run="start"
start_page=StartPage()
main()