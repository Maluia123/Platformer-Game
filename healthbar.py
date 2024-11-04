import pygame
pygame.font.init()


WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

vec = pygame.math.Vector2
HITPOINTS = 3 #how many hitpoints the player spawns with. Max 5 (how many sprites I have)

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animations()


        self.health = HITPOINTS
        self.image = self.health_animations[self.health] 
        self.pos = vec(x,y)

    def render(self, display):
        display.blit(self.image, self.pos)
    
    
    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0: self.health = 0

        self.image = self.health_animations[self.health]
 

    def heal(self, heal):
        self.health += heal
        if self.health > HITPOINTS: self.health = HITPOINTS

        self.image = self.health_animations[self.health]
        pygame
    
    def load_animations(self):
        self.health_animations = [pygame.image.load("assets/Hearts/heart0.png").convert_alpha(),
                                  pygame.image.load("assets/Hearts/heart1.png").convert_alpha(),
                                  pygame.image.load("assets/Hearts/heart2.png").convert_alpha(),
                                  pygame.image.load("assets/Hearts/heart3.png").convert_alpha(),
                                  pygame.image.load("assets/Hearts/heart4.png").convert_alpha(),
                                  pygame.image.load("assets/Hearts/heart5.png").convert_alpha()]