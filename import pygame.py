import pygame
from pygame import mixer
import os
from fighter import Fighter

# Initialize pygame and mixer
mixer.init()
pygame.init()

# Helper function to safely load assets
def load_asset(path, error_message="File not found: "):
    if not os.path.exists(path):
        raise FileNotFoundError(error_message + path)
    return path

# Game setup constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Initialize font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Initialize game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Fighter setup constants
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 120]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 150]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load assets
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Function to draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function to draw fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Function for countdown before the round starts
def count_down():
    global intro_count
    global last_count_update
    global round_over
    if intro_count <= 0:
        return True
    else:
        time_now = pygame.time.get_ticks()
        if time_now - last_count_update >= 1000:
            last_count_update = time_now
            intro_count -= 1
        draw_text(str(intro_count), count_font, YELLOW, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 3)
        return False

# Main menu function
def main_menu():
    while True:
        screen.fill((0, 0, 0))
        draw_text("Press 'Enter' to Start", count_font, YELLOW, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 3)
        draw_text("Press 'Escape' to Quit", count_font, YELLOW, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Start the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Start the game with the main menu
main_menu()

# Initialize fighters
warrior = Fighter(1, 50, SCREEN_HEIGHT - WARRIOR_SIZE, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
wizard = Fighter(2, SCREEN_WIDTH - WIZARD_SIZE - 50, SCREEN_HEIGHT - WIZARD_SIZE, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Main game loop
while True:
    draw_bg()
    warrior.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, wizard, round_over)
    wizard.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, warrior, round_over)
    warrior.update()
    wizard.update()
    warrior.draw(screen)
    wizard.draw(screen)

    round_over = count_down()
    pygame.display.update()
    clock.tick(FPS)
