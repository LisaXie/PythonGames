#########################################
################ TETRIS #################
#########################################

from Tkinter import *
from random import randint
from copy import copy

def tetrisMousePressed(event, canvas):
    tetrisRedrawAll(canvas)

def tetrisKeyPressed(event, canvas):
    canvas.data.ignoreNextTimerEvent = True
    if (event.keysym == "Up"):
        rotateFallingPiece(canvas)
    elif (event.keysym == "Down"):
        moveFallingPiece(canvas, +1, 0)
    elif (event.keysym == "Left"):
        moveFallingPiece(canvas, 0,-1)
    elif (event.keysym == "Right"):
        moveFallingPiece(canvas, 0,+1)
    elif (event.char == "r"):
        tetrisInit(canvas)
    elif (event.char == "q"):
        canvas.data.isGameOver = True
    #canvas = event.widget.canvas
    #newFallingPiece(canvas)
    tetrisRedrawAll(canvas)

def moveFallingPiece(canvas, drow, dcol):
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(canvas):
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    tetrisRedrawAll(canvas)
    return True

def fallingPieceIsLegal(canvas):
    board = canvas.data.board
    row, col = canvas.data.fallingPieceRow, canvas.data.fallingPieceCol
    emptyColor = canvas.data.emptyColor
    for pieceRow in range(len(canvas.data.fallingPiece)):
        for pieceCol in range(len(canvas.data.fallingPiece[0])):
            if (canvas.data.fallingPiece[pieceRow][pieceCol] and (row+pieceRow
                >= canvas.data.rows or row+pieceRow < 0 or
                col+pieceCol >= canvas.data.cols or col+pieceCol < 0 or
                board[row+pieceRow][col+pieceCol] != emptyColor)):
                return False
    return True

def tetrisTimerFired(canvas):
    moveFailed = not moveFallingPiece(canvas, +1, 0)
    if moveFailed: # the piece has reached the bottom
        placeFallingPiece(canvas)
        newFallingPiece(canvas)
        if not fallingPieceIsLegal(canvas):
            canvas.data.isGameOver = True
    tetrisRedrawAll(canvas)
    if not canvas.data.isGameOver:
        delay = 500 # milliseconds
        canvas.after(delay, lambda: tetrisTimerFired(canvas)) # pause, then call snakeTimerFired again

def tetrisRedrawAll(canvas):
    canvas.delete(ALL)
    tetrisDrawGame(canvas)
    tetrisDrawScore(canvas)

def tetrisDrawScore(canvas):
    scoreText = "Score: %d" % canvas.data.score
    canvas.create_text(canvas.data.canvasWidth - canvas.data.margin,
                       canvas.data.margin,
                       text=scoreText, anchor="ne", fill="white")

def tetrisDrawGame(canvas):
    canvas.create_rectangle(0, 0, canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="orange", width=0)
    tetrisDrawBoard(canvas)
    drawFallingPiece(canvas)

def tetrisDrawBoard(canvas):
    rows = canvas.data.rows
    cols = canvas.data.cols
    board = canvas.data.board
    for row in range(rows):
        for col in range(cols):
            tetrisDrawCell(canvas, row, col, board[row][col])
    if canvas.data.isGameOver:
        canvas.create_text(canvas.data.canvasWidth/2,
                           canvas.data.canvasHeight/2, fill="white",
                           text="Game Over", font="Helvetica 30")

def tetrisDrawCell(canvas, row, col, color):
    board = canvas.data.board
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    borderWidth = canvas.data.cellBorderWidth = 1.5
    canvas.create_rectangle(col*cellSize+margin, row*cellSize+margin,
                     (col+1)*cellSize+margin, (row+1)*cellSize+margin,
                     fill="black")
    canvas.create_rectangle(col*cellSize+margin+borderWidth,
                            row*cellSize+margin+borderWidth,
                            (col+1)*cellSize+margin-borderWidth,
                            (row+1)*cellSize+margin-borderWidth,
                             fill=color)

def newFallingPiece(canvas):
    pieceIndex = randint(0,6)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[pieceIndex]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[pieceIndex]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = (canvas.data.cols -
                              len(canvas.data.fallingPiece[0]))/2

