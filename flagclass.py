import pygame
from objectclass import Object
from functions import load_sprite_sheet


class Flag(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "flag")
        self.flag = load_sprite_sheet("Items", "Checkpoints", "checkpoint", width, height, False)
        self.image = self.flag["FlagIdle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "FlagIdle"
   
    def idle(self):
        self.animation_name = "FlagIdle"


    def loop(self):
        sprites = self.flag[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0