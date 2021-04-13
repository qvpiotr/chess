# Sprawdza czy podana pozycja jest na szachownicy

def in_borders(pos):
    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
        return False
    return True


class MovesGenerator:

    def __init__(self, gameplay):
        self.gameplay = gameplay

    # Generuje wszystkie ruchy zgodne z zasadami, ale mogą być w danej sytuacji niepoprawne
    # (poprawność sprawdza sobie gameplay)

    def generate_valid_moves(self):
        valid_moves = []
        self.generate_pawn_attacks(valid_moves)
        self.generate_pawn_moves(valid_moves)
        self.generate_knight_moves(valid_moves)
        self.generate_bishop_moves(valid_moves)
        self.generate_rock_moves(valid_moves)
        self.generate_queen_moves(valid_moves)
        self.generate_king_moves(valid_moves)
        self.generate_castling(valid_moves)
        return valid_moves

    # Generowanie roszad

    def generate_castling(self, valid_moves):
        if self.gameplay.active_color == "w":
            if self.gameplay.white_short_castling:
                valid_moves.append(((7, 4), (7, 6)))
            if self.gameplay.white_long_castling:
                valid_moves.append(((7, 4), (7, 2)))
        if self.gameplay.active_color == "b":
            if self.gameplay.black_short_castling:
                valid_moves.append(((0, 4), (0, 6)))
            if self.gameplay.black_long_castling:
                valid_moves.append(((0, 4), (0, 2)))

    # Generowanie bić piona

    def generate_pawn_attacks(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "P" or color != self.gameplay.active_color:
                continue
            if color == "w":
                if (pos[0] - 1, pos[1] + 1) in self.gameplay.pieces.keys() and \
                        self.gameplay.pieces.get((pos[0] - 1, pos[1] + 1))[4] == "b":
                    valid_moves.append(((pos[0], pos[1]), (pos[0] - 1, pos[1] + 1)))
                if (pos[0] - 1, pos[1] - 1) in self.gameplay.pieces.keys() \
                        and self.gameplay.pieces.get((pos[0] - 1, pos[1] - 1))[4] == "b":
                    valid_moves.append(((pos[0], pos[1]), (pos[0] - 1, pos[1] - 1)))
                # bicie w przelocie
                last_black_move, figure = self.gameplay.get_last_move()
                if last_black_move is None:
                    continue
                start_pos = last_black_move[0]
                end_pos = last_black_move[1]
                diff = (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])
                if diff == (2, 0) and figure == "P":
                    if (end_pos[0], end_pos[1] - 1) in self.gameplay.pieces.keys():
                        fig_type = self.gameplay.pieces[end_pos[0], end_pos[1]-1][5]
                        fig_color = self.gameplay.pieces[end_pos[0], end_pos[1]-1][4]
                        if fig_type == "P" and fig_color == self.gameplay.active_color:
                            valid_moves.append(((end_pos[0], end_pos[1]-1), (end_pos[0]-1, end_pos[1])))
                    if (end_pos[0], end_pos[1] + 1) in self.gameplay.pieces.keys():
                        fig_type = self.gameplay.pieces[end_pos[0], end_pos[1]+1][5]
                        fig_color = self.gameplay.pieces[end_pos[0], end_pos[1]+1][4]
                        if fig_type == "P" and fig_color == self.gameplay.active_color:
                            valid_moves.append(((end_pos[0], end_pos[1]+1), (end_pos[0]-1, end_pos[1])))
            else:
                if (pos[0] + 1, pos[1] + 1) in self.gameplay.pieces.keys() \
                        and self.gameplay.pieces.get((pos[0] + 1, pos[1] + 1))[4] == "w":
                    valid_moves.append(((pos[0], pos[1]), (pos[0] + 1, pos[1] + 1)))
                if (pos[0] + 1, pos[1] - 1) in self.gameplay.pieces.keys() \
                        and self.gameplay.pieces.get((pos[0] + 1, pos[1] - 1))[4] == "w":
                    valid_moves.append(((pos[0], pos[1]), (pos[0] + 1, pos[1] - 1)))
                # bicie w przelocie
                last_white_move, figure = self.gameplay.get_last_move()
                if last_white_move is None:
                    continue
                start_pos = last_white_move[0]
                end_pos = last_white_move[1]
                diff = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
                if diff == (-2, 0) and figure == "P":
                    if (end_pos[0], end_pos[1] - 1) in self.gameplay.pieces.keys():
                        fig_type = self.gameplay.pieces[end_pos[0], end_pos[1] - 1][5]
                        fig_color = self.gameplay.pieces[end_pos[0], end_pos[1] - 1][4]
                        if fig_type == "P" and fig_color == self.gameplay.active_color:
                            valid_moves.append(((end_pos[0], end_pos[1] - 1), (end_pos[0] + 1, end_pos[1])))
                    if (end_pos[0], end_pos[1] + 1) in self.gameplay.pieces.keys():
                        fig_type = self.gameplay.pieces[end_pos[0], end_pos[1] + 1][5]
                        fig_color = self.gameplay.pieces[end_pos[0], end_pos[1] + 1][4]
                        if fig_type == "P" and fig_color == self.gameplay.active_color:
                            valid_moves.append(((end_pos[0], end_pos[1] + 1), (end_pos[0] + 1, end_pos[1])))

    # Generowanie ruchów piona naprzód

    def generate_pawn_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "P" or color != self.gameplay.active_color:
                continue
            if color == "w":
                if (pos[0] - 1, pos[1]) not in self.gameplay.pieces.keys():
                    valid_moves.append(((pos[0], pos[1]), (pos[0] - 1, pos[1])))
                if pos[0] == 6 and (pos[0] - 2, pos[1]) not in self.gameplay.pieces.keys():
                    valid_moves.append(((pos[0], pos[1]), (pos[0] - 2, pos[1])))
            else:
                if (pos[0] + 1, pos[1]) not in self.gameplay.pieces.keys():
                    valid_moves.append(((pos[0], pos[1]), (pos[0] + 1, pos[1])))
                if pos[0] == 1 and (pos[0] + 2, pos[1]) not in self.gameplay.pieces.keys():
                    valid_moves.append(((pos[0], pos[1]), (pos[0] + 2, pos[1])))

    # Generowanie ruchów konia

    def generate_knight_moves(self, valid_moves):
        possible_vecs = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "N" or color != self.gameplay.active_color:
                continue
            for vector in possible_vecs:
                new_pos = (pos[0] + vector[0], pos[1] + vector[1])
                if new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7:
                    continue
                if new_pos in self.gameplay.pieces.keys() and \
                        self.gameplay.pieces.get(new_pos)[4] == self.gameplay.active_color:
                    continue
                valid_moves.append((pos, new_pos))

    # Generowanie ruchów gońca

    def generate_bishop_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "B" or color != self.gameplay.active_color:
                continue
            for x in range(-1, 2, 2):
                for y in range(-1, 2, 2):
                    vector = (x, y)
                    jump = 1
                    possible_pos = (jump*vector[0]+pos[0], jump*vector[1]+pos[1])
                    while in_borders(possible_pos) and possible_pos not in self.gameplay.pieces.keys():
                        valid_moves.append((pos, possible_pos))
                        jump += 1
                        possible_pos = (jump * vector[0] + pos[0], jump * vector[1] + pos[1])
                    if possible_pos in self.gameplay.pieces.keys():
                        if self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                            pass
                        else:
                            valid_moves.append((pos, possible_pos))

    # Generowanie ruchów wieży

    def generate_rock_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "R" or color != self.gameplay.active_color:
                continue
            for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    vector = (x, y)
                    jump = 1
                    possible_pos = (jump*vector[0]+pos[0], jump*vector[1]+pos[1])
                    while in_borders(possible_pos) and possible_pos not in self.gameplay.pieces.keys():
                        valid_moves.append((pos, possible_pos))
                        jump += 1
                        possible_pos = (jump * vector[0] + pos[0], jump * vector[1] + pos[1])
                    if possible_pos in self.gameplay.pieces.keys():
                        if self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                            pass
                        else:
                            valid_moves.append((pos, possible_pos))

    # Generowanie ruchów Hetmana

    def generate_queen_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "Q" or color != self.gameplay.active_color:
                continue
            for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    vector = (x, y)
                    jump = 1
                    possible_pos = (jump*vector[0]+pos[0], jump*vector[1]+pos[1])
                    while in_borders(possible_pos) and possible_pos not in self.gameplay.pieces.keys():
                        valid_moves.append((pos, possible_pos))
                        jump += 1
                        possible_pos = (jump * vector[0] + pos[0], jump * vector[1] + pos[1])
                    if possible_pos in self.gameplay.pieces.keys():
                        if self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                            pass
                        else:
                            valid_moves.append((pos, possible_pos))

    # Generowanie ruchów króla

    def generate_king_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "K" or color != self.gameplay.active_color:
                continue
            for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                vector = (x, y)
                possible_pos = (vector[0] + pos[0], vector[1] + pos[1])
                if in_borders(possible_pos):
                    if possible_pos in self.gameplay.pieces.keys() \
                            and self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                        continue
                    valid_moves.append((pos, possible_pos))
