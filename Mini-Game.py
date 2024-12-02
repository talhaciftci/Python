import pygame
import random
import sys

# Pygame başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zamanda Yolculuk Arenası")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# FPS ve Saat
clock = pygame.time.Clock()
FPS = 60

# Oyuncu özellikleri
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Enerji çubuğu
energy = 100

# Portal ve düşman ayarları
portal_width = 60
portal_height = 60
enemy_width = 50
enemy_height = 50

portals = []
enemies = []
enemy_speed = 3

# Oyun durumları
running = True
score = 0

# Fontlar
font = pygame.font.SysFont("Arial", 25)

# Rastgele portal oluştur
def create_portal():
    x = random.randint(0, SCREEN_WIDTH - portal_width)
    y = random.randint(50, SCREEN_HEIGHT // 2)
    return pygame.Rect(x, y, portal_width, portal_height)

# Rastgele düşman oluştur
def create_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_width)
    y = random.randint(-100, -40)
    return pygame.Rect(x, y, enemy_width, enemy_height)

# Oyuncu çiz
def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

# Enerji çubuğunu çiz
def draw_energy_bar(energy):
    pygame.draw.rect(screen, RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, 2 * energy, 20))

# Skoru çiz
def draw_score(score):
    score_text = font.render(f"Skor: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

# Ana oyun döngüsü
while running:
    screen.fill(BLACK)
    
    # Olayları kontrol et
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Tuş kontrolleri
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_height:
        player_y += player_speed

    # Portal ve düşman oluştur
    if random.randint(1, 100) > 98 and len(portals) < 3:
        portals.append(create_portal())
    
    if random.randint(1, 100) > 95:
        enemies.append(create_enemy())
    
    # Portalları ve düşmanları hareket ettir
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Çizimler
    draw_player()
    draw_energy_bar(energy)
    draw_score(score)

    # Portalları çiz
    for portal in portals:
        pygame.draw.rect(screen, WHITE, portal)
        if portal.colliderect((player_x, player_y, player_width, player_height)):
            score += 10
            energy = min(energy + 20, 100)
            portals.remove(portal)

    # Düşmanları çiz
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
        if enemy.colliderect((player_x, player_y, player_width, player_height)):
            running = False  # Oyun biter

    # Enerji düşüşü
    energy -= 0.1
    if energy <= 0:
        running = False

    # Ekranı güncelle
    pygame.display.flip()
    clock.tick(FPS)

# Oyun bitti ekranı
screen.fill(BLACK)
game_over_text = font.render("Oyun Bitti! Skor: " + str(score), True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
