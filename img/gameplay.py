import pygame
import sys


class Gameplay:

    def __init__(self):
        pygame.init()
        self.moveLog = []
        self.width, self.height = 480, 480
        self.size = self.width, self.height
        self.field_side = self.height // 8
        self.screen = pygame.display.set_mode(self.size)
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
        self.screen.fill((0, 0, 0))
        self.draw_chessboard()
        self.draw_pieces()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                    click_pos = pygame.mouse.get_pos()
                    old_pos = (click_pos[1]//self.field_side, click_pos[0]//self.field_side)
                    print("FROM:", old_pos)
                    if old_pos in self.pieces.keys():
                        pygame.draw.rect(self.screen, (255, 255, 0),
                         (old_pos[1] * self.field_side, old_pos[0] * self.field_side, self.field_side, self.field_side))
                        self.draw_pieces()
                        to_move = True
                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = (click_pos[1]//self.field_side, click_pos[0]//self.field_side)
                    print("TO:", new_pos)
                    self.move(old_pos, new_pos)
                    to_move = False
                    self.draw_chessboard()
                    self.draw_pieces()
            pygame.display.flip()

    def draw_chessboard(self):
        colors = [(215,199,151), (164, 124, 72)]
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.screen, colors[(col + row) % 2],
                                 (col * self.field_side, row * self.field_side, self.field_side, self.field_side))

    def draw_pieces(self):
        for pos, img_name in self.pieces.items():
            image = pygame.image.load(img_name)
            # image = pygame.transform.scale(image, (self.field_side, self.field_side))
            self.screen.blit(image, (pos[1] * self.field_side, pos[0] * self.field_side))

    def move(self, oldpos, newpos):
        if oldpos in self.pieces.keys():
            fig_val = self.pieces[oldpos]
            self.pieces.pop(oldpos)
            self.pieces[newpos] = fig_val
            self.moveLog.append((oldpos,newpos))
            print(self.moveLog)
