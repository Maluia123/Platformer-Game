import pygame
import sys

from Level_1 import main_1
from Level_2 import main_2
from victory import main_win

WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


if  __name__ == "__main__":
    main_1(window)
    main_2(window)
    main_win(window)


    pygame.quit()
    sys.exit()