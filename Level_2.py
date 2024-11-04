import pygame
import pygame.freetype
import time
from Traps import *
from os.path import join
from Traps import Blade
pygame.freetype.init()

pygame.display.set_caption("Platformer")
icon = pygame.image.load(join("assets", "Icons", "MaskDude_Icon.png"))
pygame.display.set_icon(icon)

FONT = pygame.freetype.Font("assets\Menu\Text\pixeloid-font\PixeloidMono-d94EV.ttf", 20)

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5 

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

from playerclass import Player
from objectclass import Object
from flagclass import Flag
from functions import get_purpleGrass_block, get_background, handle_move

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_purpleGrass_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def draw(window, background, bg_image, player, objects, offset, elapsed_time):
    for tile in background:             #draw background
        window.blit(bg_image, tile)

    for obj in objects:                 #draw objects
        obj.draw(window, offset)
        
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", "black")       #draw timer
    window.blit(time_text[0], (10, 60))
    
    player.draw(window, offset)             #draw player
    
    if player.healthbar.health <= 0:        #loss screen
        lost_text = FONT.render("You Lost!", "black")
        quit_text = FONT.render("press escape to quit", "black")
        restart_text = FONT.render("press R to restart", "black")     
        window.blit(lost_text[0], (WIDTH/2 - lost_text[0].get_width()/2, HEIGHT/2 - lost_text[0].get_height()/2))
        window.blit(quit_text[0], (WIDTH/2.35 - quit_text[0].get_width()/4, HEIGHT/1.85 - quit_text[0].get_height()/1.85))
        window.blit(restart_text[0], (WIDTH/2.25 - restart_text[0].get_width()/3.5, HEIGHT/1.7 - restart_text[0].get_height()/1.7))


    pygame.display.update()

def main_2(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")      #green background
    block_size = 96
    start_time = time.time()
    elapsed_time = 0


    player = Player(100, 704, 50, 50) #(x, y, width, height) x, y = spawn location
    trap = Blade(300, HEIGHT - block_size - 37, 38, 38) #(x, y, width, height)
    trap.on()
    trap2 = Blade(400, HEIGHT - block_size - 37, 38, 38) #(x, y, width, height)
    trap2.on()
    flag = Flag(block_size * 5, (HEIGHT - block_size) - 704, 64, 64) #(x, y, width, height)
    
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 1) // block_size)]

    objects = [trap, trap2, flag, *floor, Block(0, HEIGHT - block_size * 2, block_size), Block(0, HEIGHT - block_size * 3, block_size), Block(0, HEIGHT - block_size * 4, block_size),Block(0, HEIGHT - block_size * 5, block_size),  Block(0, HEIGHT - block_size * 6, block_size), Block(0, HEIGHT - block_size * 7, block_size), Block(0, HEIGHT - block_size * 8, block_size),Block(0, HEIGHT - block_size * 9, block_size),
               Block(block_size* 7, HEIGHT - block_size * 2, block_size), Block(block_size * 7, HEIGHT - block_size * 3, block_size), Block(block_size * 7, HEIGHT - block_size * 4, block_size),Block(block_size * 7, HEIGHT - block_size * 5, block_size),  Block(block_size * 7, HEIGHT - block_size * 6, block_size), Block(block_size * 7, HEIGHT - block_size * 7, block_size), Block(block_size * 7, HEIGHT - block_size * 8, block_size),Block(block_size * 7, HEIGHT - block_size * 9, block_size),
               Block(block_size* 6, HEIGHT - block_size * 2, block_size), Block(block_size, HEIGHT - block_size * 6, block_size), Block(block_size * 3, HEIGHT - block_size * 4, block_size), Block(block_size * 4, HEIGHT - block_size * 4, block_size), Block(block_size * 5, HEIGHT - block_size * 7, block_size)]
    #offset_x = 0
    offset = pygame.math.Vector2(0,0)
    scroll_area_width = 200     #how close to edge for scrolling background

    run = True
    while run:
        clock.tick(FPS)
        if player.healthbar.health > 0:
            elapsed_time = time.time() - start_time # seconds since while loop started
        else:
            start_time = time.time() - elapsed_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == player.hit_cooldown_event:
                pygame.time.set_timer(player.hit_cooldown_event, 0)
                player.hit_cooldown = False

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP) and player.jump_count < 2  and player.healthbar.health > 0:     # jump if W, space, or up arrow is pressed, double jump if already jumped
                    player.jump()

            if player.finished:
                run=False
                
            if player.rect.y > HEIGHT:  #if off window
                run = False
                main_2(window)          #reset level

            if player.healthbar.health <= 0:                #if dead
                if pygame.key.get_pressed()[pygame.K_r]:    #restart_level
                    main_2(window)
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:   #close window
                    run = False
               
            if player.x_vel < 0:                                                # scrolling background for both horizontal and vertical (doesn't work)
                if player.rect.left + offset.x < scroll_area_width:                 
                    offset.x += player.x_vel
            elif player.x_vel > 0:
                if player.rect.right + offset.x > WIDTH - scroll_area_width:
                    offset.x += player.x_vel
            if player.y_vel < 0:
                if player.rect.top + offset.y < scroll_area_width:
                    offset.y += player.x_vel
            elif player.y_vel > 0:
                if player.rect.bottom + offset.y > WIDTH - scroll_area_width:
                    offset.y += player.x_vel
        
        player.loop(FPS)
        trap.loop()
        trap2.loop()
        flag.loop()

        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset, elapsed_time)
        

    '''
        if ((player.rect.top - offset_x >= HEIGHT - scroll_area_width) and player.y_vel > 0) or (      #scrolling background
                (player.rect.bottom - offset_x <= scroll_area_width) and player.y_vel < 0):
            offset_x += player.y_vel'''
    


if __name__ == "__main__":
    main_2(window)