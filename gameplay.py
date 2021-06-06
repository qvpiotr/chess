import sys
import pygame_gui
from movesGenerator import *
from AI import *
from move import *
from messageSender import Sender
from string import ascii_lowercase


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

        # font = pygame.font.SysFont('Lucida Console', 12)
        # img = font.render('It will be info about your move here:', True, '#cdcdcb')
        # window_surface.blit(img, (500, 200))

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
                            self.two_players_game()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == play_computer:
                            self.game_with_ai(player_color)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == from_position:
                            self.from_pos(player_color)

                manager.process_events(event)

            manager.update(time_delta)
            manager.draw_ui(self.board_screen)

            pygame.display.update()

    def two_players_game(self):
        """ Obsługuje gre dla dwóch ludzi """
        clock = pygame.time.Clock()
        manager = pygame_gui.UIManager((800, 480), 'button.json')

        button_layout_rect = pygame.Rect(0, 0, 280, 30)
        button_layout_rect.topright = (-20, 210)

        undo_move = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                 text='Undo move',
                                                 manager=manager,
                                                 anchors={'left': 'right',
                                                          'right': 'right',
                                                          'top': 'top',
                                                          'bottom': 'bottom'})

        old_pos = None
        to_move = False
        pygame.display.update()

        valid_moves = self.move_generator.generate_valid_moves()
        while 1:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                    click_pos = pygame.mouse.get_pos()
                    old_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                    if old_pos in self.pieces.keys() and self.pieces.get(old_pos)[4] == self.active_color:
                        pygame.draw.rect(self.board_screen, (255, 255, 0),
                                         (old_pos[1] * self.field_side, old_pos[0] * self.field_side, self.field_side,
                                          self.field_side))
                        to_move = True

                        for moves in valid_moves:
                            if moves[0] == old_pos and self.check_move_correctness(moves[0], moves[1]):
                                if (moves[1][0] % 2 == 0 and moves[1][1] % 2 != 0) or (moves[1][0] % 2 != 0 and
                                                                                       moves[1][1] % 2 == 0):
                                    pygame.draw.rect(self.board_screen, (255, 255, 102),
                                                     (moves[1][1] * self.field_side, moves[1][0] * self.field_side,
                                                      self.field_side, self.field_side))
                                else:
                                    pygame.draw.rect(self.board_screen, (255, 255, 204),
                                                     (moves[1][1] * self.field_side, moves[1][0] * self.field_side,
                                                      self.field_side, self.field_side))
                        self.draw_pieces()

                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)

                    if (old_pos, new_pos) in valid_moves and self.check_move_correctness(old_pos, new_pos):
                        fig = self.pieces[old_pos][5]
                        move_diff = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
                        if fig == "K" and move_diff == (0, 2):
                            if not self.check_castling_availability("short"):
                                break
                        if fig == "K" and move_diff == (0, -2):
                            if not self.check_castling_availability("long"):
                                break
                        move = Move(old_pos, new_pos, self.pieces, self.board_screen)
                        self.sender.put_message("Move "+self.pos_to_string(old_pos)+"-"+self.pos_to_string(new_pos))
                        self.pieces = move.make_move()
                        self.history.append(self.pieces)
                        self.update_castling_info(old_pos, new_pos)
                        self.moveLog.append((old_pos, new_pos))
                        self.active_color, self.non_active_color = self.non_active_color, self.active_color
                    to_move = False
                    valid_moves = self.move_generator.generate_valid_moves()
                    if not self.find_any_possible_move(valid_moves):
                        if self.find_any_attacker():
                            text = "black" if self.active_color == "w" else "white"
                            text += " won"
                            self.sender.put_message(text)
                        else:
                            self.sender.put_message("tie")
                    self.draw_chessboard()
                    self.draw_pieces()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and len(self.history) > 1:
                        self.undo_move()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == undo_move and len(self.history) > 1:
                            self.undo_move()
                manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(self.board_screen)
            pygame.display.flip()

    def game_with_ai(self, player_color):

        """ Obsługa pełnej gry z botem """

        clock = pygame.time.Clock()
        manager = pygame_gui.UIManager((800, 480), 'button.json')

        button_layout_rect = pygame.Rect(0, 0, 280, 30)
        button_layout_rect.topright = (-20, 210)

        undo_move = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                 text='Undo move',
                                                 manager=manager,
                                                 anchors={'left': 'right',
                                                          'right': 'right',
                                                          'top': 'top',
                                                          'bottom': 'bottom'})

        old_pos = None
        to_move = False
        pygame.display.update()

        valid_moves = self.move_generator.generate_valid_moves()
        while 1:
            time_delta = clock.tick(60) / 1000.0
            if self.active_color == player_color:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                        click_pos = pygame.mouse.get_pos()
                        old_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                        if old_pos in self.pieces.keys() and self.pieces.get(old_pos)[4] == self.active_color:
                            pygame.draw.rect(self.board_screen, (255, 255, 0),
                                             (old_pos[1] * self.field_side, old_pos[0] * self.field_side,
                                              self.field_side,
                                              self.field_side))
                            to_move = True

                            for moves in valid_moves:
                                if moves[0] == old_pos and self.check_move_correctness(moves[0], moves[1]):
                                    if (moves[1][0] % 2 != 0 and moves[1][1] % 2 != 0) or (moves[1][0] % 2 == 0 and
                                                                                           moves[1][1] % 2 == 0):
                                        pygame.draw.rect(self.board_screen, (255, 255, 204),
                                                         (moves[1][1] * self.field_side, moves[1][0] * self.field_side,
                                                          self.field_side, self.field_side))
                                    else:
                                        pygame.draw.rect(self.board_screen, (255, 255, 102),
                                                         (moves[1][1] * self.field_side, moves[1][0] * self.field_side,
                                                          self.field_side, self.field_side))
                                    self.draw_pieces()
                    elif event.type == pygame.MOUSEBUTTONUP and to_move:
                        click_pos = pygame.mouse.get_pos()
                        new_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                        if (old_pos, new_pos) in valid_moves and self.check_move_correctness(old_pos, new_pos):
                            fig = self.pieces[old_pos][5]
                            move_diff = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
                            if fig == "K" and move_diff == (0, 2):
                                if not self.check_castling_availability("short"):
                                    break
                            if fig == "K" and move_diff == (0, -2):
                                if not self.check_castling_availability("long"):
                                    break
                            move = Move(old_pos, new_pos, self.pieces, self.board_screen)
                            self.sender.put_message("Move "+self.pos_to_string(old_pos)+"-"+self.pos_to_string(new_pos))
                            self.pieces = move.make_move()
                            self.history.append(self.pieces)
                            self.update_castling_info(old_pos, new_pos)
                            self.moveLog.append((old_pos, new_pos))
                            self.active_color, self.non_active_color = self.non_active_color, self.active_color
                        to_move = False
                        valid_moves = self.move_generator.generate_valid_moves()

                        if not self.find_any_possible_move(valid_moves):
                            if self.find_any_attacker():
                                text = "black" if self.active_color == "w" else "white"
                                text += " won"
                                self.sender.put_message(text)
                                break
                            else:
                                self.sender.put_message("tie")
                                break
                        self.draw_chessboard()
                        self.draw_pieces()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b and len(self.history) > 2:
                            self.undo_move()
                            self.undo_move()

                    elif event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == undo_move and len(self.history) > 2:
                                self.undo_move()
                                self.undo_move()
                    manager.process_events(event)
                    manager.update(time_delta)
                    manager.draw_ui(self.board_screen)
                    pygame.display.flip()
            else:
                depth = self.depth + 2
                bot_move = None
                while bot_move is None and depth > 0:
                    depth -= 2
                    ai = AI(self, depth)
                    ai.nega_max_alpha_beta(valid_moves, depth, -1 if player_color == "w" else 1, -10000, 10000)
                    bot_move = ai.get_next_move()
                if bot_move is None:
                    break
                if self.check_move_correctness(bot_move[0], bot_move[1]):
                    fig = self.pieces[bot_move[0]][5]
                    move_diff = (bot_move[1][0] - bot_move[0][0], bot_move[1][1] - bot_move[0][1])
                    if fig == "K" and move_diff == (0, 2):
                        if not self.check_castling_availability("short"):
                            continue
                    if fig == "K" and move_diff == (0, -2):
                        if not self.check_castling_availability("long"):
                            continue
                    move = Move(bot_move[0], bot_move[1], self.pieces, self.board_screen)
                    self.sender.put_message("Move "+self.pos_to_string(bot_move[0])+"-"+self.pos_to_string(bot_move[1]))
                    move.set_non_player_move()
                    self.pieces = move.make_move()
                    player_move_eval = AI(self, 1)
                    self.board_values_hist.append(player_move_eval.board_value(valid_moves))
                    if self.board_values_hist[-2] - self.board_values_hist[-1] > 1 and player_color == "w":
                        self.sender.put_message("Would suggest to undo move")
                    elif self.board_values_hist[-2] - self.board_values_hist[-1] < -1 and player_color == "b":
                        self.sender.put_message("Would suggest to undo move")
                    self.history.append(self.pieces)
                    self.update_castling_info(bot_move[0], bot_move[1])
                    self.moveLog.append((bot_move[0], bot_move[1]))
                    self.active_color, self.non_active_color = self.non_active_color, self.active_color
                valid_moves = self.move_generator.generate_valid_moves()
                if not self.find_any_possible_move(valid_moves):
                    if self.find_any_attacker():
                        text = "black" if self.active_color == "w" else "white"
                        text += " won"
                        self.sender.put_message(text)
                        break
                    else:
                        self.sender.put_message("tie")
                        break
                self.draw_chessboard()
                self.draw_pieces()
            pygame.display.flip()

        self.draw_chessboard()
        self.draw_pieces()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()

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

    def from_pos(self, player_color):
        """ Tryb gry, gdzie gracz ustawia własną sytuację i ma wykonać najlepszy ruch """
        global time_delta
        self.pieces = {}
        self.draw_chessboard()
        self.draw_pieces()

        clock = pygame.time.Clock()
        manager = pygame_gui.UIManager((800, 480), 'button.json')

        button_layout_rect = pygame.Rect(0, 0, 280, 30)
        button_layout_rect.topright = (-20, 210)

        commit = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                              text='Commit',
                                              manager=manager,
                                              anchors={'left': 'right',
                                                       'right': 'right',
                                                       'top': 'top',
                                                       'bottom': 'bottom'})

        black_pieces = {"bB", "bK", "bN", "bP", "bQ", "bR"}
        white_pieces = {"wB", "wK", "wN", "wP", "wQ", "wR"}
        button_layout_rect = pygame.Rect(0, 0, 30, 30)
        button_layout_rect.topright = (-20, 240)
        i = 0

        for piece in black_pieces:
            # image = pygame.image.load('img/'+ piece +'.png')
            # image = pygame.transform.scale(image, (40,35))
            button_layout_rect.topright = (-20 + i, 250)
            globals()['%s' % piece] = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                                   text="",
                                                                   manager=manager,
                                                                   object_id=f"{piece}",
                                                                   anchors={'left': 'right',
                                                                            'right': 'right',
                                                                            'top': 'top',
                                                                            'bottom': 'bottom'})

            i -= 50

        i = 0
        for piece in white_pieces:
            # image = pygame.image.load('img/'+ piece +'.png')
            # image = pygame.transform.scale(image, (40,35))
            button_layout_rect.topright = (-20 + i, 300)
            globals()['%s' % piece] = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                                   text="",
                                                                   manager=manager,
                                                                   object_id=f"{piece}",
                                                                   anchors={'left': 'right',
                                                                            'right': 'right',
                                                                            'top': 'top',
                                                                            'bottom': 'bottom'})

            i -= 50

        running = 1
        wK_control = 1
        bK_control = 1

        while running or wK_control or bK_control:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == commit:
                            if bK_control or wK_control:
                                self.sender.put_message("Both kings must be on board")
                            else:
                                running = 0
                        if event.ui_element == bB:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("bB", 10):
                                self.pieces[pos] = "img/bB.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == bK and bK_control:
                            bK_control = 0
                            pos = self.get_input()
                            if pos is None:
                                continue
                            self.pieces[pos] = "img/bK.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == bN:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("bN", 10):
                                self.pieces[pos] = "img/bN.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == bP:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.set_pawn_check(pos):
                                self.pieces[pos] = "img/bP.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == bQ:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("bQ", 9):
                                self.pieces[pos] = "img/bQ.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == bR:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("bR", 10):
                                self.pieces[pos] = "img/bR.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == wB:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("wB", 10):
                                self.pieces[pos] = "img/wB.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == wK and wK_control:
                            wK_control = 0
                            pos = self.get_input()
                            if pos is None:
                                continue
                            self.pieces[pos] = "img/wK.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == wN:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("wN", 10):
                                self.pieces[pos] = "img/wN.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == wP:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.set_pawn_check(pos):
                                self.pieces[pos] = "img/wP.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == wQ:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("wQ", 9):
                                self.pieces[pos] = "img/wQ.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                        if event.ui_element == wR:
                            pos = self.get_input()
                            if pos is None:
                                continue
                            if self.count_figures("wR", 10):
                                self.pieces[pos] = "img/wR.png"
                            self.draw_chessboard()
                            self.draw_pieces()
                manager.process_events(event)
                manager.update(time_delta)
                manager.draw_ui(self.board_screen)
                pygame.display.flip()

        if player_color == "b":
            self.active_color, self.non_active_color = self.non_active_color, self.active_color
        old_pos = None
        to_move = False
        pygame.display.update()

        valid_moves = self.move_generator.generate_valid_moves()

        running = 1
        depth = 1
        best_moves = None
        while depth < 4:
            ai = AI(self, depth)
            value = ai.nega_max(valid_moves, depth, 1 if player_color == "w" else -1)
            best_moves = ai.get_best_moves()
            if value == CHECKMATE:
                break
            depth += 2

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                    click_pos = pygame.mouse.get_pos()
                    old_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)
                    if old_pos in self.pieces.keys() and self.pieces.get(old_pos)[4] == self.active_color:
                        pygame.draw.rect(self.board_screen, (255, 255, 0),
                                         (old_pos[1] * self.field_side, old_pos[0] * self.field_side, self.field_side,
                                          self.field_side))
                        to_move = True

                        for moves in valid_moves:
                            if moves[0] == old_pos and self.check_move_correctness(moves[0], moves[1]):
                                if ((moves[1][0] % 2 == 0 and moves[1][1] % 2 != 0) or (
                                        moves[1][0] % 2 != 0 and moves[1][1] % 2 == 0)):
                                    pygame.draw.rect(self.board_screen, (255, 255, 102),
                                                     (moves[1][1] * self.field_side, moves[1][0] * self.field_side,
                                                      self.field_side,
                                                      self.field_side))
                                else:
                                    pygame.draw.rect(self.board_screen, (255, 255, 204),
                                                     (moves[1][1] * self.field_side, moves[1][0] * self.field_side,
                                                      self.field_side,
                                                      self.field_side))
                        self.draw_pieces()

                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = ((click_pos[1]) // self.field_side, click_pos[0] // self.field_side)

                    if (old_pos, new_pos) in valid_moves and self.check_move_correctness(old_pos, new_pos):
                        fig = self.pieces[old_pos][5]
                        move_diff = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
                        if fig == "K" and move_diff == (0, 2):
                            if not self.check_castling_availability("short"):
                                break
                        if fig == "K" and move_diff == (0, -2):
                            if not self.check_castling_availability("long"):
                                break

                        if (old_pos, new_pos) in best_moves:
                            move = Move(old_pos, new_pos, self.pieces, self.board_screen)
                            self.sender.put_message("Move " + self.pos_to_string(old_pos) + "-" + self.pos_to_string(new_pos))
                            self.pieces = move.make_move()
                            self.history.append(self.pieces)
                            self.update_castling_info(old_pos, new_pos)
                            self.moveLog.append((old_pos, new_pos))
                            self.active_color, self.non_active_color = self.non_active_color, self.active_color
                            running = 0
                        else:
                            self.sender.put_message("Bad move. Try again")
                    to_move = False
                    valid_moves = self.move_generator.generate_valid_moves()
                    if not self.find_any_possible_move(valid_moves):
                        if self.find_any_attacker():
                            text = "black" if self.active_color == "w" else "white"
                            text += " won"
                            self.sender.put_message(text)
                        else:
                            self.sender.put_message("tie")
                    self.draw_chessboard()
                    self.draw_pieces()
                    manager.update(time_delta)
                    manager.draw_ui(self.board_screen)
                    pygame.display.update()
                pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()

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
            # image = pygame.transform.scale(image, (self.field_side, self.field_side))
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