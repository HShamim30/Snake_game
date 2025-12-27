import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# ================== CONFIG ==================
WIDTH, HEIGHT = 900, 700
BLOCK = 20
BORDER = 60

GAME_WIDTH = WIDTH - 2 * BORDER
GAME_HEIGHT = HEIGHT - 2 * BORDER

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake – Arcade Levels")
clock = pygame.time.Clock()

# ================== FILES ==================
EAT_SOUND = "eat.wav"
GAMEOVER_SOUND = "gameover.wav"
HIGHSCORE_FILE = "highscore.txt"

eat_sound = pygame.mixer.Sound(EAT_SOUND) if os.path.exists(EAT_SOUND) else None
gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND) if os.path.exists(GAMEOVER_SOUND) else None

if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write("0")
with open(HIGHSCORE_FILE, "r") as f:
    high_score = int(f.read())

# ================== COLORS ==================
BG_TOP = (25, 30, 40)
BG_BOTTOM = (10, 15, 20)
GAME_BG = (18, 22, 28)
GRID_COLOR = (60, 70, 80)
SNAKE_HEAD = (90, 200, 120)
SNAKE_BODY = (60, 160, 90)
FOOD_RED = (200, 60, 60)
OBSTACLE_COLOR = (120, 120, 120)
WHITE = (240, 240, 240)

# ================== FONTS ==================
font_title = pygame.font.SysFont("arial", 44, bold=True)
font_big = pygame.font.SysFont("arial", 30, bold=True)
font_med = pygame.font.SysFont("arial", 22)
font_small = pygame.font.SysFont("arial", 14)

# ================== HELPERS ==================
def gradient_bg():
    for y in range(HEIGHT):
        r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT
        g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT
        b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def draw_shadow_rect(x, y, w, h):
    shadow = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=6)
    screen.blit(shadow, (x + 2, y + 3))

def random_cell():
    return [
        BORDER + random.randrange(0, GAME_WIDTH, BLOCK),
        BORDER + random.randrange(0, GAME_HEIGHT, BLOCK)
    ]

# ================== LEVELS / MAZE ==================
def generate_maze(level):
    """
    Simple maze-style obstacles.
    Level 1: few blocks
    Each next level: more blocks + patterns
    """
    obstacles = []

    # Vertical bars
    for i in range(level + 1):
        x = BORDER + (i + 2) * 4 * BLOCK
        for y in range(BORDER + BLOCK, HEIGHT - BORDER - BLOCK, BLOCK):
            if random.random() < 0.25:
                obstacles.append([x, y])

    # Horizontal bars
    for i in range(level):
        y = BORDER + (i + 2) * 4 * BLOCK
        for x in range(BORDER + BLOCK, WIDTH - BORDER - BLOCK, BLOCK):
            if random.random() < 0.25:
                obstacles.append([x, y])

    # Remove duplicates
    uniq = []
    for ob in obstacles:
        if ob not in uniq:
            uniq.append(ob)
    return uniq

# ================== GAME ==================
def game():
    global high_score

    # Snake
    x = BORDER + GAME_WIDTH // 2
    y = BORDER + GAME_HEIGHT // 2
    dx = dy = 0
    snake = [[x, y]]
    length = 1

    # Level system
    level = 1
    level_target = 5  # foods to eat to next level
    foods_eaten = 0

    obstacles = generate_maze(level)

    # Food
    foodx, foody = random_cell()

    score = 0
    speed_delay = 140
    last_move = pygame.time.get_ticks()

    started = False
    paused = False
    game_over = False
    gameover_played = False

    while True:
        clock.tick(60)
        gradient_bg()

        # Game area
        pygame.draw.rect(
            screen, GAME_BG,
            pygame.Rect(BORDER, BORDER, GAME_WIDTH, GAME_HEIGHT),
            border_radius=18
        )

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
            draw_text("PAUSED", font_big, WHITE, WIDTH//2 - 50, HEIGHT//2)
            pygame.display.update()
            continue

        # Movement (time-based)
        now = pygame.time.get_ticks()
        if started and not game_over and now - last_move > speed_delay:
            last_move = now
            x += dx
            y += dy

            # Wrap-around world
            if x < BORDER: x = WIDTH - BORDER - BLOCK
            elif x >= WIDTH - BORDER: x = BORDER
            if y < BORDER: y = HEIGHT - BORDER - BLOCK
            elif y >= HEIGHT - BORDER: y = BORDER

            head = [x, y]
            snake.append(head)
            if len(snake) > length:
                snake.pop(0)

            # Self collision
            for part in snake[:-1]:
                if part == head:
                    game_over = True

            # Obstacle collision (RECT BASED)
            snake_rect = pygame.Rect(x, y, BLOCK, BLOCK)
            for ob in obstacles:
                if snake_rect.colliderect(pygame.Rect(ob[0], ob[1], BLOCK, BLOCK)):
                    game_over = True

            # Food collision
            if snake_rect.colliderect(pygame.Rect(foodx, foody, BLOCK, BLOCK)):
                if eat_sound:
                    eat_sound.play()
                foods_eaten += 1
                score += 10
                length += 1
                speed_delay = max(speed_delay - 3, 70)

                # Level up
                if foods_eaten >= level_target:
                    level += 1
                    foods_eaten = 0
                    obstacles = generate_maze(level)

                # New food (avoid snake & obstacles)
                while True:
                    foodx, foody = random_cell()
                    if [foodx, foody] not in snake and [foodx, foody] not in obstacles:
                        break

        # Draw food
        draw_shadow_rect(foodx, foody, BLOCK, BLOCK)
        pygame.draw.circle(screen, FOOD_RED,
                           (foodx + BLOCK//2, foody + BLOCK//2),
                           BLOCK//2)

        # Draw obstacles
        for ob in obstacles:
            draw_shadow_rect(ob[0], ob[1], BLOCK, BLOCK)
            pygame.draw.rect(screen, OBSTACLE_COLOR,
                             (ob[0], ob[1], BLOCK, BLOCK), border_radius=5)

        # Draw snake
        for i, part in enumerate(snake):
            draw_shadow_rect(part[0], part[1], BLOCK, BLOCK)
            color = SNAKE_HEAD if i == len(snake) - 1 else SNAKE_BODY
            pygame.draw.rect(screen, color,
                             (part[0], part[1], BLOCK, BLOCK), border_radius=6)

        # HUD
        hud = pygame.Surface((260, 80), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 160))
        screen.blit(hud, (BORDER + 12, BORDER + 12))
        draw_text(f"Score : {score}", font_med, WHITE, BORDER + 24, BORDER + 18)
        draw_text(f"Level : {level}", font_small, WHITE, BORDER + 24, BORDER + 38)
        draw_text(f"High  : {high_score}", font_small, WHITE, BORDER + 24, BORDER + 56)

        # Start / Game Over
        if not started:
            draw_text("ARCADE SNAKE – LEVELS", font_title, WHITE,
                      WIDTH//2 - 260, HEIGHT//2 - 40)
            draw_text("Arrow Keys to Start", font_med, WHITE,
                      WIDTH//2 - 120, HEIGHT//2 + 20)

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

# ================== RUN ==================
game()
