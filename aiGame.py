import pygame_gui
import sys
from AI import *
from move import *
from MovesGenerator import *



class aiGame:

        def __init__(self, gameplan):
            self.gameplan = gameplan

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

            valid_moves = self.gameplan.move_generator.generate_valid_moves()
            while 1:
                time_delta = clock.tick(60) / 1000.0
                if self.gameplan.active_color == player_color:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                            click_pos = pygame.mouse.get_pos()
                            old_pos = ((click_pos[1]) // self.gameplan.field_side, click_pos[0] // self.gameplan.field_side)
                            if old_pos in self.gameplan.pieces.keys() and self.gameplan.pieces.get(old_pos)[4] == self.gameplan.active_color:
                                pygame.draw.rect(self.gameplan.board_screen, (255, 255, 0),
                                                (old_pos[1] * self.gameplan.field_side, old_pos[0] * self.gameplan.field_side,
                                                self.gameplan.field_side,
                                                self.gameplan.field_side))
                                to_move = True

                                for moves in valid_moves:
                                    if moves[0] == old_pos and self.gameplan.check_move_correctness(moves[0], moves[1]):
                                        if (moves[1][0] % 2 != 0 and moves[1][1] % 2 != 0) or (moves[1][0] % 2 == 0 and
                                                                                            moves[1][1] % 2 == 0):
                                            pygame.draw.rect(self.gameplan.board_screen, (255, 255, 204),
                                                            (moves[1][1] * self.gameplan.field_side, moves[1][0] * self.gameplan.field_side,
                                                            self.gameplan.field_side, self.gameplan.field_side))
                                        else:
                                            pygame.draw.rect(self.gameplan.board_screen, (255, 255, 102),
                                                            (moves[1][1] * self.gameplan.field_side, moves[1][0] * self.gameplan.field_side,
                                                            self.gameplan.field_side, self.gameplan.field_side))
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
                                move = Move(old_pos, new_pos, self.gameplan.pieces, self.gameplan.board_screen)
                                self.gameplan.sender.put_message("Move "+self.gameplan.pos_to_string(old_pos)+"-"+self.gameplan.pos_to_string(new_pos))
                                self.gameplan.pieces = move.make_move()
                                self.gameplan.history.append(self.gameplan.pieces)
                                self.gameplan.update_castling_info(old_pos, new_pos)
                                self.gameplan.moveLog.append((old_pos, new_pos))
                                self.gameplan.active_color, self.gameplan.non_active_color = self.gameplan.non_active_color, self.gameplan.active_color
                            to_move = False
                            valid_moves = self.gameplan.move_generator.generate_valid_moves()

                            if not self.gameplan.find_any_possible_move(valid_moves):
                                if self.gameplan.find_any_attacker():
                                    text = "black" if self.gameplan.active_color == "w" else "white"
                                    text += " won"
                                    self.gameplan.sender.put_message(text)
                                    break
                                else:
                                    self.gameplan.sender.put_message("tie")
                                    break
                            self.gameplan.draw_chessboard()
                            self.gameplan.draw_pieces()

                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_b and len(self.gameplan.history) > 2:
                                self.gameplan.undo_move()
                                self.gameplan.undo_move()

                        elif event.type == pygame.USEREVENT:
                            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                                if event.ui_element == undo_move and len(self.gameplan.history) > 2:
                                    self.gameplan.undo_move()
                                    self.gameplan.undo_move()
                        manager.process_events(event)
                        manager.update(time_delta)
                        manager.draw_ui(self.gameplan.board_screen)
                        pygame.display.flip()
                else:
                    depth = self.gameplan.depth + 2
                    bot_move = None
                    while bot_move is None and depth > 0:
                        depth -= 2
                        ai = AI(self.gameplan, depth)
                        ai.nega_max_alpha_beta(valid_moves, depth, -1 if player_color == "w" else 1, -10000, 10000)
                        bot_move = ai.get_next_move()
                    if bot_move is None:
                        break
                    if self.gameplan.check_move_correctness(bot_move[0], bot_move[1]):
                        fig = self.gameplan.pieces[bot_move[0]][5]
                        move_diff = (bot_move[1][0] - bot_move[0][0], bot_move[1][1] - bot_move[0][1])
                        if fig == "K" and move_diff == (0, 2):
                            if not self.gameplan.check_castling_availability("short"):
                                continue
                        if fig == "K" and move_diff == (0, -2):
                            if not self.gameplan.check_castling_availability("long"):
                                continue
                        move = Move(bot_move[0], bot_move[1], self.gameplan.pieces, self.gameplan.board_screen)
                        self.gameplan.sender.put_message("Move "+self.gameplan.pos_to_string(bot_move[0])+"-"+self.gameplan.pos_to_string(bot_move[1]))
                        move.set_non_player_move()
                        self.gameplan.pieces = move.make_move()
                        player_move_eval = AI(self.gameplan, 1)
                        self.gameplan.board_values_hist.append(player_move_eval.board_value(valid_moves))
                        if self.gameplan.board_values_hist[-2] - self.gameplan.board_values_hist[-1] > 1 and player_color == "w":
                            self.gameplan.sender.put_message("Would suggest to undo move")
                        elif self.gameplan.board_values_hist[-2] - self.gameplan.board_values_hist[-1] < -1 and player_color == "b":
                            self.gameplan.sender.put_message("Would suggest to undo move")
                        self.gameplan.history.append(self.gameplan.pieces)
                        self.gameplan.update_castling_info(bot_move[0], bot_move[1])
                        self.gameplan.moveLog.append((bot_move[0], bot_move[1]))
                        self.gameplan.active_color, self.gameplan.non_active_color = self.gameplan.non_active_color, self.gameplan.active_color
                    valid_moves = self.gameplan.move_generator.generate_valid_moves()
                    if not self.gameplan.find_any_possible_move(valid_moves):
                        if self.gameplan.find_any_attacker():
                            text = "black" if self.gameplan.active_color == "w" else "white"
                            text += " won"
                            self.gameplan.sender.put_message(text)
                            break
                        else:
                            self.gameplan.sender.put_message("tie")
                            break
                    self.gameplan.draw_chessboard()
                    self.gameplan.draw_pieces()
                pygame.display.flip()

            self.gameplan.draw_chessboard()
            self.gameplan.draw_pieces()
            while 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                pygame.display.flip()