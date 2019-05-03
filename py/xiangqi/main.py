""" x01.xiangqi (c) 2019 by x01"""

import os, sys, pygame 
from pygame.locals import *

BaseDir = os.path.dirname(os.path.abspath(__file__))
ImagePath = BaseDir + '/res/'

BoardWidth = 520
BoardHeight = 576
BoardEdge = 8
PieceSize = 56

# piece type
King = 0
Advisor = 1
Bishop = 2
Knight = 3
Rook = 4
Cannon = 5
Pawn = 6
Selected = 7

# piece types
types = [
	20, 19, 18, 17, 16, 17, 18, 19, 20, 
	0,  0,  0,  0,  0,  0,  0,  0,  0, 
	0, 21,  0,  0,  0,  0,  0, 21,  0, 
	22,  0, 22,  0, 22,  0, 22,  0, 22,
	0,  0,  0,  0,  0,  0,  0,  0,  0, 
	0,  0,  0,  0,  0,  0,  0,  0,  0, 
	14,  0, 14,  0, 14,  0, 14,  0, 14,
	0, 13,  0,  0,  0,  0,  0, 13,  0, 
	0,  0,  0,  0,  0,  0,  0,  0,  0, 
	12, 11, 10,  9,  8,  9, 10, 11, 12
]

class Piece(object):
	def __init__(self, player, ptype, name, pos):
		self.player = player 
		self.ptype = ptype 
		self.name = name 
		self.pos = pos 

pieces = [
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
	Piece(2, Selected, 'selected.bmp', (0,0))
]

# type index
def index(pos):
	col,row = pos[0], pos[1]
	return row * 9 + col

def draw(surface, name, xy, ispiece=True):
	img = pygame.image.load(ImagePath + name).convert()
	if ispiece:
		img.set_colorkey((0,255,0))
	surface.blit(img, xy)

def draw_pieces(surface):
	for p in pieces[:-1]:
		x = p.pos[0] * PieceSize + BoardEdge
		y = p.pos[1] * PieceSize + BoardEdge
		draw(surface, p.name, (x,y))

def run():
	pygame.init()
	screen = pygame.display.set_mode((BoardWidth, BoardHeight),0,32)
	pygame.display.set_caption('x01.xiangqi')
	draw(screen, 'board.bmp', (0,0), False)
	draw_pieces(screen)
	
	prevPiece = None 
	player = 1
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
				x,y = ((x // PieceSize) * PieceSize + BoardEdge, (y//PieceSize)*PieceSize + BoardEdge)
				pos = (x//PieceSize, y//PieceSize)
				
				draw(screen,'board.bmp',(0,0),False)
				draw_pieces(screen)	
				pieces[-1].pos = pos
				draw(screen, pieces[-1].name, (x,y))

				for p in pieces[:-1]:
					if p.pos == pos:
						prevPiece = p
						break
				
				if types[index(pos)] == 0 and prevPiece != None:
					if player != prevPiece.player:
						continue
					player = 1 - player
					if prevPiece.player == 0:
						types[index(pos)] = prevPiece.ptype + 16
					elif prevPiece.player == 1:
						types[index(pos)] = prevPiece.ptype + 8
					types[index(prevPiece.pos)] = 0
					for p in pieces[:-1]:
						if p.pos == prevPiece.pos:
							p.pos = pos 
							break
					prevPiece = None 
					
					draw(screen,'board.bmp',(0,0),False)
					draw_pieces(screen)		
					draw(screen, pieces[-1].name, (x,y))

		clock.tick(40)
		pygame.display.update()
		

if __name__ == '__main__':
	run()