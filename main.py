import pygame
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Keep Running")
clock = pygame.time.Clock()
fps = 60

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

player_colour = (150, 200, 200)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    def update(self, screen_width, screen_height):
        self.x = max(0, min(self.x, screen_width - self.size))
        self.y = max(0, min(self.y, screen_height - self.size))

player = Player(x = screen_width//2, y = screen_height//2, size=20, color= player_colour, speed = 5)

'''
enemy_pos = [100, 100]
enemy_speed = 3
enemy_size = 20
'''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.update(screen_width, screen_height)

    '''
    dx = player_pos[0] - enemy_pos[0]
    dy = player_pos[1] - enemy_pos[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance != 0:
        dx /= distance
        dy /= distance

    enemy_pos[0] += dx * enemy_speed
    enemy_pos[1] += dy * enemy_speed
    '''

    screen.blit(background, (0, 0))
    player.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
