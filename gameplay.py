from aiGame import aiGame
from twoPlayersGame import TwoPlayersGame
from fromPosGame import FromPos
import sys
from string import ascii_lowercase

import pygame_gui

from AI import *
from messageSender import Sender
from move import *
from movesGenerator import *


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
        self.depth = None
        self.board_values_hist = [0]
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
        self.history = [self.pieces]
        self.sender = Sender(self.board_screen)

    def main_game(self):
        """ Obsługa menu startowego - wybranie koloru, trybu gry i wywołanie odpowiedniej rozgrywki """
        pygame.display.set_caption('Chess')
        self.board_screen = pygame.display.set_mode((800, 480))

        background = pygame.Surface((800, 480))
        background.fill(pygame.Color('#1a1a19'))
        self.board_screen.blit(background, (0, 0))

        font = pygame.font.SysFont('Lucida Console', 20)
        img = font.render('I play as:', True, '#cdcdcb')
        self.board_screen.blit(img, (500, 140))

        self.draw_chessboard()
        self.draw_pieces()

        manager = pygame_gui.UIManager((800, 480), 'button.json')

        button_layout_rect = pygame.Rect(0, 0, 280, 30)
        button_layout_rect.topright = (-20, 20)

        play_computer = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                     text='Play with computer',
                                                     manager=manager,
                                                     anchors={'left': 'right',
                                                              'right': 'right',
                                                              'top': 'top',
                                                              'bottom': 'bottom'})

        button_layout_rect = pygame.Rect(0, 0, 280, 30)
        button_layout_rect.topright = (-20, 60)

        play_1vs1 = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                 text='Play 1 vs 1',
                                                 manager=manager,
                                                 anchors={'left': 'right',
                                                          'right': 'right',
                                                          'top': 'top',
                                                          'bottom': 'bottom'})

        button_layout_rect = pygame.Rect(0, 0, 280, 30)
        button_layout_rect.topright = (-20, 100)

        from_position = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                     text='Set and find move',
                                                     manager=manager,
                                                     anchors={'left': 'right',
                                                              'right': 'right',
                                                              'top': 'top',
                                                              'bottom': 'bottom'})

        button3_layout_rect = pygame.Rect(0, 0, 140, 30)
        button3_layout_rect.topright = (-20, 170)

        white_button3 = pygame_gui.elements.UIButton(relative_rect=button3_layout_rect,
                                                     text='White',
                                                     manager=manager,
                                                     anchors={'left': 'right',
                                                              'right': 'right',
                                                              'top': 'top',
                                                              'bottom': 'bottom'})

        button4_layout_rect = pygame.Rect(0, 0, 140, 30)
        button4_layout_rect.topright = (-160, 170)

        black_button4 = pygame_gui.elements.UIButton(relative_rect=button4_layout_rect,
                                                     text='Black',
                                                     manager=manager,
                                                     anchors={'left': 'right',
                                                              'right': 'right',
                                                              'top': 'top',
                                                              'bottom': 'bottom'})

        clock = pygame.time.Clock()
        is_running = True

        player_color = "w"

        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == white_button3:
                            player_color = "w"

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == black_button4:
                            player_color = "b"

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == play_1vs1:
                            game = TwoPlayersGame(self)
                            game.two_players_game()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == play_computer:
                            game = aiGame(self)
                            game.game_with_ai(player_color)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == from_position:
                            game = FromPos(self)
                            game.from_pos(player_color)

                manager.process_events(event)

            manager.update(time_delta)
            manager.draw_ui(self.board_screen)

            pygame.display.update()



    def get_input(self):
        """ Zwraca oznaczenia pola klikniętego przez gracza lub None w przypadku kliknięcia poza planszą """
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos()
                    pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                    if pos[0] > 7 or pos[1] > 7:
                        return None
                    return pos

    def count_figures(self, fig_type, max_allowed):
        """ Weryfikacja aby nie ustawiono więcej figur danego typu niż to możliwe,
            zwraca prawdę, jeśli jest możliwość ustawienia kolejnej figury danego typu"""
        counter = 0
        for pos, img in self.pieces.items():
            if img[4:6] == fig_type:
                counter += 1
        return True if counter <= max_allowed - 1 else False

    def set_pawn_check(self, pos):
        """ Nie dopuści możliwości ustawienia piona na skrajnej linii """
        if pos[0] == 0 or pos[0] == 7:
            return False
        return True

    def pos_to_string(self, pos):
        """ Konwersja tupla dwóch liczb, wyznaczonych kliknięciem na odpowiadające oznaczenie planszy"""
        return ascii_lowercase[pos[1]] + "" + str(8 - pos[0])

    def undo_move(self):
        """ Cofnięcie jednego ruchu """
        self.history.pop(-1)
        if len(self.board_values_hist) > 1:
            self.board_values_hist.pop(-1)
        self.pieces = self.history[-1]
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        self.draw_chessboard()
        self.draw_pieces()

    def set_depth(self, depth):
        """ Ustawienie głębokości przeszukiwania bota """
        self.depth = depth

    def draw_chessboard(self):
        """ Rysowanie planszy """
        colors = [(215, 199, 151), (164, 124, 72)]
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.board_screen, colors[(col + row) % 2],
                                 (col * self.field_side, row * self.field_side, self.field_side, self.field_side))
        for pos in range(8):
            font = pygame.font.SysFont('Lucida Console', 14)
            img = font.render(str(8 - pos), True, '#000000')
            self.board_screen.blit(img, (0, self.field_side * pos))
            img2 = font.render(str(ascii_lowercase[pos]), True, '#000000')
            self.board_screen.blit(img2, (self.field_side * pos, self.height - 15))

    def draw_pieces(self):
        """ Rysowanie figur """
        for pos, img_name in self.pieces.items():
            image = pygame.image.load(img_name)
            self.board_screen.blit(image, (pos[1] * self.field_side, pos[0] * self.field_side))

    def find_any_attacker(self):
        """ Kontrola rozstrzygania meczu, przydatne również przy weryfikacji roszady """
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

    def pos_in_danger(self, position):
        """ Zwraca prawdę jeśli dane pole jest pod atakiem rywala, wpp zwraca fałsz """
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        attacker = False
        moves = self.move_generator.generate_valid_moves()
        for start_pos, possible_pos in moves:
            if possible_pos == position:
                attacker = True
                break
        self.active_color, self.non_active_color = self.non_active_color, self.active_color
        return attacker

    def find_any_possible_move(self, valid_moves):
        """ Jeśli nie znaleziono akceptowalnego ruchu to zwraca fałsz. Warunek zakończenia partii """
        for start_pos, possible_pos in valid_moves:
            if self.check_move_correctness(start_pos, possible_pos):
                return True
        return False

    def check_move_correctness(self, start_pos, possible_pos):
        """ Sprawdzamy poprawność ruchu, przez sprawdzenie czy w następnym ruchu rywal może pokryć króla """
        if start_pos not in self.pieces:
            return False
        pos_diff = (abs(possible_pos[0] - start_pos[0]), abs(possible_pos[1] - start_pos[1]))  # roszada
        king_pos = [pos for pos, img_name in self.pieces.items() if img_name == "img/" + self.active_color + "K.png"]
        if (king_pos[0] == (7, 4) and self.active_color == "w") or (king_pos[0] == (0, 4) and self.active_color == "b"):
            if self.pieces[start_pos][5] == "K" and pos_diff == (0, 2):
                castling_type = "short"
                if possible_pos[1] == 2:
                    castling_type = "long"
                if not self.check_castling_availability(castling_type):
                    return False
                if self.pos_in_danger(possible_pos):
                    return False
        cp_init_pos = {}
        for pos, img in self.pieces.items():
            cp_init_pos[pos] = img
        king_safe = True
        move = Move(start_pos, possible_pos, self.pieces, self.board_screen)
        move.set_non_player_move()
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
        move_back = Move(possible_pos, start_pos, self.pieces, self.board_screen)
        move.set_non_player_move()
        self.pieces = move_back.make_move()
        self.pieces = cp_init_pos
        return king_safe

    def check_castling_availability(self, length):
        """ Weryfikacja możliwości roszady """
        if self.find_any_attacker():
            return False
        if length == "short" and self.active_color == "w":
            if (7, 5) in self.pieces.keys() or (7, 6) in self.pieces.keys():
                return False
            if (7, 7) not in self.pieces.keys():
                return False
        if length == "long" and self.active_color == "w":
            if (7, 1) in self.pieces.keys() or (7, 2) in self.pieces.keys() or (7, 3) in self.pieces.keys():
                return False
            if (7, 0) not in self.pieces.keys():
                return False
        if length == "short" and self.active_color == "b":
            if (0, 5) in self.pieces.keys() or (0, 6) in self.pieces.keys():
                return False
            if (0, 7) not in self.pieces.keys():
                return False
        if length == "long" and self.active_color == "b":
            if (0, 1) in self.pieces.keys() or (0, 2) in self.pieces.keys() or (0, 3) in self.pieces.keys():
                return False
            if (0, 0) not in self.pieces.keys():
                return False
        return True

    def update_castling_info(self, old_pos, new_pos):
        """ Aktualizacja możliwości wykonania roszady """
        if old_pos == (7, 4):
            self.white_long_castling = False
            self.white_short_castling = False
        if old_pos == (0, 4):
            self.black_long_castling = False
            self.black_short_castling = False
        if old_pos == (7, 0) or new_pos == (7, 0):
            self.white_long_castling = False
        if old_pos == (7, 7) or new_pos == (7, 7):
            self.white_short_castling = False
        if old_pos == (0, 0) or new_pos == (0, 0):
            self.black_long_castling = False
        if old_pos == (0, 7) or new_pos == (0, 7):
            self.black_short_castling = False

    def get_last_move(self):
        """ Pobranie ostatniego ruchu i figury wykonującej """
        if len(self.moveLog) != 0 and self.moveLog[-1][1] in self.pieces.keys():
            return self.moveLog[-1], self.pieces[self.moveLog[-1][1]][5]
        return None, None

    def get_screen(self):
        """ Getter na ekran obsługujący GUI """
        return self.board_screen