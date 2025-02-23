import pygame
import math
import random

   
#Initialisation
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Keep Running")
clock = pygame.time.Clock()
fps = 60

#Design stuff
font = pygame.font.SysFont('Courier New', 30, bold=True)
player_colour = (17, 59, 122)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

game_state = "start_menu"

def draw_start_menu():
    screen.fill(WHITE)
    title = font.render("Keep Running", True, BLUE)
    start_button = font.render("Press SPACE to start", True, BLUE)
    screen.blit(title, (screen_width//2 - title.get_width()//2, screen_height//2 - 50))
    screen.blit(start_button, (screen_width//2 - start_button.get_width()//2, screen_height//2 + 50))
    pygame.display.update()
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
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Enemy:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx /= distance
            dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def no_collision(self, other):
        if self.get_rect().colliderect(other.get_rect()):
            dx = self.x - other.x
            dy = self.y - other.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance == 0:
                distance = 0.1
            
            overlap = self.size - distance
            dx /= distance
            dy /= distance
            self.x += dx * overlap / 2
            self.y += dy * overlap / 2
            other.x -= dx * overlap / 2
            other.y -= dy * overlap / 2


def reset_game():
    global player, enemies, game_over
    player = Player(x = screen_width//2, y = screen_height//2, size=20, color= player_colour, speed = 5)
    enemies = [
        Enemy(x = random.randint(0, screen_width), y = random.randint(0, screen_height), size = 20, color = RED, speed = 4), 
        Enemy(x = random.randint(0, screen_width), y = random.randint(0, screen_height), size = 20, color = RED, speed = 4),
    ]
    game_over = False

reset_game()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()

    if game_state == "start_menu":
        draw_start_menu()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
    elif game_state == "playing":
        if game_over:
            if keys[pygame.K_r]:
                reset_game()
        else:
            player.move(keys)
            player.update(screen_width, screen_height)
            for enemy in enemies:
                enemy.move(player)
            for i in range(len(enemies)):
                for j in range(i + 1, len(enemies)):
                    enemies[i].no_collision(enemies[j])
            for enemy in enemies:
                if player.get_rect().colliderect(enemy.get_rect()):
                    game_over = True
                    break

        screen.fill(WHITE)

        if game_over:
            game_over_text = font.render("GAME OVER", True, BLUE)
            restart_text = font.render("PRESS R TO RESTART", True, BLUE)
            screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2-50))
            screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2+20))

        else:
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
