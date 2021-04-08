import pygame
import sys
from MovesGenerator import *


class Gameplay:

    def __init__(self):
        pygame.init()
        self.moveLog = []
        self.width, self.height = 480, 480
        self.size = self.width, self.height
        self.field_side = self.height // 8
        self.board_screen = pygame.display.set_mode(self.size)
        self.active_color = "w"
        self.non_active_color = "b"
        self.move_generator = MovesGenerator(self)
        self.pieces = {
                       (0, 0): "img/bR.png", (0, 1): "img/bN.png", (0, 2): "img/bB.png", (0, 3): "img/bQ.png",
                       (0, 4): "img/bK.png", (0, 5): "img/bB.png", (0, 6): "img/bN.png", (0, 7): "img/bR.png",
                       (1, 0): "img/bP.png", (1, 1): "img/bP.png", (1, 2): "img/bP.png", (1, 3): "img/bP.png",
                       (1, 4): "img/bP.png", (1, 5): "img/bP.png", (1, 6): "img/bP.png", (1, 7): "img/bP.png",
                       (7, 0): "img/wR.png", (7, 1): "img/wN.png", (7, 2): "img/wB.png", (7, 3): "img/wQ.png",
                       (7, 4): "img/wK.png", (7, 5): "img/wB.png", (7, 6): "img/wN.png", (7, 7): "img/wR.png",
                       (6, 0): "img/wP.png", (6, 1): "img/wP.png", (6, 2): "img/wP.png", (6, 3): "img/wP.png",
                       (6, 4): "img/wP.png", (6, 5): "img/wP.png", (6, 6): "img/wP.png", (6, 7): "img/wP.png"
                       }

    def two_players_game(self):
        old_pos = None
        to_move = False
        self.board_screen.fill((0, 0, 0))
        self.draw_chessboard()
        self.draw_pieces()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                    click_pos = pygame.mouse.get_pos()
                    old_pos = ((click_pos[1])//self.field_side, click_pos[0]//self.field_side)
                    print(click_pos)
                    print("FROM:", old_pos)
                    if old_pos in self.pieces.keys() and self.pieces.get(old_pos)[4] == self.active_color:
                        pygame.draw.rect(self.board_screen, (255, 255, 0),
                         (old_pos[1] * self.field_side, old_pos[0] * self.field_side, self.field_side, self.field_side))
                        self.draw_pieces()
                        to_move = True
                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = ((click_pos[1])//self.field_side, click_pos[0]//self.field_side)
                    print(click_pos)
                    print("TO:", new_pos)
                    valid_moves = self.move_generator.generate_valid_moves()
                    if (old_pos, new_pos) in valid_moves:
                        move = Move(old_pos, new_pos, self.pieces)
                        self.pieces = move.make_move()
                        self.moveLog.append((old_pos,new_pos))
                        self.active_color, self.non_active_color = self.non_active_color, self.active_color
                    to_move = False
                    self.draw_chessboard()
                    self.draw_pieces()
  
            pygame.display.flip()

    def draw_chessboard(self):
        colors = [(215,199,151), (164, 124, 72)]
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.board_screen, colors[(col + row) % 2],
                                 (col * self.field_side, row * self.field_side, self.field_side, self.field_side))

    def draw_pieces(self):
        for pos, img_name in self.pieces.items():
            image = pygame.image.load(img_name)
            # image = pygame.transform.scale(image, (self.field_side, self.field_side))
            self.board_screen.blit(image, (pos[1] * self.field_side, pos[0] * self.field_side))

    # def get_pieces(self):
    #    return self.pieces

    # def move(self, oldpos, newpos):
    #     if oldpos in self.pieces.keys():
    #         fig_val = self.pieces[oldpos]
    #         self.pieces.pop(oldpos)
    #         self.pieces[newpos] = fig_val
    #         self.moveLog.append((oldpos,newpos))
    #         print(self.moveLog)

    

    # def undo_move(self):
    #     if len(self.moveLog) != 0:
    #         move = self.moveLog.pop()


class Move:

    def __init__(self, old_pos, new_pos, previous_board):
        self.previous_board = previous_board
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.Gameplay = Gameplay

    def make_move(self):
        if self.old_pos in self.previous_board.keys():
            print("RUCH")
            # self.previous_board = Gameplay.get_pieces()
            new_board = self.previous_board
            # print(self.previous_board)
            fig_val = self.previous_board[self.old_pos]
            new_board.pop(self.old_pos)
            new_board[self.new_pos] = fig_val
            # Gameplay.moveLog.append((old_pos,new_pos))
            # print(Gameplay.moveLog)
            return new_board