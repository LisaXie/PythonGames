##### MineSweeper #######

# [type,status] types: -1 == bomb, 0 == blank, 1-8 == no of bombs
#               status: 0 == closed, 1 == open, 2 == flagged

import sys, Tkinter
sys.modules['tkinter'] = Tkinter 
from Tkinter import *
import random
import Pmw



class MineSweeper(object):
    def __init__(self, bombs, rows=10, cols=14):
        self.run(bombs, rows, cols)

    def mousePressed(self, event):
        if not self.gameOver:
            row, col = self.getCell(event.x, event.y)
            if (0 <= row < self.rows) and (0 <= col < self.cols):
                self.board[row][col][1] = 1
                if self.board[row][col][0] == -1: # Opened A BOMB! BOOOM
                    self.gameOver = True
                elif self.board[row][col][0] == 0: # Opened a blank
                    self.clearBlanks
                # print "row, col", row, col, "value", self.board[row][col]

    def keyPressed(self, event):
        pass

    def timerFired(self):
        self.draw()
        delay = 150 # milliseconds
        # pause, then call snakeTimerFired again
        self.canvas.after(delay, self.timerFired)

    def getCell(self, x, y):
            row = (y - self.margin) / self.cellSize
            col = (x - self.margin) / self.cellSize
            return row, col

    def draw(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0, self.width, self.height, fill="grey50")
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col)
        if self.gameOver:
            self.canvas.create_text(self.width/2, self.height/2, font = "Arial 50 bold", fill = "red", text = "....BOOM!!\nYou blew up!")

    def drawCell(self, row, col):
        if self.board[row][col][1] == 0: # It is a closed cell
            self.canvas.create_rectangle(self.margin+self.cellSize*col, self.margin+self.cellSize*row,
                self.margin+self.cellSize*(col+1), self.margin+self.cellSize*(row+1), fill = "grey88", activefill = "white")
        elif self.board[row][col][1] == 2: # It is a flagged cell
            self.canvas.create_oval(self.margin+self.cellSize*col, self.margin+self.cellSize*row,
                self.margin+self.cellSize*(col+1), self.margin+self.cellSize*(row+1), fill = "cherry")
        else: # It is an open cell
            if self.board[row][col][0] == -1: # Bomb
                self.canvas.create_rectangle(self.margin+self.cellSize*col, self.margin+self.cellSize*row,
                    self.margin+self.cellSize*(col+1), self.margin+self.cellSize*(row+1), fill = "grey69")
                self.canvas.create_oval(self.margin+self.cellSize*col, self.margin+self.cellSize*row,
                    self.margin+self.cellSize*(col+1), self.margin+self.cellSize*(row+1), fill = "black")
            elif self.board[row][col][0] == 0: # Blank
                self.canvas.create_rectangle(self.margin+self.cellSize*col, self.margin+self.cellSize*row,
                    self.margin+self.cellSize*(col+1), self.margin+self.cellSize*(row+1), fill = "grey69")
            else: # Number
                self.canvas.create_rectangle(self.margin+self.cellSize*col, self.margin+self.cellSize*row,
                    self.margin+self.cellSize*(col+1), self.margin+self.cellSize*(row+1), fill = "grey69")
                self.canvas.create_text(self.margin+self.cellSize*(col+.5), self.margin+self.cellSize*(row+.5), text=str(self.board[row][col][0]), font="Arial 30")

    def clearBlanks(self):
        dirs = [[0,1],[0,-1],[1,0],[-1,0],[-1,-1],[1,1],[1,-1],[-1,1]]
        for direction in dirs:
            drow, dcol = direction[0], direction[1]
            if row+drow<0 or row+drow>=self.rows or col+dcol<0 or col+dcol>=self.cols:
                return False


    def placeBombs(self):
        placedBombs = 0
        while placedBombs < self.bombs:
            row, col = random.randint(0,self.rows-1), random.randint(0,self.cols-1) # Generate random coordinates
            if self.board[row][col][0] == 0:
                self.board[row][col][0] = -1
                placedBombs += 1
                self.declareTHEExistanceofTHEBombToTheNeigbouringCells(row,col)

    def declareTHEExistanceofTHEBombToTheNeigbouringCells(self, row, col):
        dirs = [[0,1],[0,-1],[1,0],[-1,0],[-1,-1],[1,1],[1,-1],[-1,1]]
        for direction in dirs:
            drow, dcol = direction[0], direction[1]
            if row+drow<0 or row+drow>=self.rows or col+dcol<0 or col+dcol>=self.cols:
                return False
            if self.board[row+drow][col+dcol][0] != -1:
                self.board[row+drow][col+dcol][0] += 1


    def init(self, bombs, rows, cols):
        self.bombs, self.rows, self.cols= bombs, rows, cols
        print bombs
        self.cellSize = 30
        self.margin = 10
        self.board = [[[0,0] for col in range(cols)] for row in range(rows)]
        self.placeBombs()
        self.gameOver = False


    def run(self, bombs, rows, cols):
        # create the root and the canvas
        root = Tk()
        self.init(bombs, rows, cols)
        self.width = self.cols*self.cellSize+self.margin*2
        self.height = self.rows*self.cellSize+self.margin*2
        self.canvas = Canvas(root, width=self.width, 
            height=self.height)
        self.canvas.pack()
        self.draw()
        # set up events
        root.bind("<Button-1>", self.mousePressed)
        root.bind("<Key>", self.keyPressed)
        self.timerFired()
        # and launch the app
        root.mainloop() # This calls BLOCKS

master = Tk()
master = Pmw.initialise()

global  DIFICULTIES

DIFICULTIES = ["easy", "medium", "hard", "impossubruu"]

class Menu:

    def __init_(self, parent):
        # Create and pack Options Menu megawidget
        # This has a textvariable.

        self.variable = Tkinter.StringVar()
        self.var.set(DIFICULTIES[0])
        self.dropDown = Pmw.OptionMenu(parent,
            label_text = "Choose Difficulty:",
            items = DIFICULTIES
            )
        self.dropDown.pack(anchor='w', padx = 10, pady =10)

    def startGame(self):
        diffuculty = self.variable.get()
        if diffuculty == "easy":
            MineSweeper(random.randint(5,7))
        elif diffuculty == "medium":
            MineSweeper(random.randint(10,12))
        elif diffuculty == "hard":
            MineSweeper(random.randint(15,17))
        else:
            MineSweeper(random.randint(20,25))
        master.quit()
    
    button = Button(master, text="Start Game", command=startGame())
    button.pack()

Menu()

mainloop()
#dropDown = Pmw.OptionMenu(master, label_text = "Choose Difficult:")

#variable = StringVar(master)
#variable.set(DIFICULTIES[0]) # default value


#print variable.get()

   