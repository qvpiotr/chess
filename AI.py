from move import *
from random import shuffle

CHECKMATE = 10000
STALEMATE = 0


class AI:

    def __init__(self, gameplay, depth):
        self.gameplay = gameplay
        self.next_move = None
        self.best_moves = []
        self.depth = depth
        self.screen = gameplay.get_screen()

    def filter_moves(self, moves):
        """ Wybiera z wszystkich poprawnych ruchów pod względem zasad ruchy, które można wykonać z danej pozycji """
        correct_moves = []
        if ((0, 4), (0, 2)) in moves and not self.gameplay.check_castling_availability("long"): # roszady
            moves.remove(((0, 4), (0, 2)))
        if ((0, 4), (0, 6)) in moves and not self.gameplay.check_castling_availability("short"):
            moves.remove(((0, 4), (0, 6)))
        if ((7, 4), (7, 2)) in moves and not self.gameplay.check_castling_availability("long"):
            moves.remove(((7, 4), (7, 2)))
        if ((7, 4), (7, 6)) in moves and not self.gameplay.check_castling_availability("short"):
            moves.remove(((7, 4), (7, 6)))
        for move in moves:
            if self.gameplay.check_move_correctness(move[0], move[1]):
                correct_moves.append(move)
        return correct_moves

    def get_next_move(self):
        """ Pobiera znaleziony ruch dla bota """
        return self.next_move

    def get_best_moves(self):
        """ Pobiera listę równoważnych najlepszych ruchów """
        return self.best_moves

    def print_board(self):
        """ Funkcja pomocnicza wypisująca w konsoli sytuację na planszy, pomocna przy weryfikacji działania bota """
        board = []
        for i in range(8):
            board.append([""] * 8)
        for i in range(8):
            for j in range(8):
                board[i][j] = "  "
        for pos, img in self.gameplay.pieces.items():
            board[pos[0]][pos[1]] = img[4:6]
        for i in range(8):
            print(board[i])

    def nega_max(self, valid_moves, depth, sign):
        """ Zwraca najbardziej korzystną ewaluację planszy dla bota, dodatkowo zapisuje równoważnie najlepsze ruchy w
            tablicy """
        if depth == 0:
            return sign * self.board_value(valid_moves)
        correct_moves = self.filter_moves(valid_moves)
        max_val = -CHECKMATE
        for move in correct_moves:
            cp_init_pos = {}
            for pos, img in self.gameplay.pieces.items():
                cp_init_pos[pos] = img
            next_move = Move(move[0], move[1], self.gameplay.pieces, self.screen)
            next_move.set_non_player_move()
            self.gameplay.pieces = next_move.make_move()
            self.gameplay.active_color, self.gameplay.non_active_color = self.gameplay.non_active_color, \
                                                                         self.gameplay.active_color
            score = -self.nega_max(self.gameplay.move_generator.generate_valid_moves(), depth - 1, -sign)
            if score == max_val and depth == self.depth:
                self.best_moves.append(move)
            elif score > max_val:
                max_val = score
                if depth == self.depth:
                    self.best_moves.clear()
                    self.best_moves.append(move)
                    self.next_move = move
            back_move = Move(move[1], move[0], self.gameplay.pieces, self.screen)
            back_move.set_non_player_move()
            self.gameplay.pieces = back_move.make_move()
            self.gameplay.active_color, self.gameplay.non_active_color = self.gameplay.non_active_color, \
                                                                         self.gameplay.active_color
            self.gameplay.pieces = cp_init_pos
        return max_val

    def nega_max_alpha_beta(self, valid_moves, depth, sign, alpha, beta):
        """ Znajduje jeden ruch dla bota, o największej wartości na planszy, zwraca wartość tego ruchu """
        if self.gameplay.pieces is None:
            print("_")
        if depth == 0:
            return sign * self.board_value(valid_moves)
        correct_moves = self.filter_moves(valid_moves)
        shuffle(correct_moves)
        max_val = -CHECKMATE
        for move in correct_moves:
            cp_init_pos = {}
            for pos, img in self.gameplay.pieces.items():
                cp_init_pos[pos] = img
            next_move = Move(move[0], move[1], self.gameplay.pieces, self.screen)
            next_move.set_non_player_move()
            self.gameplay.pieces = next_move.make_move()
            self.gameplay.active_color, self.gameplay.non_active_color = self.gameplay.non_active_color, \
                                                                         self.gameplay.active_color
            score = -1*self.nega_max_alpha_beta(self.gameplay.move_generator.generate_valid_moves(), depth - 1, -sign, -beta, -alpha)
            if score > max_val:
                max_val = score
                if depth == self.depth:
                    self.next_move = move
            back_move = Move(move[1], move[0], self.gameplay.pieces, self.screen)
            back_move.set_non_player_move()
            self.gameplay.pieces = back_move.make_move()
            self.gameplay.active_color, self.gameplay.non_active_color = self.gameplay.non_active_color, \
                                                                         self.gameplay.active_color
            self.gameplay.pieces = cp_init_pos
            alpha = max(alpha, max_val)
            if alpha >= beta:
                break
        return max_val

    def board_value(self, valid_moves):
        """ Zwraca wartość obliczonej sytuacji na planszy """
        if not self.gameplay.find_any_possible_move(valid_moves):
            if self.gameplay.find_any_attacker():
                return CHECKMATE
            else:
                return STALEMATE
        score = 0
        fig_val = {"wK": 0, "bK": 0, "wQ": 10, "bQ": -10, "wB": 3, "bB": -3, "wR": 5, "bR": -5,
                   "wN": 3, "bN": -3, "wP": 1, "bP": -1}
        for pos, img in self.gameplay.pieces.items():
            piece_type = img[4:6]
            score = score +fig_val[piece_type]
        return score
