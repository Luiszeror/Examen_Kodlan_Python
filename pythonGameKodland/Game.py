import pygame
import random
import sys

pygame.init()

# pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defiende el Puente")

# colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# imágenes
background_img = pygame.image.load("background.jpg")
weapon_img = pygame.image.load("weapon.png")
monster_img = pygame.image.load("monster.png")
heart_img = pygame.image.load("heart.png")

# escala de imágenes
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
weapon_img = pygame.transform.scale(weapon_img, (120, 120))
monster_img = pygame.transform.scale(monster_img, (50, 50))
heart_img = pygame.transform.scale(heart_img, (30, 30))

# sonidos
shoot_sound = pygame.mixer.Sound("shoot.mp3")
hit_sound = pygame.mixer.Sound("mosnter.mp3")

# fuente txto
font = pygame.font.Font(None, 36)

# puntajes
high_scores = []



def draw_text(text, x, y, color=WHITE, center=True):
    text_surface = font.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
    screen.blit(text_surface, (x, y))


# botoness
def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, RED if x < mouse[0] < x + width and y < mouse[1] < y + height else GRAY,
                     (x, y, width, height))
    draw_text(text, x + width // 2, y + 10)

    if x < mouse[0] < x + width and y < mouse[1] < y + height and click[0] == 1:
        if action:
            action()


# Puntajes
def show_high_scores():
    while True:
        screen.blit(background_img, (0, 0))
        draw_text("Puntajes Más Altos", WIDTH // 2, HEIGHT // 4)
        for i, score in enumerate(high_scores[:5]):
            draw_text(f"{i + 1}. {score}", WIDTH // 2, HEIGHT // 3 + i * 40)
        draw_button("Volver", WIDTH // 2 - 75, HEIGHT - 100, 150, 40, retry_screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Menú principal
def main_menu():
    while True:
        screen.blit(background_img, (0, 0))
        draw_text("Defiende el Puente", WIDTH // 2, HEIGHT // 4)
        draw_button("Jugar", WIDTH // 2 - 75, HEIGHT // 2 - 70, 150, 40, game_loop)
        draw_button("Puntajes", WIDTH // 2 - 75, HEIGHT // 2 - 10, 150, 40, show_high_scores)
        draw_button("Salir", WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 40, quit_game)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Juego
def game_loop():
    global lives, score, high_scores
    running = True
    bullets = []
    monsters = []
    weapon_x = WIDTH // 2
    lives = 3
    score = 0

    while running:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append([weapon_x + 60, HEIGHT - 150])
                shoot_sound.play()

        weapon_x, _ = pygame.mouse.get_pos()
        weapon_x = max(0, min(WIDTH - 120, weapon_x))

        for i in range(lives):
            screen.blit(heart_img, (10 + i * 40, 10))

        draw_text(f"Puntaje: {score}", WIDTH - 100, 10)

        for bullet in bullets:
            bullet[1] -= 5
            pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], 5, 10))

        bullets = [b for b in bullets if b[1] > 0]

        if random.randint(1, 60) == 1:
            monsters.append([random.randint(50, WIDTH - 50), 0])

        for monster in monsters[:]:
            monster[1] += 2
            screen.blit(monster_img, (monster[0], monster[1]))

            if monster[1] > HEIGHT:
                monsters.remove(monster)
                lives -= 1
                hit_sound.play()
                if lives == 0:
                    running = False

        for bullet in bullets[:]:
            for monster in monsters[:]:
                if monster[0] < bullet[0] < monster[0] + 50 and monster[1] < bullet[1] < monster[1] + 50:
                    monsters.remove(monster)
                    bullets.remove(bullet)
                    score += 10
                    break

        screen.blit(weapon_img, (weapon_x, HEIGHT - 150))
        pygame.display.flip()
        pygame.time.delay(30)

    high_scores.append(score)
    high_scores.sort(reverse=True)
    retry_screen()


# Menu de reintentar
def retry_screen():
    while True:
        screen.blit(background_img, (0, 0))
        draw_text("Has perdido", WIDTH // 2, HEIGHT // 4, RED)
        draw_button("Ver Puntajes", WIDTH // 2 - 100, HEIGHT // 2 - 90, 200, 40, show_high_scores)
        draw_button("Reintentar", WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 40, game_loop)
        draw_button("Salir", WIDTH // 2 - 75, HEIGHT // 2 + 30, 150, 40, quit_game)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def quit_game():
    pygame.quit()
    sys.exit()



main_menu()