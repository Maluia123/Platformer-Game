import pygame
import pygame.freetype
from os.path import join
from Level_1 import main_1
pygame.freetype.init()

from functions import get_background


pygame.display.set_caption("Platformer")
icon = pygame.image.load(join("assets", "Icons", "MaskDude_Icon.png"))
pygame.display.set_icon(icon)

FONT = pygame.freetype.Font("assets\Menu\Text\pixeloid-font\PixeloidMono-d94EV.ttf", 20)

WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


def draw(window, background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)

    win_text = FONT.render("Victory!", "black")
    quit_text = FONT.render("Press Escape to Quit", "black")
    restart_text = FONT.render("Press R to Restart", "black")
    window.blit(win_text[0], (WIDTH/2 - win_text[0].get_width()/2, HEIGHT/2 - win_text[0].get_height()/2))
    window.blit(quit_text[0], (WIDTH/2.35 - quit_text[0].get_width()/4, HEIGHT/1.85 - quit_text[0].get_height()/1.85))
    window.blit(restart_text[0], (WIDTH/2.25 - restart_text[0].get_width()/3.5, HEIGHT/1.7 - restart_text[0].get_height()/1.7))    
    pygame.display.update()

def main_win(window):
    background, bg_image = get_background("Blue.png")


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if pygame.key.get_pressed()[pygame.K_r]:
                #restart_game
                main_1(window)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                #close window
                run = False
        draw(window, background, bg_image)