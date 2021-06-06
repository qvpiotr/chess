import pygame
from messageSender import Sender

class Move:

    def __init__(self, old_pos, new_pos, previous_board, board_screen):
        self.previous_board = previous_board
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.player_move = True
        self.screen = board_screen

    def set_non_player_move(self):
        """ Funkcja pomocnicza, która informuje o tym, że ruch jest:
            - wykonywany przez bota
            - testowy w celu sprawdzenia pewnej sytuacji po nim """
        self.player_move = False

    def check_castling(self, board):
        """ Weryfikacja roszady - po przestawieniu króla automatycznie przestawi też odpowiednią wieżę """
        img_name = board[self.old_pos]
        color = img_name[4]
        fig = img_name[5]
        move_diff = (self.new_pos[0]-self.old_pos[0], self.new_pos[1]-self.old_pos[1])
        if self.old_pos == (7, 4):
            if fig == "K" and move_diff == (0, 2) and color == "w":
                board[(7, 5)] = board[(7, 7)]
                board.pop((7, 7))
            if fig == "K" and move_diff == (0, -2) and color == "w":
                board[(7, 3)] = board[(7, 0)]
                board.pop((7, 0))
        if self.old_pos == (0, 4):
            if fig == "K" and move_diff == (0, 2) and color == "b":
                board[(0, 5)] = board[(0, 7)]
                board.pop((0, 7))
            if fig == "K" and move_diff == (0, -2) and color == "b":
                board[(0, 3)] = board[(0, 0)]
                board.pop((0, 0))

    def check_en_passant(self, board):
        """ Sprawdza czy wykonano bicie w przelocie """
        img_name = board[self.old_pos]
        color = img_name[4]
        fig = img_name[5]
        pos_diff = (self.new_pos[0] - self.old_pos[0], self.new_pos[1] - self.old_pos[1])
        if pos_diff in [(-1, -1), (-1, 1)] and self.new_pos not in board.keys() and color == "w" and fig == "P":
            return self.new_pos[0] + 1, self.new_pos[1]
        if pos_diff in [(1, -1), (1, 1)] and self.new_pos not in board.keys() and color == "b" and fig == "P":
            return self.new_pos[0] - 1, self.new_pos[1]
        return None, None

    def promote_pawn(self, board):
        """ Funkcja do obsługi promocji piona na ostatniej linii """
        color = board[self.new_pos][4]
        fig = board[self.new_pos][5]
        promotion = False
        if fig == "P" and color == "w" and self.new_pos[0] == 0:
            promotion = True
        if fig == "P" and color == "b" and self.new_pos[0] == 7:
            promotion = True
        sender = Sender(self.screen)
        if promotion:
            if self.player_move:
                sender.put_message("Left to commit, right to switch")
                figures = ["Q", "R", "B", "N"]
                running = 1
                type_counter = -1
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 3:
                                type_counter = (type_counter + 1) % 4
                                sender.put_message("Actual choice {0}".format(figures[type_counter]))
                            elif event.button == 1 and type_counter != -1:
                                running = 0
                new_fig = figures[type_counter]
                board[self.new_pos] = "img/"+color+new_fig+".png"
            else:
                board[self.new_pos] = "img/"+color+"Q.png"

    def make_move(self):
        """ Funkcja obsługująca wykonanie jednego ruchu z old_pos do new_pos """
        if self.old_pos in self.previous_board.keys():
            new_board = self.previous_board
            col, row = self.check_en_passant(new_board)
            if col is not None:
                new_board.pop((col, row))
            self.check_castling(new_board)
            fig_val = self.previous_board[self.old_pos]
            new_board.pop(self.old_pos)
            new_board[self.new_pos] = fig_val
            self.promote_pawn(new_board)
            return new_board
