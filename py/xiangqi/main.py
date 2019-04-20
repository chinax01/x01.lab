import os, sys, pygame 
from pygame.locals import *

BaseDir = os.path.dirname(os.path.abspath(__file__))
ImagePath = BaseDir + '/res/'

BoardWidth = 520
BoardHeight = 576
BoardEdge = 8
PieceSize = 56

King = 0
Advisor = 1
Bishop = 2
Knight = 3
Rook = 4
Cannon = 5
Pawn = 6



pieceImages = [
	# black
	(0, King, "bk.bmp", (4,0)), 
	(0, Advisor, "ba.bmp", (3,0)),(0, Advisor, "ba.bmp", (5,0)), 
	(0, Bishop, "bb.bmp", (2,0)), (0, Bishop, "bb.bmp", (6,0)),
	(0, Knight, "bn.bmp", (1,0)), (0, Knight, "bn.bmp", (7,0)),
	(0, Rook, "br.bmp", (0,0)), (0, Rook, "br.bmp", (8,0)),
	(0, Cannon, "bc.bmp", (1,2)), (0, Cannon, "bc.bmp", (7,2)), 
	(0, Pawn, "bp.bmp", (0,3)), (0, Pawn, "bp.bmp", (2,3)),
	(0, Pawn, "bp.bmp", (4,3)),(0, Pawn, "bp.bmp", (6,3)),(0, Pawn, "bp.bmp", (8,3)),
	
	# red
	(1, King, "rk.bmp", (4,9)), 
	(1, Advisor, "ra.bmp", (3,9)),(1, Advisor, "ra.bmp", (5,9)), 
	(1, Bishop, "rb.bmp", (2,9)), (1, Bishop, "rb.bmp", (6,9)),
	(1, Knight, "rn.bmp", (1,9)), (1, Knight, "rn.bmp", (7,9)),
	(1, Rook, "rr.bmp", (0,9)), (1, Rook, "rr.bmp", (8,9)),
	(0, Cannon, "rc.bmp", (1,7)), (0, Cannon, "rc.bmp", (7,7)), 
	(0, Pawn, "rp.bmp", (0,6)), (0, Pawn, "rp.bmp", (2,6)),
	(0, Pawn, "rp.bmp", (4,6)),(0, Pawn, "rp.bmp", (6,6)),(0, Pawn, "rp.bmp", (8,6))
	]

def init():
	pygame.init()
	screen = pygame.display.set_mode((BoardWidth, BoardHeight),0,32)
	pygame.display.set_caption('中国象棋')
	board = pygame.image.load(ImagePath + 'board.bmp').convert()
	screen.blit(board, (0,0))
	
	for p in pieceImages:
		piece = pygame.image.load(ImagePath + p[2]).convert()
		piece.set_colorkey((0,255,0))
		col = p[3][0]
		row = p[3][1] 
		screen.blit(piece, (col * PieceSize + BoardEdge, row * PieceSize + BoardEdge))

def run():
	init()
	xqClock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()

		pygame.display.update()
		xqClock.tick(40)

if __name__ == '__main__':
	run()