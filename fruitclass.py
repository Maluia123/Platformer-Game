import pygame
from objectclass import Object
from functions import load_sprite_sheets


class Fruit(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fruit")
        self.fruit = load_sprite_sheets("Items", "Fruits", width, height, False)
        self.image = self.fruit["Strawberry"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Strawberry"
        self.killed = False
   
    def idle(self):
        self.animation_name = "Strawberry"

    def loop(self):
        sprites = self.fruit[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        
        if self.killed ==True:
            #something probably
            
            
            pass

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0