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
        self.white_short_castling = True
        self.white_long_castling = True
        self.black_short_castling = True
        self.black_long_castling = True
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
        valid_moves = self.move_generator.generate_valid_moves()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                    click_pos = pygame.mouse.get_pos()
                    old_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                    print(click_pos)
                    print("FROM:", old_pos)
                    if old_pos in self.pieces.keys() and self.pieces.get(old_pos)[4] == self.active_color:
                        pygame.draw.rect(self.board_screen, (255, 255, 0),
                                         (old_pos[1] * self.field_side, old_pos[0] * self.field_side, self.field_side,
                                          self.field_side))
                        self.draw_pieces()
                        to_move = True
                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                    print(click_pos)
                    print("TO:", new_pos)
                    if (old_pos, new_pos) in valid_moves and self.check_move_correctness(old_pos, new_pos):
                        fig = self.pieces[old_pos][5]
                        move_diff = (new_pos[0]-old_pos[0], new_pos[1]-old_pos[1])
                        if fig == "K" and move_diff == (0, 2):
                            if not self.check_castling_availability("short"):
                                break
                        if fig == "K" and move_diff == (0, -2):
                            if not self.check_castling_availability("long"):
                                break
                        move = Move(old_pos, new_pos, self.pieces)
                        self.pieces = move.make_move()
                        self.update_castling_info(old_pos)
                        self.moveLog.append((old_pos, new_pos))
                        self.active_color, self.non_active_color = self.non_active_color, self.active_color
                    to_move = False
                    valid_moves = self.move_generator.generate_valid_moves()
                    if not self.find_any_possible_move(valid_moves):
                        print("NO MOVES FOR COLOR", self.active_color)
                        if self.find_any_attacker():
                            print("CHECKMATE")
                        else:
                            print("STALEMATE")
                    self.draw_chessboard()
                    self.draw_pieces()
            pygame.display.flip()

    def draw_chessboard(self):
        colors = [(215, 199, 151), (164, 124, 72)]
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.board_screen, colors[(col + row) % 2],
                                 (col * self.field_side, row * self.field_side, self.field_side, self.field_side))

    def draw_pieces(self):
        for pos, img_name in self.pieces.items():
            image = pygame.image.load(img_name)
            # image = pygame.transform.scale(image, (self.field_side, self.field_side))
            self.board_screen.blit(image, (pos[1] * self.field_side, pos[0] * self.field_side))

    def find_any_attacker(self):
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        attacker = False
        king_pos = None
        moves = self.move_generator.generate_valid_moves()
        for pos, img in self.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "K" or color == self.active_color:
                continue
            king_pos = pos
            break
        for start_pos, possible_pos in moves:
            if possible_pos == king_pos:
                attacker = True
                break
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        return attacker

    def find_any_possible_move(self, valid_moves):
        for start_pos, possible_pos in valid_moves:
            if self.check_move_correctness(start_pos, possible_pos):
                return True
        return False

    def check_move_correctness(self, start_pos, possible_pos):  # sprawdza czy PO RUCHU BEDZIE OK
        cp_init_pos = {}    # dla pewnosci dzialam na kopii bo nie pamietam jak sie zachowuje przypisanie slownika
        for pos, img in self.pieces.items():
            cp_init_pos[pos] = img
        king_safe = True
        move = Move(start_pos, possible_pos, self.pieces)
        self.pieces = move.make_move()
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        valid_moves = self.move_generator.generate_valid_moves()
        end_positions = [move[1] for move in valid_moves]
        for pos, img in self.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "K" or color != self.non_active_color:
                continue
            if pos in end_positions:
                king_safe = False
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        move_back = Move(possible_pos, start_pos, self.pieces)
        self.pieces = move_back.make_move()
        self.pieces = cp_init_pos
        return king_safe

    def check_castling_availability(self, length):
        if self.find_any_attacker():
            return False
        if length == "short" and self.active_color == "w":
            if (7, 5) in self.pieces.keys() or (7, 6) in self.pieces.keys():
                return False
        if length == "long" and self.active_color == "w":
            if (7, 1) in self.pieces.keys() or (7, 2) in self.pieces.keys() or (7, 3) in self.pieces.keys():
                return False
        if length == "short" and self.active_color == "b":
            if (0, 5) in self.pieces.keys() or (0, 6) in self.pieces.keys():
                return False
        if length == "long" and self.active_color == "b":
            if (0, 1) in self.pieces.keys() or (0, 2) in self.pieces.keys() or (0, 3) in self.pieces.keys():
                return False
        return True

    def update_castling_info(self, old_pos):
        if old_pos == (7, 4):
            self.white_long_castling = False
            self.white_short_castling = False
        if old_pos == (0, 4):
            self.black_long_castling = False
            self.black_short_castling = False
        if old_pos == (7, 0):
            self.white_long_castling = False
        if old_pos == (7, 7):
            self.white_short_castling = False
        if old_pos == (0, 0):
            self.black_long_castling = False
        if old_pos == (0, 7):
            self.black_short_castling = False

    def get_last_move(self):  # zwraca ostatni zapisany ruch w movelogu i figure ktora go wykonala
        if len(self.moveLog) != 0 and self.moveLog[-1][1] in self.pieces.keys():
            return self.moveLog[-1], self.pieces[self.moveLog[-1][1]][5]
        return None, None

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

    def check_castling(self, board):
        img_name = board[self.old_pos]
        color = img_name[4]
        fig = img_name[5]
        move_diff = (self.new_pos[0]-self.old_pos[0], self.new_pos[1]-self.old_pos[1])
        if fig == "K" and move_diff == (0, 2) and color == "w":
            board[(7, 5)] = board[(7, 7)]
            board.pop((7, 7))
        if fig == "K" and move_diff == (0, -2) and color == "w":
            board[(7, 3)] = board[(7, 0)]
            board.pop((7, 0))
        if fig == "K" and move_diff == (0, 2) and color == "b":
            board[(0, 5)] = board[(0, 7)]
            board.pop((0, 7))
        if fig == "K" and move_diff == (0, -2) and color == "b":
            board[(0, 3)] = board[(0, 0)]
            board.pop((0, 0))

    def check_en_passant(self, board):
        img_name = board[self.old_pos]
        color = img_name[4]
        fig = img_name[5]
        pos_diff = (self.new_pos[0] - self.old_pos[0], self.new_pos[1] - self.old_pos[1])
        if pos_diff in [(-1, -1), (-1, 1)] and self.new_pos not in board.keys() and color == "w" and fig == "P":
            return self.new_pos[0] + 1, self.new_pos[1]
        if pos_diff in [(1, -1), (1, 1)] and self.new_pos not in board.keys() and color == "b" and fig == "P":
            return self.new_pos[0] - 1, self.new_pos[1]
        return None, None

    def make_move(self):
        if self.old_pos in self.previous_board.keys():
            # print("RUCH",self.old_pos,self.new_pos)
            # self.previous_board = Gameplay.get_pieces()
            new_board = self.previous_board
            col, row = self.check_en_passant(new_board)
            if col is not None:
                new_board.pop((col, row))
            self.check_castling(new_board)
            # print(self.previous_board)
            fig_val = self.previous_board[self.old_pos]
            new_board.pop(self.old_pos)
            new_board[self.new_pos] = fig_val
            # Gameplay.moveLog.append((old_pos,new_pos))
            # print(Gameplay.moveLog)
            return new_board
