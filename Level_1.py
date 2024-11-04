import pygame
import pygame.freetype
import time
from Traps import *
from os.path import join
pygame.freetype.init()

pygame.display.set_caption("Platformer")
icon = pygame.image.load(join("assets", "Icons", "MaskDude_Icon.png"))
pygame.display.set_icon(icon)

FONT = pygame.freetype.Font("assets\Menu\Text\pixeloid-font\PixeloidMono-d94EV.ttf", 20)


WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
StartGame = False

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

from playerclass import Player
from objectclass import Object
from flagclass import Flag
from fruitclass import Fruit
from functions import get_grass_block, get_background, handle_move


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_grass_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def draw(window, background, bg_image, player, objects, offset_x, elapsed_time):
    for tile in background:             #draw background
        window.blit(bg_image, tile)

    for obj in objects:                 #draw objects
        obj.draw(window, offset_x)
    
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", "black")       #draw timer
    window.blit(time_text[0], (10, 60))
    
    player.draw(window, offset_x)             #draw player
    
    if player.healthbar.health <= 0:        #loss screen
        lost_text = FONT.render("You Lost!", "black")
        quit_text = FONT.render("press escape to quit", "black")
        restart_text = FONT.render("press R to restart", "black")
        window.blit(lost_text[0], (WIDTH/2 - lost_text[0].get_width()/2, HEIGHT/2 - lost_text[0].get_height()/2))
        window.blit(quit_text[0], (WIDTH/2.35 - quit_text[0].get_width()/4, HEIGHT/1.85 - quit_text[0].get_height()/1.85))
        window.blit(restart_text[0], (WIDTH/2.25 - restart_text[0].get_width()/3.5, HEIGHT/1.7 - restart_text[0].get_height()/1.7))

    pygame.display.update()



def main_1(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    block_size = 96
    start_time = time.time()
    elapsed_time = 0


    player = Player(100, 650, 50, 50) #(x, y, width, height) x, y = spawn location
    trap = Flame(block_size * 3.15, HEIGHT - (block_size * 3) - 64, 16, 32) #(x, y, width, height)
    trap.on()
    trap2 = Flame(block_size* 6.75, HEIGHT - (block_size * 1.65), 16, 32) #(x, y, width, height)
    trap2.on()
    
    trap3 = Spikes(block_size* 3, HEIGHT - (block_size * 1.33), 16, 16) #(x, y, width, height)
    trap3.Idle()
    trap4 = Spikes(block_size* 3.33, HEIGHT - (block_size * 1.33), 16, 16) #(x, y, width, height)
    trap4.Idle()
    trap5 = Spikes(block_size* 3.66, HEIGHT - (block_size * 1.33), 16, 16) #(x, y, width, height)
    trap5.Idle()
    trap6 = Spikes(block_size* 4, HEIGHT - (block_size * 1.33), 16, 16) #(x, y, width, height)
    trap6.Idle()
    trap7 = Spikes(block_size* 4.33, HEIGHT - (block_size * 1.33), 16, 16) #(x, y, width, height)
    trap7.Idle()
    trap8 = Spikes(block_size* 4.66, HEIGHT - (block_size * 1.33), 16, 16) #(x, y, width, height)
    trap8.Idle()
    
    
    
    flag = Flag(block_size * 30, (HEIGHT - block_size) - 127, 64, 64) #(x, y, width, height)
    fruit = Fruit(block_size * 9, (HEIGHT - block_size) - 350, 32, 32) #(x, y, width, height))
    fruit2 = Fruit(block_size * 17.15, (HEIGHT - block_size) - 550, 32, 32) #(x, y, width, height))
    
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 3) // block_size)]

    objects = [*floor, 
               Block(0, HEIGHT - block_size * 2, block_size), Block(0, HEIGHT - block_size * 3, block_size), Block(0, HEIGHT - block_size * 4, block_size), Block(0, HEIGHT - block_size * 5, block_size), Block(0, HEIGHT - block_size * 6, block_size),
               Block(block_size * 2, HEIGHT - block_size * 3, block_size), Block(block_size * 3, HEIGHT - block_size * 3, block_size),  Block(block_size * 4, HEIGHT - block_size * 3, block_size),  Block(block_size * 5, HEIGHT - block_size * 3, block_size),
               Block(block_size * 8, HEIGHT - block_size * 4, block_size), Block(block_size * 9, HEIGHT - block_size * 4, block_size), Block(block_size * 10, HEIGHT - block_size * 4, block_size), 
               Block(block_size * 14, HEIGHT - block_size * 2, block_size), Block(block_size * 15, HEIGHT - block_size * 4, block_size), Block(block_size * 16, HEIGHT - block_size * 5, block_size),  Block(block_size * 17, HEIGHT - block_size * 6, block_size), 
               trap, trap2, flag, fruit, fruit2,
               trap3, trap4, trap5, trap6, trap7, trap8]

    offset_x = 0
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
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP) and player.jump_count < 2  and player.healthbar.health > 0: # jump if W, space, or up arrow is pressed, double jump if already jumped
                    player.jump()

            if player.finished:
                run = False

            if player.rect.y > HEIGHT:  #if off window
                run = False
                main_1(window)          #reset level


            if player.healthbar.health <= 0:                #if dead
                if pygame.key.get_pressed()[pygame.K_r]:    #restart_level
                    main_1(window)
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:   #close window
                    run = False


        player.loop(FPS)
        trap.loop()
        trap2.loop()
        flag.loop()
        fruit.loop()
        fruit2.loop()

        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, elapsed_time)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (      #scrolling background
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel


if __name__ == "__main__":
    main_1(window)