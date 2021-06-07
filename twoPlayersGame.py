import pygame_gui
import sys
from AI import *
from move import *
from MovesGenerator import *


class TwoPlayersGame:

    def __init__(self, gameplan):
        self.gameplay = gameplan

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

        valid_moves = self.gameplay.move_generator.generate_valid_moves()
        while 1:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and not to_move:
                    click_pos = pygame.mouse.get_pos()
                    old_pos = ((click_pos[1]) // self.gameplay.field_side, click_pos[0] // self.gameplay.field_side)
                    if old_pos in self.gameplay.pieces.keys() and self.gameplay.pieces.get(old_pos)[4] == self.gameplay.active_color:
                        pygame.draw.rect(self.gameplay.board_screen, (255, 255, 0),
                                         (old_pos[1] * self.gameplay.field_side, old_pos[0] * self.gameplay.field_side, self.gameplay.field_side,
                                          self.gameplay.field_side))
                        to_move = True

                        for moves in valid_moves:
                            if moves[0] == old_pos and self.gameplay.check_move_correctness(moves[0], moves[1]):
                                if (moves[1][0] % 2 == 0 and moves[1][1] % 2 != 0) or (moves[1][0] % 2 != 0 and
                                                                                       moves[1][1] % 2 == 0):
                                    pygame.draw.rect(self.gameplay.board_screen, (255, 255, 102),
                                                     (moves[1][1] * self.gameplay.field_side, moves[1][0] * self.gameplay.field_side,
                                                      self.gameplay.field_side, self.gameplay.field_side))
                                else:
                                    pygame.draw.rect(self.gameplay.board_screen, (255, 255, 204),
                                                     (moves[1][1] * self.gameplay.field_side, moves[1][0] * self.gameplay.field_side,
                                                      self.gameplay.field_side, self.gameplay.field_side))
                        self.gameplay.draw_pieces()

                elif event.type == pygame.MOUSEBUTTONUP and to_move:
                    click_pos = pygame.mouse.get_pos()
                    new_pos = ((click_pos[1]) // self.gameplay.field_side, click_pos[0] // self.gameplay.field_side)

                    if (old_pos, new_pos) in valid_moves and self.gameplay.check_move_correctness(old_pos, new_pos):
                        fig = self.gameplay.pieces[old_pos][5]
                        move_diff = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
                        if fig == "K" and move_diff == (0, 2):
                            if not self.gameplay.check_castling_availability("short"):
                                break
                        if fig == "K" and move_diff == (0, -2):
                            if not self.gameplay.check_castling_availability("long"):
                                break
                        move = Move(old_pos, new_pos, self.gameplay.pieces, self.gameplay.board_screen)
                        self.gameplay.sender.put_message("Move "+self.gameplay.pos_to_string(old_pos)+"-"+self.gameplay.pos_to_string(new_pos))
                        self.gameplay.pieces = move.make_move()
                        self.gameplay.history.append(self.gameplay.pieces)
                        self.gameplay.update_castling_info(old_pos, new_pos)
                        self.gameplay.moveLog.append((old_pos, new_pos))
                        self.gameplay.active_color, self.gameplay.non_active_color = self.gameplay.non_active_color, self.gameplay.active_color
                    to_move = False
                    valid_moves = self.gameplay.move_generator.generate_valid_moves()
                    if not self.gameplay.find_any_possible_move(valid_moves):
                        if self.gameplay.find_any_attacker():
                            text = "black" if self.gameplay.active_color == "w" else "white"
                            text += " won"
                            self.gameplay.sender.put_message(text)
                        else:
                            self.gameplay.sender.put_message("tie")
                    self.gameplay.draw_chessboard()
                    self.gameplay.draw_pieces()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and len(self.gameplay.history) > 1:
                        self.gameplay.undo_move()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == undo_move and len(self.gameplay.history) > 1:
                            self.gameplay.undo_move()
                manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(self.gameplay.board_screen)
            pygame.display.flip()