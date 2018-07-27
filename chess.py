import pygame, sys
from pygame.locals import *

# set constants
screenWidth = 533
screenHeight = 480

# Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((screenWidth,screenHeight), 0, 32)
pygame.display.set_caption("Chess by Eric Thomas")

# Create constants
GRAY = (160, 160, 160)
BLACK = (0,0,0)
BROWN = (135, 64, 8)
RED = (255, 0, 0)
FPS = 30
fpsClock = pygame.time.Clock()
SQUARESIZE = 50	
LEFTOFFSET = 60
TOPOFFSET = 10
BORDERWIDTH = 5

# Given a row and column of the state matrix it returns a touple of the coordinates for the top left of the rectangle on the board
def map_state_to_coord(row, column):
	xCoord = LEFTOFFSET + (column-2) * SQUARESIZE
	yCoord = TOPOFFSET + (row - 2) * SQUARESIZE
	return (xCoord, yCoord)

# Given the coordinates of the mouse it returns a touple of the row and column of the state matrix
# If the coordinates are off the board it returns (-1, -1)
def map_coord_to_state(xCoord, yCoord):
	leftOfBoard = LEFTOFFSET - BORDERWIDTH + 2
	topOfBoard = TOPOFFSET - BORDERWIDTH + 2
	# Check if the coordinates are on the board
	if on_board(xCoord, yCoord):
		row = (yCoord - topOfBoard)//SQUARESIZE + 2
		column = (xCoord - leftOfBoard)//SQUARESIZE + 2
	else:
		row = -1
		column = -1	
	return (row, column)

# Checks whether coordinates are on the board
def on_board(xCoord, yCoord):
	borderTop = TOPOFFSET
	borderLeft = LEFTOFFSET
	borderRight = borderLeft + 8*SQUARESIZE - BORDERWIDTH
	borderBottom = borderTop + 8*SQUARESIZE - BORDERWIDTH
	return xCoord > borderLeft and xCoord < borderRight and yCoord > borderTop and yCoord < borderBottom

# Board Class
""" Board state will be a 12x12 array of Piece objects. Value of pieces are below
99 -> Out of Bounds
0 -> Empty
Positive -> White
Negative -> Black
1 -> Pawn
2 -> Bishop
3 -> Knight
4 -> Rook
5 -> Queen
6 -> King
"""
class Board:
	borderTop = TOPOFFSET - BORDERWIDTH + 2
	borderLeft = LEFTOFFSET - BORDERWIDTH + 2
	borderSize = BORDERWIDTH*2 + 8*SQUARESIZE - 4

	# Create Board in new game state
	def __init__(self):
		self.whiteMove = True
		self.whiteKingSideCastle = True
		self.whiteQueenSideCastle = True
		self.blackKingSideCastle = True
		self.blackQueenSideCastle = True

		size = 12
		self.state = list([Piece("out of bounds") for i in range(size)] for j in range(size))

		for row in range(size):
			for column in range(size):
				# Set empty spaces
				if 4 <= row < 8 and 2 <= column < 10:
					self.state[row][column] = Piece()
				# Set white pawns
				elif row == 8 and 2 <= column < 10:
					self.state[row][column] = Piece(piece="pawn", color="white")
				# Set black pawns
				elif row == 3 and 2 <= column < 10:
					self.state[row][column] = Piece(piece="pawn", color="black")
				# Set white bishops
				elif row == 9 and (column == 4 or column == 7):
					self.state[row][column] = Piece(piece="bishop", color="white")
				# Set black bishops
				elif row == 2 and (column == 4 or column == 7):
					self.state[row][column] = Piece(piece="bishop", color="black")
				# Set white knights
				elif row == 9 and (column == 3 or column == 8):
					self.state[row][column] = Piece(piece="knight", color="white")
				# Set black knights
				elif row == 2 and (column == 3 or column == 8):
					self.state[row][column] = Piece(piece="knight", color="black")
				# Set white rooks
				elif row == 9 and (column == 2 or column == 9):
					self.state[row][column] = Piece(piece="rook", color="white")
				# Set black rooks
				elif row == 2 and (column == 2 or column == 9):
					self.state[row][column] = Piece(piece="rook", color="black")
				# Set white quuen
				elif row == 9 and column == 5:
					self.state[row][column] = Piece(piece="queen", color="white")
				# Set black quuen
				elif row == 2 and column == 5:
					self.state[row][column] = Piece(piece="queen", color="black")
				# Set white king
				elif row == 9 and column == 6:
					self.state[row][column] = Piece(piece="king", color="white")
				# Set black king
				elif row == 2 and column == 6:
					self.state[row][column] = Piece(piece="king", color="black")		

	# Draw board squares and coordinate system (a-h and 1-8)
	def draw_board(self, legalMoves = []):
		# Create squares
		for row in range(1,9):
			for column in range(1,9):
				rectLeft = LEFTOFFSET + (column - 1) * SQUARESIZE
				rectTop = TOPOFFSET + (row - 1) * SQUARESIZE			

				# create white squares
				if row % 2 == 1 and column % 2 == 1 or (row % 2 == 0 and column % 2 == 0):
					wSquare = pygame.Rect(rectLeft, rectTop, SQUARESIZE, SQUARESIZE)
					pygame.draw.rect(DISPLAYSURF, GRAY, wSquare)
					
				# create black squares
				elif row % 2 == 0 and column % 2 == 1 or (row % 2 == 1 and column % 2 == 0):
					bSquare = pygame.Rect(rectLeft, rectTop, SQUARESIZE, SQUARESIZE)
					pygame.draw.rect(DISPLAYSURF, BLACK, bSquare)

		# Create legal moves squares red
		for space in legalMoves:
			rSquare = pygame.Rect(space[0], space[1], SQUARESIZE, SQUARESIZE)
			pygame.draw.rect(DISPLAYSURF, RED, rSquare)
		# Create border
		border = pygame.Rect(self.borderLeft, self.borderTop, self.borderSize, self.borderSize)
		pygame.draw.rect(DISPLAYSURF, BLACK, border, BORDERWIDTH)

		
	# Draw pieces on their squares
	def draw_pieces(state):
		for row in range(len(state)):
			for column in range((len(state[row]))):
				if state[row][column].value == 1:
					DISPLAYSURF.blit(wPawnImg, map_state_to_coord(row,column))
				elif state[row][column].value == -1:
					DISPLAYSURF.blit(bPawnImg, map_state_to_coord(row,column))
				elif state[row][column].value == 2:
					DISPLAYSURF.blit(wBishopImg, map_state_to_coord(row,column))
				elif state[row][column].value == -2:
					DISPLAYSURF.blit(bBishopImg, map_state_to_coord(row,column))
				elif state[row][column].value == 3:
					DISPLAYSURF.blit(wKnightImg, map_state_to_coord(row,column))				
				elif state[row][column].value == -3:
					DISPLAYSURF.blit(bKnightImg, map_state_to_coord(row,column))
				elif state[row][column].value == 4:
					DISPLAYSURF.blit(wRookImg, map_state_to_coord(row,column))
				elif state[row][column].value == -4:
					DISPLAYSURF.blit(bRookImg, map_state_to_coord(row,column))
				elif state[row][column].value == 5:
					DISPLAYSURF.blit(wQueenImg, map_state_to_coord(row,column))
				elif state[row][column].value == -5:
					DISPLAYSURF.blit(bQueenImg, map_state_to_coord(row,column))
				elif state[row][column].value == 6:
					DISPLAYSURF.blit(wKnightImg, map_state_to_coord(row,column))
				elif state[row][column].value == -6:
					DISPLAYSURF.blit(bKnightImg, map_state_to_coord(row,column))
