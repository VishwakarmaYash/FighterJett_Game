import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
W, H = 1024, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fighter Jett (Pygame)")

# Colors
BG_COLOR = (230, 230, 230)
BULLET_COLOR = (255, 200, 0)

# Clock & font 
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load images
jet_img = pygame.image.load("jett2.png").convert_alpha()
jet_img = pygame.transform.scale(jet_img, (70, 70))

enemy_img = pygame.image.load("Enemy2.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

explosion_img = pygame.image.load("Blast2.png").convert_alpha()
explosion_img = pygame.transform.scale(explosion_img, (60, 60))

# Player (Jet)
jet_x = W // 2
jet_y = H - 100
jet_speed = 6

# Bullets
bullets = []
bullet_speed = 8

# Enemies
enemies = []
enemy_speed = 3
spawn_delay = 40
frame_count = 0

# Explosions
explosions = []

# Score
score = 0
game_over = False

# Game loop
running = True
while running:
    clock.tick(60)
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([jet_x, jet_y - 20])

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jet_x -= jet_speed
        if keys[pygame.K_RIGHT]:
            jet_x += jet_speed
        if keys[pygame.K_UP]:
            jet_y -= jet_speed
        if keys[pygame.K_DOWN]:
            jet_y += jet_speed

        # Keep player inside screen
        jet_x = max(35, min(W - 35, jet_x))
        jet_y = max(35, min(H - 35, jet_y))

        # Spawn enemies
        if frame_count % spawn_delay == 0:
            enemy_x = random.randint(50, W - 50)
            enemy_y = -20
            enemies.append([enemy_x, enemy_y])

        # Update bullets
        for b in bullets[:]:
            b[1] -= bullet_speed
            if b[1] < 0:
                bullets.remove(b)

        # Update enemies
        for e in enemies[:]:
            e[1] += enemy_speed
            if e[1] > H:
                enemies.remove(e)

        # Bullet-enemy collision
        for b in bullets[:]:
            for e in enemies[:]:
                if abs(b[0] - e[0]) < 30 and abs(b[1] - e[1]) < 30:
                    bullets.remove(b)
                    enemies.remove(e)
                    explosions.append([e[0], e[1], pygame.time.get_ticks()])
                    score += 10
                    break

        # --- Player-enemy collision (GAME OVER) ---
        jet_rect = jet_img.get_rect(center=(jet_x, jet_y))
        for e in enemies:
            enemy_rect = enemy_img.get_rect(center=(e[0], e[1]))
            if jet_rect.colliderect(enemy_rect):
                game_over = True
                explosions.append([jet_x, jet_y, pygame.time.get_ticks()])
                break

    # --- Drawing ---
    screen.fill(BG_COLOR)

    # Draw jet
    if not game_over:
        screen.blit(jet_img, (jet_x - 35, jet_y - 35))

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, (b[0] - 2, b[1], 4, 10))

    # Draw enemies
    for e in enemies:
        enemy_rect = enemy_img.get_rect(center=(e[0], e[1]))
        screen.blit(enemy_img, enemy_rect)

    # Draw explosions
    current_time = pygame.time.get_ticks()
    for ex in explosions[:]:
        if current_time - ex[2] < 300:  # explosion lasts 0.3 sec
            ex_rect = explosion_img.get_rect(center=(ex[0], ex[1]))
            screen.blit(explosion_img, ex_rect)
        else:
            explosions.remove(ex)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game Over screen
    if game_over:
        msg = font.render("💥 GAME OVER 💥", True, (255, 0, 0))
        score_msg = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 40))
        screen.blit(score_msg, (W // 2 - score_msg.get_width() // 2, H // 2 + 10))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        continue

    pygame.display.flip()

pygame.quit()
sys.exit()