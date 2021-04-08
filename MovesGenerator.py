class MovesGenerator:

    def __init__(self, gameplay):
        self.gameplay = gameplay

    def in_borders(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return False
        return True

    def generate_valid_moves(self):
        valid_moves = []
        self.generate_pawn_attacks(valid_moves)
        self.generate_pawn_moves(valid_moves)
        self.generate_knight_moves(valid_moves)
        self.generate_bishop_moves(valid_moves)
        self.generate_rock_moves(valid_moves)
        self.generate_queen_moves(valid_moves)
        self.generate_king_moves(valid_moves)
        return valid_moves

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
            else:
                if (pos[0] + 1, pos[1] + 1) in self.gameplay.pieces.keys() \
                        and self.gameplay.pieces.get((pos[0] + 1, pos[1] + 1))[4] == "w":
                    valid_moves.append(((pos[0], pos[1]), (pos[0] + 1, pos[1] + 1)))
                if (pos[0] + 1, pos[1] - 1) in self.gameplay.pieces.keys() \
                        and self.gameplay.pieces.get((pos[0] + 1, pos[1] - 1))[4] == "w":
                    valid_moves.append(((pos[0], pos[1]), (pos[0] + 1, pos[1] - 1)))

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
                    while self.in_borders(possible_pos) and possible_pos not in self.gameplay.pieces.keys():
                        valid_moves.append((pos, possible_pos))
                        jump += 1
                        possible_pos = (jump * vector[0] + pos[0], jump * vector[1] + pos[1])
                    if possible_pos in self.gameplay.pieces.keys():
                        if self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                            pass
                        else:
                            valid_moves.append((pos, possible_pos))

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
                    while self.in_borders(possible_pos) and possible_pos not in self.gameplay.pieces.keys():
                        valid_moves.append((pos, possible_pos))
                        jump += 1
                        possible_pos = (jump * vector[0] + pos[0], jump * vector[1] + pos[1])
                    if possible_pos in self.gameplay.pieces.keys():
                        if self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                            pass
                        else:
                            valid_moves.append((pos, possible_pos))

    def generate_queen_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "Q" or color != self.gameplay.active_color:
                continue
            for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1),(-1, 1), (-1, -1)]:
                    vector = (x, y)
                    jump = 1
                    possible_pos = (jump*vector[0]+pos[0], jump*vector[1]+pos[1])
                    while self.in_borders(possible_pos) and possible_pos not in self.gameplay.pieces.keys():
                        valid_moves.append((pos, possible_pos))
                        jump += 1
                        possible_pos = (jump * vector[0] + pos[0], jump * vector[1] + pos[1])
                    if possible_pos in self.gameplay.pieces.keys():
                        if self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                            pass
                        else:
                            valid_moves.append((pos, possible_pos))

    def generate_king_moves(self, valid_moves):
        for pos, img in self.gameplay.pieces.items():
            color = img[4]
            fig = img[5]
            if fig != "K" or color != self.gameplay.active_color:
                continue
            for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1),(-1, 1), (-1, -1)]:
                vector = (x, y)
                possible_pos = (vector[0] + pos[0], vector[1] + pos[1])
                if self.in_borders(possible_pos):
                    if possible_pos in self.gameplay.pieces.keys() \
                            and self.gameplay.pieces.get(possible_pos)[4] == self.gameplay.active_color:
                        continue
                    valid_moves.append((pos,possible_pos))