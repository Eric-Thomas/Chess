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
FPS = 30
fpsClock = pygame.time.Clock()

# Given a row and column of the state matrix it returns a touple of the coordinates for the correct rectangle on the display
def map_state_to_coord(row, column):
	squareSize = 50	
	leftOffset = 60
	topOffset = 10
	xCoord = leftOffset + (column-2) * squareSize
	yCoord = topOffset + (row - 2) * squareSize
	return (xCoord, yCoord)

# Given the coordinates of the mouse it returns the row and column of the state matrix
def map_coord_to_state(xCoord, yCoord):


# Board Class
""" Board state will be a 12x12 array 
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
	# Board drawing variables
	squareSize = 50
	leftOffset = 60
	topOffset = 10
	borderWidth = 5
	borderTop = topOffset - borderWidth + 2
	borderLeft = leftOffset - borderWidth + 2
	borderSize = borderWidth*2 + 8*squareSize - 4
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
	# Create Board in new game state
	def __init__(self):
		self.whiteMove = True
		self.whiteKingSideCastle = True
		self.whiteQueenSideCastle = True
		self.blackKingSideCastle = True
		self.blackQueenSideCastle = True

		size = 12
		self.state = list([99 for i in range(size)] for j in range(size))

		for row in range(size):
			for column in range(size):
				# Set empty spaces
				if 4 <= row < 8 and 2 <= column < 10:
					self.state[row][column] = 0
				# Set white pawns
				elif row == 8 and 2 <= column < 10:
					self.state[row][column] = 1
				# Set black pawns
				elif row == 3 and 2 <= column < 10:
					self.state[row][column] = -1
				# Set white bishops
				elif row == 9 and (column == 4 or column == 7):
					self.state[row][column] = 2
				# Set black bishops
				elif row == 2 and (column == 4 or column == 7):
					self.state[row][column] = -2
				# Set white knights
				elif row == 9 and (column == 3 or column == 8):
					self.state[row][column] = 3
				# Set black knights
				elif row == 2 and (column == 3 or column == 8):
					self.state[row][column] = -3
				# Set white rooks
				elif row == 9 and (column == 2 or column == 9):
					self.state[row][column] = 4
				# Set black rooks
				elif row == 2 and (column == 2 or column == 9):
					self.state[row][column] = -4
				# Set white quuen
				elif row == 9 and column == 5:
					self.state[row][column] = 5
				# Set black quuen
				elif row == 2 and column == 5:
					self.state[row][column] = -5
				# Set white king
				elif row == 9 and column == 6:
					self.state[row][column] = 6
				# Set black king
				elif row == 2 and column == 6:
					self.state[row][column] = -6		

	# Draw board squares and coordinate system (a-h and 1-8)
	def draw_board(self):
		# Create squares
		for row in range(1,9):
			for column in range(1,9):
				rectLeft = self.leftOffset + (column - 1) * self.squareSize
				rectTop = self.topOffset + (row - 1) * self.squareSize			

				# create white squares
				if row % 2 == 1 and column % 2 == 1 or (row % 2 == 0 and column % 2 == 0):
					wSquare = pygame.Rect(rectLeft, rectTop, self.squareSize, self.squareSize)
					pygame.draw.rect(DISPLAYSURF, GRAY, wSquare)
					
				# create black squares
				elif row % 2 == 0 and column % 2 == 1 or (row % 2 == 1 and column % 2 == 0):
					bSquare = pygame.Rect(rectLeft, rectTop, self.squareSize, self.squareSize)
					pygame.draw.rect(DISPLAYSURF, BLACK, bSquare)

		# Create border
		border = pygame.Rect(self.borderLeft, self.borderTop, self.borderSize, self.borderSize)
		pygame.draw.rect(DISPLAYSURF, BLACK, border, self.borderWidth)

		
	# Draw pieces on their squares
	def draw_pieces(state):
		for row in range(len(state)):
			for column in range((len(state[row]))):
				if state[row][column] == 1:
					DISPLAYSURF.blit(wPawnImg, map_state_to_coord(row,column))
				elif state[row][column] == -1:
					DISPLAYSURF.blit(bPawnImg, map_state_to_coord(row,column))
				elif state[row][column] == 2:
					DISPLAYSURF.blit(wBishopImg, map_state_to_coord(row,column))
				elif state[row][column] == -2:
					DISPLAYSURF.blit(bBishopImg, map_state_to_coord(row,column))
				elif state[row][column] == 3:
					DISPLAYSURF.blit(wKnightImg, map_state_to_coord(row,column))				
				elif state[row][column] == -3:
					DISPLAYSURF.blit(bKnightImg, map_state_to_coord(row,column))
				elif state[row][column] == 4:
					DISPLAYSURF.blit(wRookImg, map_state_to_coord(row,column))
				elif state[row][column] == -4:
					DISPLAYSURF.blit(bRookImg, map_state_to_coord(row,column))
				elif state[row][column] == 5:
					DISPLAYSURF.blit(wQueenImg, map_state_to_coord(row,column))
				elif state[row][column] == -5:
					DISPLAYSURF.blit(bQueenImg, map_state_to_coord(row,column))
				elif state[row][column] == 6:
					DISPLAYSURF.blit(wKnightImg, map_state_to_coord(row,column))
				elif state[row][column] == -6:
					DISPLAYSURF.blit(bKnightImg, map_state_to_coord(row,column))
# Piece Class
"""
Each piece will have a value that corresponds to the boards specification

Pawns will have a boolean determining if an en pessant is available

Each piece will have a coordinate variable and picture file to represent piece

Each pice will have a list of squares that it is able to move to
"""
class Piece:
	def __init__(self, piece, color):
		self.enPessant = False
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
		elif piece == "knigt":
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
		else:
			if color == "white":
				self.value = 6
			else:
				self.value = -6
# Create board
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