# Piece Class
"""
If piece name is not included then an empty space is returned

Each non empty non out of bounds piece will have a value that corresponds to the boards specification

Each non empty non out of bounds piece will have a boolean that says if it has moved or not

Pawns will have a boolean determining if an en pessant is available

Each non empty non out of bounds piece will have a coordinate variable and picture file to represent piece

Each non empty non out of bounds piece will have a list of squares that it is able to move to

Each non empty non out of bounds piece will have a boolean saying if its captured or not
"""
class Piece:
	# Piece image variables
	"""
	wPawnImg = pygame.image.load("white pawn.png")
	bPawnImg = pygame.image.load("black pawn.png")
	wBishopImg = pygame.image.load("white bishop.png")
	bBishopImg = pygame.image.load("black bishop.png")
	wKnightImg = pygame.image.load("white knight.png")
	bKnightImg = pygame.image.load("black knight.png")
	wRookImg = pygame.image.load("white rook.png")
	bRookImg = pygame.image.load("black rook.png")
	wQueenImg = pygame.image.load("white queen.png")
	bQueenImg = pygame.image.load("black queen.png")
	wKingImg = pygame.image.load("white king.png")
	bKingImg = pygame.image.load("black king.png")
	"""

	def __init__(self, piece="empty", color="white"):
		if piece == "empty":
			self.value = 0
		elif piece == "out of bounds":
			self.value = 99
		else:
			self.moved = False
			self.coords = ()
			self.legalMoves = []
			self.captured = False
			if piece == "pawn":
				self.enPessant = False
				if color == "white":
					self.value = 1
				else:
					self.value = -1
			elif piece == "bishop":
				if color == "white":
					self.value = 2
				else:
					self.value = -2
			elif piece == "knight":
				if color == "white":
					self.value = 3
				else:
					self.value = -3
			elif piece == "rook":
				if color =="white":
					self.value = 4
				else:
					self.value = -4
			elif piece == "queen":
				if color == "white":
					self.value = 5
				else:
					self.value = -5
			elif piece == "king":
				if color == "white":
					self.value = 6
				else:
					self.value = -6

board = Board()

# Game loop
while True:
	DISPLAYSURF.fill(BROWN)
	board.draw_board()
	#board.draw_pieces(board.state)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
	fpsClock.tick(FPS)