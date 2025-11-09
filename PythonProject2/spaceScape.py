##############################################################

###               S P A C E     E S C A P E                ###

##############################################################

###                  versao Alpha 0.3                      ###

##############################################################

### Objetivo: desviar dos meteoros que caem.               ###

### Cada colisão tira uma vida. Sobreviva o máximo que     ###

### conseguir!                                             ###

##############################################################

### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###

##############################################################


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

# 🧩 SEÇÃO DE ASSETS (os alunos podem trocar os arquivos aqui)

# ----------------------------------------------------------

# Dica: coloque as imagens e sons na mesma pasta do arquivo .py

# e troque apenas os nomes abaixo.


ASSETS = {

    "background": "ceu.jpg",  # imagem de fundo

    "player": "nave-d-gerra.png",  # imagem da nave

    "meteor": "cometa.png",  # imagem do meteoro

    "sound_point": "ponto.mp3",  # som ao desviar com sucesso

    "sound_hit": "destruicao.mp3",  # som de colisão

    "music": "music-rock.mp3"  # música de fundo. direitos: Music by Maksym Malko from Pixabay

}

# ----------------------------------------------------------

# 🖼️ CARREGAMENTO DE IMAGENS E SONS

# ----------------------------------------------------------

# Cores para fallback (caso os arquivos não existam)

WHITE = (255, 255, 255)

RED = (255, 60, 60)

BLUE = (60, 100, 255)

# Tela do jogo

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Função auxiliar para carregar imagens de forma segura

def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):

        img = pygame.image.load(filename).convert_alpha()

        if size:
            img = pygame.transform.scale(img, size)

        return img

    else:

        # Gera uma superfície simples colorida se a imagem não existir

        surf = pygame.Surface(size or (50, 50))

        surf.fill(fallback_color)

        return surf


# Carrega imagens

background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))

player_img = load_image(ASSETS["player"], BLUE, (80, 60))

meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))


# Sons

def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)

    return None


sound_point = load_sound(ASSETS["sound_point"])

sound_hit = load_sound(ASSETS["sound_hit"])

# Música de fundo (opcional)

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])

    pygame.mixer.music.set_volume(0.3)

    pygame.mixer.music.play(-1)  # loop infinito

# ----------------------------------------------------------

# 🧠 VARIÁVEIS DE JOGO

# ----------------------------------------------------------

player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))

player_speed = 7

meteor_list = []

for _ in range(5):
    x = random.randint(0, WIDTH - 40)

    y = random.randint(-500, -40)

    rect = pygame.Rect(x, y, 40, 40)

    angle = 0

    rot_speed = random.choice([-2, -1, 1, 2])  # Velocidade e direção da rotação

    meteor_list.append({'rect': rect, 'angle': angle, 'rot_speed': rot_speed})

meteor_speed = 5

score = 0

lives = 3

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

running = True

#########


### NOVO: Variáveis para o efeito de "piscar" (invencibilidade) ###

PLAYER_INVINCIBLE_DURATION = 1500  # Duração em milissegundos (1.5 segundos)

player_hit = False  # A nave foi atingida?

player_hit_timer = 0  # "Cronômetro" para medir o tempo da invencibilidade

# ----------------------------------------------------------

# 🕹️ LOOP PRINCIPAL

# ----------------------------------------------------------

while running:

    clock.tick(FPS)

    screen.blit(background, (0, 0))

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

    ### NOVO: Verifica o timer de invencibilidade ###

    if player_hit:

        current_time = pygame.time.get_ticks()

        if current_time - player_hit_timer > PLAYER_INVINCIBLE_DURATION:
            player_hit = False  # Tempo de invencibilidade acabou

    # --- Movimento dos meteoros ---

    for meteor_data in meteor_list:  ### ALTERADO: Itera sobre a lista de dicionários

        # Movimento de queda

        meteor_data['rect'].y += meteor_speed

        ### NOVO: Atualiza o ângulo de rotação ###

        meteor_data['angle'] = (meteor_data['angle'] + meteor_data['rot_speed']) % 360

        # Saiu da tela → reposiciona e soma pontos

        if meteor_data['rect'].y > HEIGHT:

            meteor_data['rect'].y = random.randint(-100, -40)

            meteor_data['rect'].x = random.randint(0, WIDTH - meteor_data['rect'].width)

            score += 1

            if sound_point:
                sound_point.play()

        # Colisão

        ### ALTERADO: Verifica 'player_hit' para dar invencibilidade ###

        if meteor_data['rect'].colliderect(player_rect) and not player_hit:

            lives -= 1

            ### NOVO: Ativa o estado de "hit" e o timer ###

            player_hit = True

            player_hit_timer = pygame.time.get_ticks()  # Marca a hora da colisão

            # Reposiciona o meteoro

            meteor_data['rect'].y = random.randint(-100, -40)

            meteor_data['rect'].x = random.randint(0, WIDTH - meteor_data['rect'].width)

            if sound_hit:
                sound_hit.play()

            if lives <= 0:
                running = False

    # --- Desenha tudo ---

    ### ALTERADO: Lógica para desenhar o jogador (piscar) ###

    # Se o jogador não foi atingido, desenha normalmente

    if not player_hit:

        screen.blit(player_img, player_rect)

    else:

        # Se foi atingido, pisca (alterna o desenho)

        # (pygame.time.get_ticks() // 100) % 2 alterna entre 0 e 1

        if (pygame.time.get_ticks() // 100) % 2 == 1:
            screen.blit(player_img, player_rect)

    ### ALTERADO: Lógica para desenhar os meteoros (com rotação) ###

    for meteor_data in meteor_list:
        # 1. Rotaciona a imagem original do meteoro

        rotated_img = pygame.transform.rotate(meteor_img, meteor_data['angle'])

        # 2. Cria um novo rect para a imagem rotacionada,

        #    mas mantém o centro do rect original (isso evita que ele "pule")

        rotated_rect = rotated_img.get_rect(center=meteor_data['rect'].center)

        # 3. Desenha a imagem rotacionada no novo rect

        screen.blit(rotated_img, rotated_rect)

    # --- Exibe pontuação e vidas ---

    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)

    screen.blit(text, (10, 10))

    pygame.display.flip()

# ----------------------------------------------------------

# 🏁 TELA DE FIM DE JOGO

# ----------------------------------------------------------

pygame.mixer.music.stop()

screen.fill((20, 20, 20))

end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)

final_score = font.render(f"Pontuação final: {score}", True, WHITE)

screen.blit(end_text, (150, 260))

screen.blit(final_score, (300, 300))

pygame.display.flip()

waiting = True

while waiting:

    for event in pygame.event.get():

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()