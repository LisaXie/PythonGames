from Tkinter import *

class Connect4(object):
    def __init__(self, rows=6, cols=8):
        self.run(rows, cols)

    def mousePressed(self, event):
        if not self.gameOver:
            row, col = self.getCell(event.x, event.y)
            if (0 <= row < self.rows) and (0 <= col < self.cols):
                self.placePiece(col)
        

    def keyPressed(self, event):
        if event.char == "r":
            self.init(self.rows, self.cols)

    def getCell(self, x, y):
        row = (y - self.margin) / self.cellSize
        col = (x - self.margin) / self.cellSize
        return row, col

    def placePiece(self, col):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == 0: # found an empty cell
                self.board[row][col] = self.currentPlayer
                self.currentPlayer *= -1 # SWITCH!
                self.checkWin()
                return

    def checkWin(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.winner = self.checkWinFromCell(row, col)
                if self.winner != 0:
                    return

    def checkWinFromCell(self, row, col):
        if self.board[row][col] == 0:
            return False
        dirs = [[0,1], [1,0], [1,1], [1,-1], [0,-1], [-1,0], [-1,-1], [-1,1]]
        for direction in dirs:
            connected = self.checkWinFromCellInDir(row, col, direction)
            if connected != 0:
                return connected
        return False

    def checkWinFromCellInDir(self, row, col, direction):
        drow, dcol = direction[0], direction[1]
        for i in range(1,4):
            if row+i*drow<0 or row+i*drow>=self.rows or col+i*dcol<0 or col+i*dcol>=self.cols:
                return False
            if self.board[row][col] != self.board[row+i*drow][col+i*dcol]:
                return False
        return self.board[row][col]

    def timerFired(self):
        self.draw()
        delay = 150 # milliseconds
        # pause, then call snakeTimerFired again
        self.canvas.after(delay, self.timerFired)

    def draw(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,self.width, self.height,
            fill="yellow", outline="yellow")
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col)
        if self.winner:
            win = (3-self.winner)/2 # change -1 to 2
            self.canvas.create_text(self.width/2,self.height/2,
                text="Player %d wins!" % win, font="Arial 30", fill="blue")
            self.gameOver = True


    def drawCell(self, row, col):
        if self.board[row][col] == 0:
            color = "white"
        elif self.board[row][col] == 1:
            color = "red"
        elif self.board[row][col] == -1:
            color = "black"
        self.canvas.create_oval(self.margin+self.cellSize*col+4, self.margin+self.cellSize*row+4,
            self.margin+self.cellSize*(col+1)-4, self.margin+self.cellSize*(row+1)-4, fill=color)

    def init(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.cellSize = 60
        self.margin = 20
        self.board = [[0] * self.cols for i in range(self.rows)]
        self.currentPlayer = 1
        self.gameOver = False
        self.winner = 0

    def run(self, rows, cols):
        # create the root and the canvas
        root = Tk()
        self.init(rows, cols)
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

connect = Connect4()