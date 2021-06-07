import pygame_gui
import sys
from AI import *
from move import *
from MovesGenerator import *


class FromPos:

    def __init__(self, gameplan):
        self.gameplan = gameplan

    
    def from_pos(self, player_color):
        """ Tryb gry, gdzie gracz ustawia własną sytuację i ma wykonać najlepszy ruch """
        global time_delta
        self.gameplan.pieces = {}
        self.gameplan.draw_chessboard()
        self.gameplan.draw_pieces()

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
                                self.gameplan.sender.put_message("Both kings must be on board")
                            else:
                                running = 0
                        if event.ui_element == bB:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("bB", 10):
                                self.gameplan.pieces[pos] = "img/bB.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == bK and bK_control:
                            bK_control = 0
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            self.gameplan.pieces[pos] = "img/bK.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == bN:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("bN", 10):
                                self.gameplan.pieces[pos] = "img/bN.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == bP:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.set_pawn_check(pos):
                                self.gameplan.pieces[pos] = "img/bP.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == bQ:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("bQ", 9):
                                self.gameplan.pieces[pos] = "img/bQ.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == bR:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("bR", 10):
                                self.gameplan.pieces[pos] = "img/bR.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == wB:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("wB", 10):
                                self.gameplan.pieces[pos] = "img/wB.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == wK and wK_control:
                            wK_control = 0
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            self.gameplan.pieces[pos] = "img/wK.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == wN:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("wN", 10):
                                self.gameplan.pieces[pos] = "img/wN.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == wP:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.set_pawn_check(pos):
                                self.gameplan.pieces[pos] = "img/wP.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == wQ:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("wQ", 9):
                                self.gameplan.pieces[pos] = "img/wQ.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                        if event.ui_element == wR:
                            pos = self.gameplan.get_input()
                            if pos is None:
                                continue
                            if self.gameplan.count_figures("wR", 10):
                                self.gameplan.pieces[pos] = "img/wR.png"
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()
                manager.process_events(event)
                manager.update(time_delta)
                manager.draw_ui(self.gameplan.board_screen)
                pygame.display.flip()

        if player_color == "b":
            self.gameplan.active_color, self.gameplan.non_active_color = self.gameplan.non_active_color, self.gameplan.active_color
        old_pos = None
        to_move = False
        pygame.display.update()

        valid_moves = self.gameplan.move_generator.generate_valid_moves()

        running = 1
        depth = 1
        best_moves = None
        while depth < 4:
            ai = AI(self.gameplan, depth)
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
                    old_pos = ((click_pos[1]) // self.gameplan.field_side, click_pos[0] // self.gameplan.field_side)
                    if old_pos in self.gameplan.pieces.keys() and self.gameplan.pieces.get(old_pos)[4] == self.gameplan.active_color:
                        pygame.draw.rect(self.gameplan.board_screen, (255, 255, 0),
                                         (old_pos[1] * self.gameplan.field_side, old_pos[0] * self.gameplan.field_side, self.gameplan.field_side,
                                          self.gameplan.field_side))
                        to_move = True

                        for moves in valid_moves:
                            if moves[0] == old_pos and self.gameplan.check_move_correctness(moves[0], moves[1]):
                                if ((moves[1][0] % 2 == 0 and moves[1][1] % 2 != 0) or (
                                        moves[1][0] % 2 != 0 and moves[1][1] % 2 == 0)):
                                    pygame.draw.rect(self.gameplan.board_screen, (255, 255, 102),
                                                     (moves[1][1] * self.gameplan.field_side, moves[1][0] * self.gameplan.field_side,
                                                      self.gameplan.field_side,
                                                      self.gameplan.field_side))
                                else:
                                    pygame.draw.rect(self.gameplan.board_screen, (255, 255, 204),
                                                     (moves[1][1] * self.gameplan.field_side, moves[1][0] * self.gameplan.field_side,
                                                      self.gameplan.field_side,
                                                      self.gameplan.field_side))
                        self.gameplan.draw_pieces()

                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = ((click_pos[1]) // self.gameplan.field_side, click_pos[0] // self.gameplan.field_side)

                    if (old_pos, new_pos) in valid_moves and self.gameplan.check_move_correctness(old_pos, new_pos):
                        fig = self.gameplan.pieces[old_pos][5]
                        move_diff = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
                        if fig == "K" and move_diff == (0, 2):
                            if not self.gameplan.check_castling_availability("short"):
                                break
                        if fig == "K" and move_diff == (0, -2):
                            if not self.gameplan.check_castling_availability("long"):
                                break

                        if (old_pos, new_pos) in best_moves:
                            move = Move(old_pos, new_pos, self.gameplan.pieces, self.gameplan.board_screen)
                            self.gameplan.sender.put_message("Move " + self.gameplan.pos_to_string(old_pos) + "-" + self.gameplan.pos_to_string(new_pos))
                            self.gameplan.pieces = move.make_move()
                            self.gameplan.history.append(self.gameplan.pieces)
                            self.gameplan.update_castling_info(old_pos, new_pos)
                            self.gameplan.moveLog.append((old_pos, new_pos))
                            self.gameplan.active_color, self.gameplan.non_active_color = self.gameplan.non_active_color, self.gameplan.active_color
                            running = 0
                        else:
                            self.gameplan.sender.put_message("Bad move. Try again")
                    to_move = False
                    valid_moves = self.gameplan.move_generator.generate_valid_moves()
                    if not self.gameplan.find_any_possible_move(valid_moves):
                        if self.gameplan.find_any_attacker():
                            text = "black" if self.gameplan.active_color == "w" else "white"
                            text += " won"
                            self.gameplan.sender.put_message(text)
                        else:
                            self.gameplan.sender.put_message("tie")
                    self.gameplan.draw_chessboard()
                    self.gameplan.draw_pieces()
                    manager.update(time_delta)
                    manager.draw_ui(self.gameplan.board_screen)
                    pygame.display.update()
                pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()