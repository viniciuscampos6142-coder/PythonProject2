import pygame
import random
import os

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "foto-selva-2.png",
    "background1": "ceu.jpg",
    "background2": "fase-final3.0.png",
    "player": "nave-d-gerra.png",
    "meteor": "meteoro-final.png",
    "sound_point": "point-final.mp3",
    "sound_hit": "som-dano-final.mp3",
    "music": "som-final.mp3"
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf


# Carrega imagens
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
background1 = load_image(ASSETS["background1"], WHITE, (WIDTH, HEIGHT))
background2 = load_image(ASSETS["background2"], WHITE, (WIDTH, HEIGHT))

# Define o fundo inicial
current_background = background

player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))


def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None


sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

meteor_list = []


# Função para criar meteoro (para facilitar adicionar mais depois)
def create_meteor():
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    rect = pygame.Rect(x, y, 40, 40)
    angle = 0
    rot_speed = random.choice([-2, -1, 1, 2])
    return {'rect': rect, 'angle': angle, 'rot_speed': rot_speed}


# Cria os meteoros iniciais
for _ in range(5):
    meteor_list.append(create_meteor())

meteor_speed = 5
score = 0
lives = 3
fase = 1
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

# Variáveis de invencibilidade
PLAYER_INVINCIBLE_DURATION = 1500
player_hit = False
player_hit_timer = 0

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)

    # --- CORREÇÃO 1: Desenhar 'current_background' e não 'background' ---
    screen.blit(current_background, (0, 0))

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Movimento do jogador ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # --- Timer de invencibilidade ---
    if player_hit:
        current_time = pygame.time.get_ticks()
        if current_time - player_hit_timer > PLAYER_INVINCIBLE_DURATION:
            player_hit = False

    # --- Movimento dos meteoros ---
    for meteor_data in meteor_list:
        meteor_data['rect'].y += meteor_speed
        meteor_data['angle'] = (meteor_data['angle'] + meteor_data['rot_speed']) % 360

        # Saiu da tela -> reposiciona e ganha ponto
        if meteor_data['rect'].y > HEIGHT:
            meteor_data['rect'].y = random.randint(-100, -40)
            meteor_data['rect'].x = random.randint(0, WIDTH - meteor_data['rect'].width)
            score += 1
            if sound_point:
                sound_point.play()

        # Colisão
        if meteor_data['rect'].colliderect(player_rect) and not player_hit:
            lives -= 1
            player_hit = True
            player_hit_timer = pygame.time.get_ticks()

            meteor_data['rect'].y = random.randint(-100, -40)
            meteor_data['rect'].x = random.randint(0, WIDTH - meteor_data['rect'].width)

            if sound_hit:
                sound_hit.play()

            if lives <= 0:
                running = False

    # --- CORREÇÃO 2: Lógica de fases fora do loop de colisão ---
    # Movemos isso para o loop principal para ser verificado constantemente

    if fase == 1 and score >= 200:
        fase = 2
        meteor_speed = 7
        current_background = background1  # Atualiza a variável de fundo
        print("--- FASE 2 INICIADA ---")
        # Adiciona 5 meteoros extras
        for _ in range(5):
            meteor_list.append(create_meteor())

    elif fase == 2 and score >= 500:
        fase = 3
        meteor_speed = 10
        current_background = background2  # Atualiza a variável de fundo
        print("--- FASE FINAL INICIADA ---")
        # Adiciona mais 5 meteoros
        for _ in range(5):
            meteor_list.append(create_meteor())

    # --- Desenha Jogador (efeito piscar) ---
    if not player_hit:
        screen.blit(player_img, player_rect)
    else:
        if (pygame.time.get_ticks() // 100) % 2 == 1:
            screen.blit(player_img, player_rect)

    # --- Desenha Meteoros ---
    for meteor_data in meteor_list:
        rotated_img = pygame.transform.rotate(meteor_img, meteor_data['angle'])
        rotated_rect = rotated_img.get_rect(center=meteor_data['rect'].center)
        screen.blit(rotated_img, rotated_rect)

    # --- HUD ---
    text = font.render(f"Pontos: {score}   Vidas: {lives}  Fase: {fase}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)

# Centraliza o texto
text_rect = end_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30))
score_rect = final_score.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 30))

screen.blit(end_text, text_rect)
screen.blit(final_score, score_rect)
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()