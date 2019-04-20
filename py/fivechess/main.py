import os
from enum import Enum
from sys import exit

import pygame
from pygame.locals import *

BaseDir = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH =  BaseDir + '/res/'

N = 19
StoneSize = 32
WIDTH = 650
HEIGHT = 732
ColSize = 33
RowSize = 34.44
H_Pad = (HEIGHT- RowSize * N) / 2 + (RowSize - StoneSize) / 2 + 1
W_Pad = (WIDTH - ColSize * N) / 2 + (ColSize - StoneSize) / 2 + 1
Pad = ColSize - StoneSize, RowSize - StoneSize

class ChessboardState(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class GameRender(object):
    def __init__(self, gobang):
        self.__gobang = gobang
        self.__currentPieceState = ChessboardState.BLACK

        pygame.init()
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('五子棋')

        self.__ui_chessboard = pygame.image.load(IMAGE_PATH + 'board.jpeg').convert()
        self.__ui_piece_black = pygame.image.load(IMAGE_PATH + 'piece_black.png').convert_alpha()
        self.__ui_piece_white = pygame.image.load(IMAGE_PATH + 'piece_white.png').convert_alpha()

    def coordinate_transform_map2pixel(self, i, j):    
        return j * (StoneSize+Pad[0]) + W_Pad, i * (StoneSize+Pad[1]) + H_Pad

    def coordinate_transform_pixel2map(self, x, y):    
        i , j = int((y-H_Pad) / (StoneSize+Pad[1])), int((x-W_Pad) / (StoneSize+Pad[0]))
        if i < 0 or i >= N or j < 0 or j >= N:
            return None, None
        else:
            return i, j

    def draw_chess(self):
        self.__screen.blit(self.__ui_chessboard, (0,0))
        for i in range(0, N):
            for j in range(0, N):
                x,y = self.coordinate_transform_map2pixel(i,j)
                state = self.__gobang.get_chessboard_state(i,j)
                if state == ChessboardState.BLACK:
                    self.__screen.blit(self.__ui_piece_black, (x,y))
                elif state == ChessboardState.WHITE:
                    self.__screen.blit(self.__ui_piece_white, (x,y))
                else: # ChessboardState.EMPTY
                    pass
                
    def draw_result(self, result):
        font = pygame.font.SysFont('ubuntu', 50)
        tips = u"Game Over : "
        if result == ChessboardState.BLACK :
            tips = tips + u"Black Win"
        elif result == ChessboardState.WHITE:
            tips = tips + u"White Win"
        else:
            tips = tips + u"None Win"
        text = font.render(tips, True, (255, 0, 0))
        self.__screen.blit(text, (WIDTH / 2 - 200, HEIGHT / 2 - 50))

    def one_step(self):
        i, j = None, None
        # 鼠标点击
        mouse_button = pygame.mouse.get_pressed()
        # 左键
        if mouse_button[0]:
            x, y = pygame.mouse.get_pos()
            i, j = self.coordinate_transform_pixel2map(x, y)

        if not i is None and not j is None:
            # 格子上已经有棋子
            if self.__gobang.get_chessboard_state(i, j) != ChessboardState.EMPTY:
                return False
            else:
                self.__gobang.set_chessboard_state(i, j, self.__currentPieceState)
                return True

        return False
            
    def change_state(self):
        if self.__currentPieceState == ChessboardState.BLACK:
            self.__currentPieceState = ChessboardState.WHITE
        else:
            self.__currentPieceState = ChessboardState.BLACK

class GoBang(object):
    def __init__(self):
        self.__chessMap = [[ChessboardState.EMPTY for j in range(N)] for i in range(N)]
        self.__currentI = -1
        self.__currentJ = -1
        self.__currentState = ChessboardState.EMPTY

    def get_chessMap(self):
        return self.__chessMap

    def get_chessboard_state(self, i, j):
        return self.__chessMap[i][j]

    def set_chessboard_state(self, i, j, state):
        self.__chessMap[i][j] = state
        self.__currentI = i
        self.__currentJ = j
        self.__currentState = state

    def get_chess_result(self):
        if self.have_five(self.__currentI, self.__currentJ, self.__currentState):
            return self.__currentState
        else:
            return ChessboardState.EMPTY

    def count_on_direction(self, i, j, xdirection, ydirection, color):
        count = 0
        for step in range(1, 5):
            if xdirection != 0 and (j + xdirection * step < 0 or j + xdirection * step >= N):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i + ydirection * step >= N):
                break
            if self.__chessMap[i + ydirection * step][j + xdirection * step] == color:
                count += 1
            else:
                break
        return count

    def have_five(self, i, j, color):
        directions = [[(-1, 0), (1, 0)], \
                      [(0, -1), (0, 1)], \
                      [(-1, 1), (1, -1)], \
                      [(-1, -1), (1, 1)]]

        for axis in directions:
            axis_count = 1
            for (xdirection, ydirection) in axis:
                axis_count += self.count_on_direction(i, j, xdirection, ydirection, color)
                if axis_count >= 5:
                    return True

        return False

if __name__ == '__main__': 
    gobang = GoBang()
    render = GameRender(gobang)
    result = ChessboardState.EMPTY
    enable_ai = False
    is_over = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_q or event.key == K_ESCAPE:
                    exit()
            elif event.type ==  MOUSEBUTTONDOWN:
                # pygame.display.set_caption(str(event)) # find pos
                if render.one_step():
                    result = gobang.get_chess_result()
                else:
                    continue
                if result != ChessboardState.EMPTY:
                    break
                if enable_ai:
                    result = gobang.get_chess_result()
                else:
                    render.change_state()

        if not is_over:
            render.draw_chess()
        
        if result != ChessboardState.EMPTY:
            render.draw_result(result)
            pygame.display.set_caption("Press 'q' or 'ESC' key exit.")
            is_over = True

        pygame.display.update()