from time import sleep
import pygame


class Sender:

    def __init__(self, board_screen):
        self.board_screen = board_screen

    def put_message(self, text):
        """ Wypisz na ekranie komunikat podany jako parametr text """
        font = pygame.font.SysFont('Lucida Console', 14)
        img = font.render(text, True, '#cdcdcb')
        self.board_screen.blit(img, (500, 340))
        pygame.display.flip()
        sleep(1)
        pygame.draw.rect(self.board_screen, '#1a1a19', pygame.Rect(500, 340, 250, 20))