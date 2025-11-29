import pygame
import random
import sys

# Creative Pygame Mini-Game: "Orbit Runner"
# You control a small comet orbiting a star. Avoid obstacles and survive as long as possible.

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Runner")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 230, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)

# Game objects
center = (WIDTH // 2, HEIGHT // 2)
angle = 0
radius = 150
player_speed = 0.03

obstacles = []
spawn_timer = 0
score = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= player_speed
    if keys[pygame.K_RIGHT]:
        angle += player_speed

    # Player position (orbiting)
    px = center[0] + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x
    py = center[1] + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
    player_pos = (int(px), int(py))

    # Spawn obstacles
    spawn_timer += 1
    if spawn_timer > 40:
        spawn_timer = 0
        # Random direction
        dir_angle = random.uniform(0, 360)
        speed = random.uniform(2, 4)
        vec = pygame.math.Vector2(1, 0).rotate(dir_angle)
        ox = center[0] + vec.x * 500
        oy = center[1] + vec.y * 500
        obstacles.append([ox, oy, vec * -speed])

    # Move obstacles
    for o in obstacles:
        o[0] += o[2].x
        o[1] += o[2].y

    # Collision detection
    for o in obstacles:
        if pygame.math.Vector2(o[0] - px, o[1] - py).length() < 20:
            running = False

    # Scoring
    score += 1

    # Drawing
    screen.fill(BLACK)

    # Draw star
    pygame.draw.circle(screen, YELLOW, center, 20)

    # Draw orbit circle
    pygame.draw.circle(screen, BLUE, center, radius, 1)

    # Draw player comet
    pygame.draw.circle(screen, WHITE, player_pos, 10)

    # Draw obstacles
    for o in obstacles:
        pygame.draw.circle(screen, RED, (int(o[0]), int(o[1])), 10)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

# Game Over Screen
screen.fill(BLACK)
game_over = font.render("Game Over!", True, RED)
final_score = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over, (WIDTH // 2 - 80, HEIGHT // 2 - 30))
screen.blit(final_score, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
pygame.display.update()
pygame.time.wait(3000)
