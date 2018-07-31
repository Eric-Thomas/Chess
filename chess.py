import pygame, sys
from pygame.locals import *

# set constants
screenWidth = 584
screenHeight = 575

# Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((screenWidth,screenHeight), 0, 32)
pygame.display.set_caption("Chess by Eric Thomas")

# Create constants
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (175,175,175)
DARKGREEN = (10,68,46)
RED = (255, 0, 0)
FPS = 30
fpsClock = pygame.time.Clock()
SQUARESIZE = 64	
LEFTOFFSET = 60
TOPOFFSET = 10
BOTTOMOFFSET = 35
BORDERWIDTH = 5

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
bKingImg = pygame.image.load("black king.png")

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

Board will have boolean variables for what color move it is, if any piece is currently highlighted, and if either color is in check

Board will have lists with all piece of each color
"""
class Board:
	borderTop = TOPOFFSET - BORDERWIDTH + 2
	borderLeft = LEFTOFFSET - BORDERWIDTH + 2
	borderSize = BORDERWIDTH*2 + 8*SQUARESIZE - 4

	# Create Board in new game state
	def __init__(self):
		self.whiteMove = True
		self.anyPieceIsHighlighted = False
		self.whiteCheck = False
		self.blackCheck = False
		self.whitePieces = []
		self.blackPieces = []

		size = 12
		self.state = list([Piece("out of bounds") for i in range(size)] for j in range(size))

		for row in range(size):
			for column in range(size):
				# Set empty spaces
				if 4 <= row < 8 and 2 <= column < 10:
					self.state[row][column] = Piece()
				# Set white pawns
				elif row == 8 and 2 <= column < 10:
					self.state[row][column] = Piece(piece="pawn", color="white", row=row, column=column)
				# Set black pawns
				elif row == 3 and 2 <= column < 10:
					self.state[row][column] = Piece(piece="pawn", color="black", row=row, column=column)
				# Set white bishops
				elif row == 9 and (column == 4 or column == 7):
					self.state[row][column] = Piece(piece="bishop", color="white", row=row, column=column)
				# Set black bishops
				elif row == 2 and (column == 4 or column == 7):
					self.state[row][column] = Piece(piece="bishop", color="black", row=row, column=column)
				# Set white knights
				elif row == 9 and (column == 3 or column == 8):
					self.state[row][column] = Piece(piece="knight", color="white", row=row, column=column)
				# Set black knights
				elif row == 2 and (column == 3 or column == 8):
					self.state[row][column] = Piece(piece="knight", color="black", row=row, column=column)
				# Set white rooks
				elif row == 9 and (column == 2 or column == 9):
					self.state[row][column] = Piece(piece="rook", color="white", row=row, column=column)
				# Set black rooks
				elif row == 2 and (column == 2 or column == 9):
					self.state[row][column] = Piece(piece="rook", color="black", row=row, column=column)
				# Set white quuen
				elif row == 9 and column == 5:
					self.state[row][column] = Piece(piece="queen", color="white", row=row, column=column)
				# Set black quuen
				elif row == 2 and column == 5:
					self.state[row][column] = Piece(piece="queen", color="black", row=row, column=column)
				# Set white king
				elif row == 9 and column == 6:
					self.state[row][column] = Piece(piece="king", color="white", row=row, column=column)
				# Set black king
				elif row == 2 and column == 6:
					self.state[row][column] = Piece(piece="king", color="black", row=row, column=column)	

		# Initialize piece lists
		self.set_piece_lists()			

	def set_piece_lists(self):
		for row in range(len(self.state)):
			for column in range(len(self.state[row])):
				if 0 < self.state[row][column].value < 99:
					self.whitePieces.append(self.state[row][column])
				elif self.state[row][column].value < 0:
					self.blackPieces.append(self.state[row][column])

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
					pygame.draw.rect(DISPLAYSURF, WHITE, wSquare)
					
				# create black squares
				elif row % 2 == 0 and column % 2 == 1 or (row % 2 == 1 and column % 2 == 0):
					bSquare = pygame.Rect(rectLeft, rectTop, SQUARESIZE, SQUARESIZE)
					pygame.draw.rect(DISPLAYSURF, GRAY, bSquare)

		# Create legal moves squares red
		for space in legalMoves:
			coords = map_state_to_coord(space[0], space[1])
			rSquare = pygame.Rect(coords[0] + 1, coords[1] + 1, SQUARESIZE - 2, SQUARESIZE - 2)
			pygame.draw.rect(DISPLAYSURF, RED, rSquare)

		# Create border
		border = pygame.Rect(self.borderLeft, self.borderTop, self.borderSize, self.borderSize)
		pygame.draw.rect(DISPLAYSURF, BLACK, border, BORDERWIDTH)
		
	# Draw pieces on their squares
	def draw_pieces(self):
		for row in range(len(self.state)):
			for column in range((len(self.state[row]))):
				if self.state[row][column].value == 1:
					DISPLAYSURF.blit(wPawnImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == -1:
					DISPLAYSURF.blit(bPawnImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == 2:
					DISPLAYSURF.blit(wBishopImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == -2:
					DISPLAYSURF.blit(bBishopImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == 3:
					DISPLAYSURF.blit(wKnightImg, map_state_to_coord(row,column))				
				elif self.state[row][column].value == -3:
					DISPLAYSURF.blit(bKnightImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == 4:
					DISPLAYSURF.blit(wRookImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == -4:
					DISPLAYSURF.blit(bRookImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == 5:
					DISPLAYSURF.blit(wQueenImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == -5:
					DISPLAYSURF.blit(bQueenImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == 6:
					DISPLAYSURF.blit(wKingImg, map_state_to_coord(row,column))
				elif self.state[row][column].value == -6:
					DISPLAYSURF.blit(bKingImg, map_state_to_coord(row,column))

	def move_piece(self, piece, row, column):
		# Check to see if piece was captured via en pessant
		if piece.value == -1 or piece.value == 1:
			if self.state[row][column].value == 0:
				if piece.value == 1:
					# Caputre black piece
					self.state[row+1][column] = Piece()
				else:
					self.state[row-1][column] = Piece()

		# Send piece to destination
		self.state[row][column] = piece
		# Make square where piece was previously now empty
		self.state[piece.row][piece.column] = Piece()

		# Check to see if move is a castle
		if piece.value == 6 or piece.value == -6:
			if column == self.state[piece.row][piece.column-2] or column == self.state[piece.row][piece.column+2]:
				# Move queenside rook
				if column == piece.column-2:
					self.state[piece.row][piece.column-1] = self.state[piece.row][piece.column-4]
					# Make rook space empty
					self.state[piece.row][piece.column-4] = Piece()
					# Update rook column
					self.state[piece.row][piece.column-1].column = piece.column-1
					# Update rook moved
					self.state[piece.row][piece.column-1].moved = True
				# Move kingside rook
				else:
					self.state[piece.row][piece.column+1] = self.state[piece.row][piece.column+3]
					self.state[piece.row][piece.column+3] = Piece()
					self.state[piece.row][piece.column+1].column = piece.column+1
					self.state[piece.row][piece.column+1].moved = True

		# Make all en pessants false
		for wPiece in self.whitePieces:
			if wPiece.value == 1:
				wPiece.enPessant = False
		for bPiece in self.blackPieces:
			if bPiece.value == -1:
				bPiece.enPessant = False

		# Check if en pessant is now available
		if piece.value == 1 and row == piece.row-2:
			if self.state[row][piece.column-1].value < 0 or self.state[row][piece.column+1].value < 0:
				piece.enPessant = True
		elif piece.value == -1 and row == piece.row+2:
			if 0 < self.state[row][piece.column-1].value < 99 or 0 < self.state[row][piece.column+1].value < 99:
				piece.enPessant = True

		# Update piece row, column, and moved
		piece.row = row
		piece.column = column
		piece.moved = True

	def white_in_check(self):
		# Find white king
		for row in range(len(self.state)):
			for column in range(len(self.state[row])):
				if self.state[row][column].value == 6:
					king = self.state[row][column]

		# Calculate all balck legal moves
		possibleBlackMoves = []
		for piece in board.blackPieces:
			for move in piece.return_legal_moves(board):
				possibleBlackMoves.append(move)

		return (king.row, king.column) in possibleBlackMoves


	def black_in_check(self):
		# Find white king
		for row in range(len(self.state)):
			for column in range(len(self.state[row])):
				if self.state[row][column].value == -6:
					king = self.state[row][column]

		# Calculate all possible white moves
		possibleWhiteMoves = []
		for piece in board.whitePieces:
			for move in piece.return_legal_moves(board):
				possibleWhiteMoves.append(move)

		return (king.row, king.column) in possibleWhiteMoves

# Piece Class
"""
If piece name is not included then an empty space is returned

