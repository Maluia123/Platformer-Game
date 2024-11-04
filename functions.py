import pygame
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT = 1000, 800

PLAYER_VEL = 5

def flip(sprites):      #flip sprite so it can face the other way
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def load_sprite_sheet(dir1, dir2, dir3, width, height, direction=False):
    path = join("assets", dir1, dir2, dir3)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_grass_block(size):  #get the grassblock image to be loaded
    path = join("assets", "Terrain", "Grass Block.png  ")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_purpleGrass_block(size):    #get the grass block image to be loaded (but this time pink)
    path = join("assets", "Terrain", "Pink Grass Block.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_background(name):   #get the background image
    image = pygame.image.load(join("assets", "Background", name)).convert()
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(1920 // width + 1):                 #WIDTH replaced with 1920        #tile the image across the whole screen
        for j in range(1080 // height + 1):           #HEIGHT replaced with 1080
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def handle_vertical_collision(player, objects, dy): #veritcal collision
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects 

def collide(player, objects, dx):                   #horizontal collision
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
        

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left and player.healthbar.health > 0:      #move left if left arrow or a is pressed
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right and player.healthbar.health > 0:    #move right if right arrow or d is pressed
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "flame" or obj and obj.name == "blade" or obj and obj.name == "spikes":      #take damage when hit a trap
            player.make_hit()
            player.player_hit(1)
        
        from fruitclass import Fruit  
        if obj and obj.name == "fruit":     #heal when hit a fruit
            player.player_heal(1)
            Fruit.kill
        
        if obj and obj.name == "flag":      #level over when hit the flag
            player.finished = True