def drawFallingPiece(canvas):
    row, col = canvas.data.fallingPieceRow, canvas.data.fallingPieceCol
    for pieceRow in range(len(canvas.data.fallingPiece)):
        for pieceCol in range(len(canvas.data.fallingPiece[0])):
            if canvas.data.fallingPiece[pieceRow][pieceCol]:
                tetrisDrawCell(canvas, row+pieceRow, col+pieceCol,
                               canvas.data.fallingPieceColor)

def fallingPieceCenter(canvas):
    row = canvas.data.fallingPieceRow
    col = canvas.data.fallingPieceCol
    row += len(canvas.data.fallingPiece)/2
    col += len(canvas.data.fallingPiece[0])/2
    return (row, col)

def rotateFallingPiece(canvas):
    originalRow = canvas.data.fallingPieceRow
    originalCol = canvas.data.fallingPieceCol
    originalPiece = canvas.data.fallingPiece
    (originalCenterRow, originalCenterCol) = fallingPieceCenter(canvas)
    canvas.data.fallingPiece = [[originalPiece[row][-col-1] for row in
        range(len(originalPiece))] for col in range(len(originalPiece[0]))]
    (centerRow, centerCol) = fallingPieceCenter(canvas)
    canvas.data.fallingPieceRow -= centerRow - originalCenterRow
    canvas.data.fallingPieceCol -= centerCol - originalCenterCol
    if not fallingPieceIsLegal(canvas):
        canvas.data.fallingPieceRow = originalRow
        canvas.data.fallingPieceCol = originalCol
        canvas.data.fallingPiece = originalPiece
    tetrisRedrawAll(canvas)
    
def placeFallingPiece(canvas):
    color = canvas.data.fallingPieceColor
    row, col = canvas.data.fallingPieceRow, canvas.data.fallingPieceCol
    for pieceRow in range(len(canvas.data.fallingPiece)):
        for pieceCol in range(len(canvas.data.fallingPiece[0])):
            if canvas.data.fallingPiece[pieceRow][pieceCol]:
                canvas.data.board[row+pieceRow][col+pieceCol] = color
    removeFullRows(canvas)

def removeFullRows(canvas):
    board = canvas.data.board
    newRow = len(board)-1
    fullRows = 0
    for oldRow in range(-1, -len(board)-1, -1):
        if canvas.data.emptyColor in board[oldRow]:
            board[newRow] = copy(board[oldRow])
            #print oldRow
            newRow -= 1
        else:
            fullRows += 1
    for fullRow in range(fullRows):
        board[fullRow] = [canvas.data.emptyColor for col in
                          range(canvas.data.cols)]
    canvas.data.score += fullRows**2
    tetrisRedrawAll(canvas)

def tetrisInitPieces(canvas):
    iPiece = [ [ True,  True,  True,  True] ]

    jPiece = [ [ True, False, False],
               [ True, True,  True] ]

    lPiece = [ [ False, False, True],
               [ True,  True,  True] ]

    oPiece = [ [ True, True],
               [ True, True] ]

    sPiece = [ [ False, True, True],
               [ True,  True, False ] ]

    tPiece = [ [ False, True, False],
               [ True,  True, True] ]

    zPiece = [ [ True,  True, False],
               [ False, True, True] ]

    canvas.data.tetrisPieces = [ iPiece, jPiece, lPiece,
                                 oPiece, sPiece, tPiece, zPiece ]
    canvas.data.tetrisPieceColors = [ "red", "yellow", "magenta",
                                      "pink", "cyan", "green", "orange" ]

def tetrisInit(canvas):
    canvas.data.score = 0
    canvas.data.isGameOver = False
    emptyColor = canvas.data.emptyColor = "blue"
    canvas.data.board = [[emptyColor for i in range(canvas.data.cols)]
                         for j in range(canvas.data.rows)]
    tetrisInitPieces(canvas)
    newFallingPiece(canvas)
    

def tetrisRun(rows, cols):
    # create the root and the canvas
    root = Tk()
    margin = 20
    cellSize = 20
    width = cols*cellSize+margin*2
    height = rows*cellSize+margin*2
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = width
    canvas.data.canvasHeight = height
    tetrisInit(canvas)
    # set up events
    root.bind("<Button-1>", lambda event: tetrisMousePressed(event,canvas))
    root.bind("<Key>", lambda event: tetrisKeyPressed(event, canvas))
    tetrisTimerFired(canvas)
    # and launch the app
    root.mainloop() 

tetrisRun(15, 10)