Each non empty non out of bounds piece will have a value that corresponds to the boards specification

Each non empty non out of bounds piece will have a boolean that says if it has moved or not

Each non empty non out of bounds piece will have a row and column variable coorresponding to the state row and column

Pawns will have a boolean determining if an en pessant is available

"""
class Piece:

	def __init__(self, piece="empty", color="white", row="0", column="0"):
		if piece == "empty":
			self.value = 0
		elif piece == "out of bounds":
			self.value = 99
		else:
			self.moved = False
			self.row = row
			self.column = column
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

	def set_legal_moves(self, board):
		self.legalMoves=[]
		# Set legal moves for white pawns
		if self.value == 1:
			self.white_pawn_legal_moves(self.row, self.column, board.state)
		# Set legal moves for black pawns
		elif self.value == -1:
			self.black_pawn_legal_moves(self.row, self.column, board.state)
		# Set legal moves for all bishops
		elif self.value == 2 or self.value == -2:	
			self.bishop_legal_moves(self.row, self.column, board.state)
		# Set legal moves for all knights
		elif self.value == 3 or self.value == -3:
			self.knight_legal_moves(self.row, self.column, board.state)
		# Set legal moves for all rooks
		elif self.value == 4 or self.value == -4:
			self.rook_legal_moves(self.row, self.column, board.state)
		# Set legal moves for all queens
		elif self.value == 5 or self.value == -5:
			self.bishop_legal_moves(self.row, self.column, board.state)
			self.rook_legal_moves(self.row, self.column, board.state)
		# Set legal moves for white king
		elif self.value == 6:
			self.white_king_legal_moves(self.row, self.column, board)
		# set legal moves for black king
		elif self.value == -6:
			self.black_king_legal_moves(self.row, self.column, board)

	def return_legal_moves(self, board):
		legalMoves=[]
		# Set legal moves for white pawns
		if self.value == 1:
			legalMoves = self.white_pawn_legal_moves(self.row, self.column, board.state, rtrn = True)
		# Set legal moves for black pawns
		elif self.value == -1:
			legalMoves = self.black_pawn_legal_moves(self.row, self.column, board.state, rtrn = True)
		# Set legal moves for all bishops
		elif self.value == 2 or self.value == -2:	
			legalMoves = self.bishop_legal_moves(self.row, self.column, board.state, rtrn = True)
		# Set legal moves for all knights
		elif self.value == 3 or self.value == -3:
			legalMoves = self.knight_legal_moves(self.row, self.column, board.state, rtrn = True)
		# Set legal moves for all rooks
		elif self.value == 4 or self.value == -4:
			legalMoves = self.rook_legal_moves(self.row, self.column, board.state, rtrn = True)
		# Set legal moves for all queens
		elif self.value == 5 or self.value == -5:
			legalMoves = self.bishop_legal_moves(self.row, self.column, board.state, rtrn = True)
			tempLegalMoves = (self.rook_legal_moves(self.row, self.column, board.state, rtrn = True))
			for move in tempLegalMoves:
				legalMoves.append(move)
		return legalMoves

	def white_pawn_legal_moves(self, row, column, state, rtrn = False):
		if not rtrn:
			# Check space in front is empty
			if state[row-1][column].value == 0:
				self.legalMoves.append((row-1,column))
				# Check if 2 spaces in front are empty and piece hasn't moved
				if state[row-2][column].value == 0 and not self.moved:
					self.legalMoves.append((row-2,column))
			# Check if pawn can capture diagonally normally or via en pessant
			if state[row-1][column-1].value < 0 or (state[row][column-1].value == -1 and state[row][column-1].enPessant and state[row-1][column-1].value == 0):
				self.legalMoves.append((row-1, column-1))
			if state[row-1][column+1].value < 0 or (state[row][column+1].value == -1 and state[row][column+1].enPessant and state[row-1][column+1].value == 0):
				self.legalMoves.append((row-1, column + 1))
		# If it is a king only legal moves are to capture diagonally
		else:
			legalMoves = []
			legalMoves.append((row-1, column-1))
			legalMoves.append((row-1, column + 1))
			return legalMoves

	def black_pawn_legal_moves(self, row, column, state, rtrn = False):
		if not rtrn:
			if state[row + 1][column].value == 0:
				self.legalMoves.append((row+1, column))
				if state[row+2][column].value == 0 and not self.moved:
					self.legalMoves.append((row+2,column))
			if 0 < state[row+1][column-1].value < 99 or (state[row][column-1].value == 1 and state[row][column-1].enPessant and state[row+1][column-1].value == 0):
				self.legalMoves.append((row+1, column-1))
			if 0 < state[row+1][column+1].value < 99 or (state[row][column+1].value == 1 and state[row][column+1].enPessant and state[row+1][column+1].value == 0):
				self.legalMoves.append((row+1, column+1))
		else:
			legalMoves = []
			legalMoves.append((row+1, column-1))
			legalMoves.append((row+1, column+1))
			return legalMoves

	def bishop_legal_moves(self, row, column, state, rtrn = False):
		if rtrn:
			legalMoves = []
		# check front left diagonal empty spaces
		tempRow = row
		tempColumn = column
		while state[tempRow-1][tempColumn-1].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn-1))
			else:
				legalMoves.append((tempRow-1, tempColumn-1))
			empties = True
			tempRow -= 1
			tempColumn -= 1
		# Check to see if next space is enemy
		# set white enemies
		if self.value > 0 and state[tempRow-1][tempColumn-1].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn-1))
			else:
				legalMoves.append((tempRow-1, tempColumn-1))
		# set black enemies
		elif self.value < 0 and 0 <  state[tempRow-1][tempColumn-1].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn-1))
			else:
				legalMoves.append((tempRow-1, tempColumn-1))
		# check front right diagonal empty spaces
		tempRow = row
		tempColumn = column
		while state[tempRow-1][tempColumn+1].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn+1))
			else:
				legalMoves.append((tempRow-1, tempColumn+1))
			empties = True
			tempRow -= 1
			tempColumn += 1
		# Check to see if next space is enemy
		# Set white enemies
		if self.value > 0 and state[tempRow-1][tempColumn+1].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn+1))
			else:
				legalMoves.append((tempRow-1, tempColumn+1))
		# Set balck enemies
		elif self.value < 0 and 0 < state[tempRow-1][tempColumn+1].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn+1))
			else:
				legalMoves.append((tempRow-1, tempColumn+1))
		# check back left diagonal empty spaces
		tempRow = row
		tempColumn = column
		while state[tempRow+1][tempColumn-1].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn-1))
			else:
				legalMoves.append((tempRow+1, tempColumn-1))
			empties = True
			tempRow += 1
			tempColumn -= 1
		# Check to see if next space is enemy
		# Set white enemies
		if self.value > 0 and state[tempRow+1][tempColumn-1].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn-1))
			else:
				legalMoves.append((tempRow+1, tempColumn-1))
		# Set black enemies
		elif self.value < 0 and 0 <  state[tempRow+1][tempColumn-1].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn-1))
			else:
				legalMoves.append((tempRow+1, tempColumn-1))
		# check back right diagonal empty spaces
		tempRow = row
		tempColumn = column
		while state[tempRow+1][tempColumn+1].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn+1))
			else:
				legalMoves.append((tempRow+1, tempColumn+1))
			empties = True
			tempRow += 1
			tempColumn += 1
		# Check to see if next space is enemy
		if self.value > 0 and state[tempRow+1][tempColumn+1].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn+1))	
			else:
				legalMoves.append((tempRow+1, tempColumn+1))	
		elif self.value < 0 and 0 < state[tempRow+1][tempColumn+1].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn+1))	
			else:
				legalMoves.append((tempRow+1, tempColumn+1))

		if rtrn:
			return legalMoves

	def knight_legal_moves(self, row, column, state, rtrn = False):
		if rtrn:
			legalMoves = []
		# Set empty spaces as legal moves
		knightMoves = [(row-2, column-1), (row-2, column+1), (row-1, column+2), (row-1,column-2), (row+2, column-1), (row+2, column+1), (row+1, column-2), (row+1, column+2)] 
		for square in knightMoves:
			if state[square[0]][square[1]].value == 0:
				if not rtrn:
					self.legalMoves.append(square)
				else:
					legalMoves.append(square)
			if self.value > 0 and state[square[0]][square[1]].value < 0:
				if not rtrn:
					self.legalMoves.append(square)
				else:
					legalMoves.append(square)
			elif self.value < 0 and 0 < state[square[0]][square[1]].value < 99:
				if not rtrn:
					self.legalMoves.append(square)
				else:
					legalMoves.append(square)
		if rtrn:
			return legalMoves

	def rook_legal_moves(self, row, column, state, rtrn = False):
		if rtrn:
			legalMoves = []
		# Check front spaces
		tempRow = row
		tempColumn = column
		while state[tempRow-1][tempColumn].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn))
			else:
				legalMoves.append((tempRow-1, tempColumn))
			tempRow -= 1
		# Check for enemies
		if self.value > 0 and state[tempRow-1][tempColumn].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn))
			else:
				legalMoves.append((tempRow-1, tempColumn))
		elif self.value < 0 and 0 < state[tempRow-1][tempColumn].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow-1, tempColumn))
			else:
				legalMoves.append((tempRow-1, tempColumn))
		# Check back spaces
		tempRow = row
		while state[tempRow+1][tempColumn].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn))
			else:
				legalMoves.append((tempRow+1, tempColumn))
			tempRow += 1
		# Check for enemies
		if self.value > 0 and state[tempRow+1][tempColumn].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn))
			else:
				legalMoves.append((tempRow+1, tempColumn))
		elif self.value < 0 and 0 < state[tempRow+1][tempColumn].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow+1, tempColumn))
			else:
				legalMoves.append((tempRow+1, tempColumn))
		# Check left spaces
		tempRow = row
		while state[tempRow][tempColumn-1].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow, tempColumn-1))
			else:
				legalMoves.append((tempRow, tempColumn-1))
			tempColumn -= 1
		# Check for enemies
		if self.value > 0 and state[tempRow][tempColumn-1].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow, tempColumn-1))
			else:
				legalMoves.append((tempRow, tempColumn-1))
		elif self.value < 0 and 0 < state[tempRow][tempColumn-1].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow, tempColumn-1))
			else:
				legalMoves.append((tempRow, tempColumn-1))
		# Check right spaces
		tempColumn = column
		while state[tempRow][tempColumn+1].value == 0:
			if not rtrn:
				self.legalMoves.append((tempRow, tempColumn+1))
			else:
				legalMoves.append((tempRow, tempColumn+1))
			tempColumn += 1
		# Check for enemies
		if self.value > 0 and state[tempRow][tempColumn+1].value < 0:
			if not rtrn:
				self.legalMoves.append((tempRow, tempColumn+1))
			else:
				legalMoves.append((tempRow, tempColumn+1))
		elif self.value < 0 and 0 < state[tempRow][tempColumn+1].value < 99:
			if not rtrn:
				self.legalMoves.append((tempRow, tempColumn+1))
			else:
				legalMoves.append((tempRow, tempColumn+1))

		if rtrn:
			return legalMoves

	def white_king_legal_moves(self, row, column, board):
		kingMoves = [(row+1, column), (row-1, column), (row, column-1), (row, column+1), (row+1, column+1), (row+1, column-1), (row-1, column+1), (row-1, column-1)]

		# Calculate all balck legal moves
		possibleBlackMoves = []
		for piece in board.blackPieces:
			for move in piece.return_legal_moves(board):
				possibleBlackMoves.append(move)

		# For each of the possible king moves, make sure he isn't under attack by moving to a possible black move
		for square in kingMoves:
			if (square[0], square[1]) not in possibleBlackMoves:
				if board.state[square[0]][square[1]].value == 0 or board.state[square[0]][square[1]].value < 0:
					self.legalMoves.append(square)

		# Check for king side castle
		# Make sure neither king nor rook has moved
		if not self.moved and not board.state[self.row][self.column+3].moved:
			# Make sure no pieces in between king and rook
			if board.state[self.row][self.column+1].value == 0 and board.state[self.row][self.column+2].value == 0:
				# Make sure king isn't in check, doesn't cross over or end on a square being attacked
				if (self.row, self.column) not in possibleBlackMoves and (self.row, self.column+1) not in possibleBlackMoves and (self.row, self.column+2) not in possibleBlackMoves:
					self.legalMoves.append((self.row, self.column+2))
		# Check for queen side castle
		if not self.moved and not board.state[self.row][self.column-4].moved:
			if board.state[self.row][self.column-1].value == 0 and board.state[self.row][self.column-2].value == 0 and board.state[self.row][self.column-3].value == 0:
				if (self.row, self.column) not in possibleBlackMoves and (self.row, self.column-1) not in possibleBlackMoves and (self.row, self.column-2) not in possibleBlackMoves:
					self.legalMoves.append((self.row, self.column-2))

	def black_king_legal_moves(self, row, column, board):
		kingMoves = [(row+1, column), (row-1, column), (row, column-1), (row, column+1), (row+1, column+1), (row+1, column-1), (row-1, column+1), (row-1, column-1)]
		# Calculate all possible white moves
		possibleWhiteMoves = []
		for piece in board.whitePieces:
			for move in piece.return_legal_moves(board):
				possibleWhiteMoves.append(move)

		# For each of the possible king moves, make sure he isn't under attack by moving to a possible black move
		for square in kingMoves:
			if (square[0], square[1]) not in possibleWhiteMoves:
				if board.state[square[0]][square[1]].value == 0 or 0 < board.state[square[0]][square[1]].value < 99:
					self.legalMoves.append(square)

		# Check for king side castle
		# Make sure neither king nor rook has moved
		if not self.moved and not board.state[self.row][self.column+3].moved:
			# Make sure no pieces in between king and rook
			if board.state[self.row][self.column+1].value == 0 and board.state[self.row][self.column+2].value == 0:
				# Make sure king isn't in check, doesn't cross over or end on a square being attacked
				if (self.row, self.column) not in possibleWhiteMoves and (self.row, self.column+1) not in possibleWhiteMoves and (self.row, self.column+2) not in possibleWhiteMoves:
					self.legalMoves.append((self.row, self.column+2))
		# Check for queen side castle
		if not self.moved and not board.state[self.row][self.column-4].moved:
			if board.state[self.row][self.column-1].value == 0 and board.state[self.row][self.column-2].value == 0 and board.state[self.row][self.column-3].value == 0:
				if (self.row, self.column) not in possibleWhiteMoves and (self.row, self.column-1) not in possibleWhiteMoves and (self.row, self.column-2) not in possibleWhiteMoves:
					self.legalMoves.append((self.row, self.column-2))


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

# Draws the 1-8 and A-H grid markers
def draw_grid_markers(surface):
	# Create A-H and 1-8 markers
	fontSize = 16
	fontObj = pygame.font.Font("freesansbold.ttf", fontSize)
	letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
	numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
	for i in range(len(numbers)):
		font = pygame.font.SysFont(None, fontSize)
		textSurfaceObj = font.render(numbers[i], True, WHITE)
		surface.blit(textSurfaceObj, (LEFTOFFSET//2 - fontSize//2, TOPOFFSET + (i) * SQUARESIZE + SQUARESIZE//2))

	for i in range(len(letters)):
		font = pygame.font.SysFont(None, fontSize)
		textSurfaceObj = font.render(letters[i], True, WHITE)
		surface.blit(textSurfaceObj, (LEFTOFFSET + (i)*SQUARESIZE + SQUARESIZE//2 - fontSize//2, screenHeight - BOTTOMOFFSET))



board = Board()
legalMoves = []

# Game loop
while True:
	DISPLAYSURF.fill(DARKGREEN)
	draw_grid_markers(DISPLAYSURF)
	board.draw_board(legalMoves)
	board.draw_pieces()
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == MOUSEBUTTONDOWN:
			rowCol = map_coord_to_state(event.pos[0], event.pos[1])
			# check that click was on the board
			if rowCol[0] != -1:
				if board.anyPieceIsHighlighted:
					# If a legal move is made, move the piece, change board turn, change any highlighted piece, set legal moves to empty, and calculate piece lists, check for check and checkmate
					if (rowCol[0], rowCol[1]) in legalMoves:
						board.move_piece(piece, rowCol[0], rowCol[1])
						board.set_piece_lists()
						board.whiteMove = not board.whiteMove
						board.anyPieceIsHighlighted = False
						legalMoves = []
						if board.whiteMove:
							board.whiteCheck = board.white_in_check()
							if board.whiteCheck:
								print("White check")
						else:
							board.blackCheck = board.black_in_check()
							if board.blackCheck:
								print("Black check")
					# If a white peice is clicked, set new piece object, change board to have highlighted piece, and set legal moves
					elif board.whiteMove and 0 < board.state[rowCol[0]][rowCol[1]].value < 99:
						piece = board.state[rowCol[0]][rowCol[1]]
						board.anyPieceIsHighlighted = True						
						piece.set_legal_moves(board)
						legalMoves = piece.legalMoves
					# If a black peice is clicked, set new piece object, change board to have highlighted piece, and set legal moves
					elif not board.whiteMove and board.state[rowCol[0]][rowCol[1]].value  < 0:
						piece = board.state[rowCol[0]][rowCol[1]]
						board.anyPieceIsHighlighted = True	
						piece.set_legal_moves(board)
						legalMoves = piece.legalMoves
				else:
					# If a white peice is clicked, set new piece object, change board to have highlighted piece, and set legal moves
					if board.whiteMove and 0 < board.state[rowCol[0]][rowCol[1]].value  < 99:
						piece = board.state[rowCol[0]][rowCol[1]]
						board.anyPieceIsHighlighted = True						
						piece.set_legal_moves(board)
						legalMoves = piece.legalMoves
					# If a black peice is clicked, set new piece object, change board to have highlighted piece, and set legal moves
					elif not board.whiteMove and board.state[rowCol[0]][rowCol[1]].value  < 0:
						piece = board.state[rowCol[0]][rowCol[1]]
						board.anyPieceIsHighlighted = True	
						piece.set_legal_moves(board)
						legalMoves = piece.legalMoves					
			# If click was off the board then set legal moves to empty
			else:
				legalMoves = []
	pygame.display.update()
	fpsClock.tick(FPS)