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
import traceback  # Para nos mostrar o erro se o jogo fechar

# ----------------------------------------------------------
# 🔧 INICIALIZAÇÃO E PROTEÇÃO CONTRA ERROS
# ----------------------------------------------------------
try:
    pygame.init()

    # Configurações
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    pygame.display.set_caption("Space Escape")  # Tirei emojis do título para evitar bugs em Windows antigo

    # Tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # ----------------------------------------------------------
    # 🧩 ASSETS (IMAGENS E SONS)
    # ----------------------------------------------------------
    ASSETS = {
        "background": "foto-selva-2.png",
        "background1": "ceu.png",
        "background2": "fase-final3.0.png",
        "player": "nave-d-gerra.png",
        "meteor": "meteoro-final.png",
        "sound_point": "point-final.mp3",
        "sound_hit": "som-dano-final.mp3",
        "music": "som-final.mp3"
    }

    # Cores
    WHITE = (255, 255, 255)
    RED = (255, 60, 60)
    BLUE = (60, 100, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)


    # Funções de Carregamento
    def load_image(filename, fallback_color, size=None):
        path = os.path.join(os.getcwd(), filename)  # Garante que pega o caminho certo
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        else:
            print(f"AVISO: Imagem nao encontrada: {filename}")
            surf = pygame.Surface(size or (50, 50))
            surf.fill(fallback_color)
            return surf


    def load_sound(filename):
        if os.path.exists(filename):
            return pygame.mixer.Sound(filename)
        return None


    # Carregando Assets
    background = load_image(ASSETS["background"], BLACK, (WIDTH, HEIGHT))
    background1 = load_image(ASSETS["background1"], BLACK, (WIDTH, HEIGHT))
    background2 = load_image(ASSETS["background2"], BLACK, (WIDTH, HEIGHT))

    player_img = load_image(ASSETS["player"], BLUE, (80, 60))
    meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

    sound_point = load_sound(ASSETS["sound_point"])
    sound_hit = load_sound(ASSETS["sound_hit"])

    # Fontes
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 80)

    # ----------------------------------------------------------
    # 🧠 VARIÁVEIS GLOBAIS DO JOGO
    # ----------------------------------------------------------
    # Estado do jogo: "MENU", "JOGANDO", "GAMEOVER"
    game_state = "MENU"

    # Variáveis que mudam
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    meteor_list = []
    score = 0
    lives = 3
    fase = 1
    current_background = background
    meteor_speed = 5

    # Invencibilidade
    player_hit = False
    player_hit_timer = 0
    INVINCIBLE_DURATION = 1500


    # Função para reiniciar as variáveis quando o jogo começa
    def start_new_game():
        global score, lives, fase, meteor_list, player_rect, current_background, meteor_speed, player_hit
        score = 0
        lives = 3
        fase = 1
        meteor_speed = 5
        current_background = background
        player_rect.center = (WIDTH // 2, HEIGHT - 60)
        player_hit = False

        meteor_list.clear()
        for _ in range(5):
            add_meteor()

        # Inicia música se existir
        if os.path.exists(ASSETS["music"]):
            pygame.mixer.music.load(ASSETS["music"])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)


    def add_meteor():
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-500, -40)
        rect = pygame.Rect(x, y, 40, 40)
        angle = 0
        rot_speed = random.choice([-2, -1, 1, 2])
        meteor_list.append({'rect': rect, 'angle': angle, 'rot_speed': rot_speed})


    # ----------------------------------------------------------
    # 🕹️ LOOP PRINCIPAL (GAME ENGINE)
    # ----------------------------------------------------------
    running = True
    while running:
        clock.tick(FPS)

        # 1. GESTÃO DE EVENTOS (Teclado/Mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Se estiver no MENU, qualquer tecla começa
            if game_state == "MENU":
                if event.type == pygame.KEYDOWN:
                    start_new_game()
                    game_state = "JOGANDO"

            # Se estiver no GAMEOVER, qualquer tecla volta pro menu
            elif game_state == "GAMEOVER":
                if event.type == pygame.KEYDOWN:
                    game_state = "MENU"

        # 2. LÓGICA E DESENHO BASEADO NO ESTADO

        # --- TELA DE MENU ---
        if game_state == "MENU":
            screen.blit(background, (0, 0))

            # Título
            t_surf = title_font.render("SPACE ESCAPE", True, YELLOW)
            t_rect = t_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            screen.blit(t_surf, t_rect)

            # Piscar texto
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                msg = font.render("Pressione qualquer tecla", True, WHITE)
                msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                screen.blit(msg, msg_rect)

        # --- TELA DE JOGO ---
        elif game_state == "JOGANDO":
            screen.blit(current_background, (0, 0))

            # Movimento Nave
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= 7
            if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
                player_rect.x += 7

            # Timer Invencibilidade
            if player_hit:
                if pygame.time.get_ticks() - player_hit_timer > INVINCIBLE_DURATION:
                    player_hit = False

            # Meteoros
            for meteor in meteor_list:
                meteor['rect'].y += meteor_speed
                meteor['angle'] = (meteor['angle'] + meteor['rot_speed']) % 360

                # Caiu e voltou pro topo
                if meteor['rect'].y > HEIGHT:
                    meteor['rect'].y = random.randint(-100, -40)
                    meteor['rect'].x = random.randint(0, WIDTH - 40)
                    score += 1
                    if sound_point: sound_point.play()

                # Colisão
                if meteor['rect'].colliderect(player_rect) and not player_hit:
                    lives -= 1
                    player_hit = True
                    player_hit_timer = pygame.time.get_ticks()
                    if sound_hit: sound_hit.play()

                    # Reposiciona meteoro que bateu
                    meteor['rect'].y = random.randint(-100, -40)
                    meteor['rect'].x = random.randint(0, WIDTH - 40)

                    if lives <= 0:
                        game_state = "GAMEOVER"
                        pygame.mixer.music.stop()

            # Sistema de Fases
            if fase == 1 and score >= 200:
                fase = 2
                meteor_speed = 7
                current_background = background1
                if len(meteor_list) < 10:  # Limita maximo de meteoros
                    for _ in range(5): add_meteor()

            elif fase == 2 and score >= 500:
                fase = 3
                meteor_speed = 10
                current_background = background2
                if len(meteor_list) < 15:
                    for _ in range(5): add_meteor()

            # Desenha Player (Piscando se atingido)
            if not player_hit or (pygame.time.get_ticks() // 100) % 2:
                screen.blit(player_img, player_rect)

            # Desenha Meteoros
            for meteor in meteor_list:
                rot_img = pygame.transform.rotate(meteor_img, meteor['angle'])
                rot_rect = rot_img.get_rect(center=meteor['rect'].center)
                screen.blit(rot_img, rot_rect)

            # Placar
            score_text = font.render(f"Score: {score}  Vidas: {lives}  Fase: {fase}", True, WHITE)
            screen.blit(score_text, (10, 10))

        # --- TELA DE GAMEOVER ---
        elif game_state == "GAMEOVER":
            screen.fill((20, 20, 20))

            over_text = font.render("FIM DE JOGO", True, RED)
            pts_text = font.render(f"Pontos Finais: {score}", True, WHITE)
            restart_text = font.render("Pressione qualquer tecla para voltar ao menu", True, BLUE)

            screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
            screen.blit(pts_text, (WIDTH // 2 - 90, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - 220, HEIGHT // 2 + 60))

        pygame.display.flip()

    pygame.quit()

except Exception as e:
    # SE O JOGO DER ERRO, ELE VAI CAIR AQUI E MOSTRAR O MOTIVO
    print("\n---------------------------------------------------")
    print("❌ OCORREU UM ERRO E O JOGO FECHOU:")
    print(e)
    print("---------------------------------------------------")
    traceback.print_exc()  # Mostra a linha exata do erro
    input("\nPressione ENTER para fechar a janela de erro...")
