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

# Board Class
""" Board will be a 12x12 array 
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
	"""
	# Piece image variables
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
	bQueenImg = pygame.image.load("black queen.png")
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
		squareSize = 50
		leftOffset = 60
		topOffset = 10

		# Create squares
		for row in range(1,9):
			for column in range(1,9):
				# create white squares
				if row % 2 == 1 and column % 2 == 1 or (row % 2 == 0 and column % 2 == 0):
					rectLeft = leftOffset + (column-1) * squareSize
					rectTop = topOffset + (row - 1) * squareSize
					wSquare = pygame.Rect(rectLeft, rectTop, squareSize, squareSize)
					pygame.draw.rect(DISPLAYSURF, GRAY, wSquare)
					
				# create black squares
				elif row % 2 == 0 and column % 2 == 1 or (row % 2 == 1 and column % 2 == 0):
					rectLeft = leftOffset + (column - 1) * squareSize
					rectTop = topOffset + (row - 1) * squareSize
					bSquare = pygame.Rect(rectLeft, rectTop, squareSize, squareSize)
					pygame.draw.rect(DISPLAYSURF, BLACK, bSquare)

		# Create border
		borderWidth = 5
		borderTop = topOffset - borderWidth + 2
		borderLeft = leftOffset - borderWidth + 2
		borderSize = borderWidth*2 + 8*squareSize - 4
		border = pygame.Rect(borderLeft, borderTop, borderSize, borderSize)
		pygame.draw.rect(DISPLAYSURF, BLACK, border, borderWidth)

		"""
	# Draw pieces on their squares
	def draw_pieces(state):
		for row in range(len(state)):
			for column in range((len(state[row]))):
				"""




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