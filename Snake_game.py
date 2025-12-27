import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 900, 700
BLOCK = 20
BORDER = 60
GAME_WIDTH = WIDTH - 2 * BORDER
GAME_HEIGHT = HEIGHT - 2 * BORDER

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game - Premium Edition")
clock = pygame.time.Clock()

# ---------------- FILES ----------------
EAT_SOUND = "eat.wav"
GAMEOVER_SOUND = "gameover.wav"
HIGHSCORE_FILE = "highscore.txt"

# Load sounds safely
eat_sound = pygame.mixer.Sound(EAT_SOUND) if os.path.exists(EAT_SOUND) else None
gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND) if os.path.exists(GAMEOVER_SOUND) else None

# High score load
if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write("0")

with open(HIGHSCORE_FILE, "r") as f:
    high_score = int(f.read())

# ---------------- COLORS ----------------
BG_TOP = (10, 15, 25)
BG_BOTTOM = (25, 35, 50)
GAME_BG = (15, 20, 30)
GRID_COLOR = (30, 40, 55)
SNAKE_HEAD = (120, 255, 120)
SNAKE_BODY = (60, 180, 60)
FOOD_RED = (255, 60, 60)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
NEON = (0, 200, 255)

# ---------------- FONTS ----------------
font_title = pygame.font.SysFont("arial", 48, bold=True)
font_big = pygame.font.SysFont("arial", 34, bold=True)
font_med = pygame.font.SysFont("arial", 22, bold=True)
font_small = pygame.font.SysFont("arial", 14)

# ---------------- HELPERS ----------------
def gradient_bg():
    for y in range(HEIGHT):
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def glow_rect(surface, color, rect, radius=15, glow=6):
    for i in range(glow, 0, -1):
        s = pygame.Surface((rect.width + i*2, rect.height + i*2), pygame.SRCALPHA)
        pygame.draw.rect(s, (*color, 30), s.get_rect(), border_radius=radius+i)
        surface.blit(s, (rect.x - i, rect.y - i))
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_text(txt, font, color, x, y):
    screen.blit(font.render(txt, True, color), (x, y))

# ---------------- GAME ----------------
def game():
    global high_score

    x = BORDER + GAME_WIDTH // 2
    y = BORDER + GAME_HEIGHT // 2
    dx = dy = 0

    snake = [[x, y]]
    length = 1

    foodx = BORDER + random.randrange(0, GAME_WIDTH, BLOCK)
    foody = BORDER + random.randrange(0, GAME_HEIGHT, BLOCK)

    score = 0
    speed_delay = 140
    last_move = pygame.time.get_ticks()

    started = False
    paused = False
    game_over = False
    pulse = 0
    gameover_played = False

    while True:
        clock.tick(60)
        pulse += 0.1

        # Background
        gradient_bg()
        game_rect = pygame.Rect(BORDER, BORDER, GAME_WIDTH, GAME_HEIGHT)
        glow_rect(screen, NEON, game_rect, 18, 8)
        pygame.draw.rect(screen, GAME_BG, game_rect, border_radius=15)

        # Grid
        for gx in range(BORDER, WIDTH - BORDER, BLOCK):
            pygame.draw.line(screen, GRID_COLOR, (gx, BORDER), (gx, HEIGHT - BORDER))
        for gy in range(BORDER, HEIGHT - BORDER, BLOCK):
            pygame.draw.line(screen, GRID_COLOR, (BORDER, gy), (WIDTH - BORDER, gy))

        # Events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p and started:
                    paused = not paused

                if not paused and not game_over:
                    if e.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -BLOCK, 0; started = True
                    elif e.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = BLOCK, 0; started = True
                    elif e.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -BLOCK; started = True
                    elif e.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, BLOCK; started = True

                if game_over and e.key == pygame.K_r:
                    return game()

        if paused:
            draw_text("PAUSED", font_big, NEON, WIDTH//2 - 70, HEIGHT//2)
            pygame.display.update()
            continue

        # Movement
        now = pygame.time.get_ticks()
        if started and not game_over and now - last_move > speed_delay:
            last_move = now
            x += dx
            y += dy

            if x < BORDER or x >= WIDTH - BORDER or y < BORDER or y >= HEIGHT - BORDER:
                game_over = True

            head = [x, y]
            snake.append(head)
            if len(snake) > length:
                snake.pop(0)

            for part in snake[:-1]:
                if part == head:
                    game_over = True

            # Food collision
            if pygame.Rect(x, y, BLOCK, BLOCK).colliderect(
               pygame.Rect(foodx, foody, BLOCK, BLOCK)):
                if eat_sound:
                    eat_sound.play()

                while True:
                    foodx = BORDER + random.randrange(0, GAME_WIDTH, BLOCK)
                    foody = BORDER + random.randrange(0, GAME_HEIGHT, BLOCK)
                    if [foodx, foody] not in snake:
                        break

                length += 1
                score += 10
                speed_delay = max(speed_delay - 6, 60)

        # Food draw
        glow = int(5 + 3 * math.sin(pulse))
        food_glow = pygame.Surface((BLOCK + glow*2, BLOCK + glow*2), pygame.SRCALPHA)
        pygame.draw.circle(food_glow, (*FOOD_RED, 120),
                           (BLOCK//2 + glow, BLOCK//2 + glow),
                           BLOCK//2 + glow)
        screen.blit(food_glow, (foodx - glow, foody - glow))
        pygame.draw.rect(screen, FOOD_RED, (foodx, foody, BLOCK, BLOCK), border_radius=6)

        # Snake draw
        for i, part in enumerate(snake):
            color = SNAKE_HEAD if i == len(snake) - 1 else SNAKE_BODY
            pygame.draw.rect(screen, color,
                             (part[0], part[1], BLOCK, BLOCK), border_radius=5)

        # HUD INSIDE GAME BOX
        hud = pygame.Surface((220, 65), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 160))
        screen.blit(hud, (BORDER + 10, BORDER + 10))

        draw_text(f"Score : {score}", font_med, GOLD, BORDER + 20, BORDER + 18)
        draw_text(f"High  : {high_score}", font_small, WHITE, BORDER + 20, BORDER + 38)
        draw_text(f"Length: {length}", font_small, WHITE, BORDER + 20, BORDER + 54)

        # Start / Game Over
        if not started:
            draw_text("🐍 SNAKE PREMIUM", font_title, NEON,
                      WIDTH//2 - 220, HEIGHT//2 - 40)
            draw_text("Press Arrow Keys to Start", font_med, WHITE,
                      WIDTH//2 - 150, HEIGHT//2 + 20)

        if game_over:
            if not gameover_played:
                if gameover_sound:
                    gameover_sound.play()
                gameover_played = True

            if score > high_score:
                high_score = score
                with open(HIGHSCORE_FILE, "w") as f:
                    f.write(str(high_score))

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            draw_text("GAME OVER", font_big, FOOD_RED,
                      WIDTH//2 - 90, HEIGHT//2 - 20)
            draw_text("Press R to Restart", font_med, WHITE,
                      WIDTH//2 - 110, HEIGHT//2 + 30)

        pygame.display.update()

game()
