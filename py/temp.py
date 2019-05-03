import os, sys, pygame 
from pygame.locals import *

BaseDir = os.path.dirname(os.path.abspath(__file__))
ImagePath = BaseDir + '/res/'

BoardWidth = 520
BoardHeight = 576
BoardEdge = 8
PieceSize = 56

# board range
StartRow = 3
EndRow = 12
StartCol = 3
EndCol = 11

# piece type
King = 0
Advisor = 1
Bishop = 2
Knight = 3
Rook = 4
Cannon = 5
Pawn = 6
Selected = 7

squares = [
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0, 20, 19, 18, 17, 16, 17, 18, 19, 20,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0, 21,  0,  0,  0,  0,  0, 21,  0,  0,  0,  0,  0,
	0,  0,  0, 22,  0, 22,  0, 22,  0, 22,  0, 22,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0, 14,  0, 14,  0, 14,  0, 14,  0, 14,  0,  0,  0,  0,
	0,  0,  0,  0, 13,  0,  0,  0,  0,  0, 13,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0, 12, 11, 10,  9,  8,  9, 10, 11, 12,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
]

class Piece(object):
	def __init__(self, player, type, name, pos):
		self.player = player 
		self.type = type 
		self.name = name 
		self.pos = pos 

pieceImages = [
	# black
	Piece(0, King, "bk.bmp", (4,0)), 
	Piece(0, Advisor, "ba.bmp", (3,0)),Piece(0, Advisor, "ba.bmp", (5,0)), 
	Piece(0, Bishop, "bb.bmp", (2,0)), Piece(0, Bishop, "bb.bmp", (6,0)),
	Piece(0, Knight, "bn.bmp", (1,0)), Piece(0, Knight, "bn.bmp", (7,0)),
	Piece(0, Rook, "br.bmp", (0,0)), Piece(0, Rook, "br.bmp", (8,0)),
	Piece(0, Cannon, "bc.bmp", (1,2)), Piece(0, Cannon, "bc.bmp", (7,2)), 
	Piece(0, Pawn, "bp.bmp", (0,3)), Piece(0, Pawn, "bp.bmp", (2,3)),
	Piece(0, Pawn, "bp.bmp", (4,3)),Piece(0, Pawn, "bp.bmp", (6,3)),Piece(0, Pawn, "bp.bmp", (8,3)),
	
	# red
	Piece(1, King, "rk.bmp", (4,9)), 
	Piece(1, Advisor, "ra.bmp", (3,9)),Piece(1, Advisor, "ra.bmp", (5,9)), 
	Piece(1, Bishop, "rb.bmp", (2,9)), Piece(1, Bishop, "rb.bmp", (6,9)),
	Piece(1, Knight, "rn.bmp", (1,9)), Piece(1, Knight, "rn.bmp", (7,9)),
	Piece(1, Rook, "rr.bmp", (0,9)), Piece(1, Rook, "rr.bmp", (8,9)),
	Piece(1, Cannon, "rc.bmp", (1,7)), Piece(1, Cannon, "rc.bmp", (7,7)), 
	Piece(1, Pawn, "rp.bmp", (0,6)), Piece(1, Pawn, "rp.bmp", (2,6)),
	Piece(1, Pawn, "rp.bmp", (4,6)),Piece(1, Pawn, "rp.bmp", (6,6)),Piece(1, Pawn, "rp.bmp", (8,6)),

	# selected
	Piece(2, Selected, 'selected.bmp', (-1,-1))
]

def row(i):
	return i >> 4
def col(i):
	return i & 15
def index(row,col):
	return (row << 4) + col 
def me_flag(i):
	return 8 + (i<<3)
def other_flag(i):
	return 16 - (i<<3)
def source(mv):
	return mv & 255
def destination(mv):
	return mv >> 8
def move(src, dest):
	return src + dest*256

class Positions(object):
	def __init__(self, squares):
		self.squares = squares 
		self.player = 0
	def change_side(self):
		self.player = 1 - self.player
	def add_piece(self, i, piece):
		self.squares[i] = piece 
	def del_piece(self, i):
		self.squares[i] = 0
	def move_piece(self, mv):
		src = source(mv)
		dest = destination(mv)
		self.del_piece(dest)
		piece = self.squares[src]
		self.del_piece(src)
		self.add_piece(dest, piece)
	def make_move(self, mv):
		self.move_piece(mv)
		self.change_side()

def run():
	pygame.init()
	screen = pygame.display.set_mode((BoardWidth, BoardHeight),0,32)
	pygame.display.set_caption('x01.xiangqi')
	board = pygame.image.load(ImagePath + 'board.bmp').convert()
	screen.blit(board, (0,0))
	
	for p in pieceImages[:-1]:
		piece = pygame.image.load(ImagePath + p.name).convert()
		piece.set_colorkey((0,255,0))
		col = p.pos[0]
		row = p.pos[1]
		screen.blit(piece, (col * PieceSize + BoardEdge, row * PieceSize + BoardEdge))

	positions = Positions(squares)
	
	clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
					x,y = pygame.mouse.get_pos()
					c = (x + PieceSize-1) // PieceSize
					r = (y + PieceSize-1) // PieceSize
					print(c,y)
		

		clock.tick(40)
		pygame.display.update()
		

if __name__ == '__main__':
	run()