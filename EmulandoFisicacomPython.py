import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Simulação Física em Python")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
LIMITE_CEU_COR = (0, 0, 255)  # Cor azul para o limite do céu

# Parâmetros do objeto
posicao = [largura_tela // 2, 50]
velocidade = [0, 0]
aceleracao = [0, 0.1]
resistencia_ar = 0.02  # Adicionando resistência do ar
amortecimento = 0.9  # Fator de amortecimento

# Parâmetros do chão
CHAO_ALTURA = 20
CHAO_COR = (0, 255, 0)  # Cor verde para o chão

# Raio do objeto
RAIO_OBJETO = 20

def handle_mouse_events():
    global clicando_no_objeto
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Lógica de Interação com o Mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down(evento)
        elif evento.type == pygame.MOUSEBUTTONUP:
            handle_mouse_up()

def handle_mouse_down(evento):
    global clicando_no_objeto
    # Verifica se o clique do mouse ocorreu sobre o objeto
    if posicao[0] - RAIO_OBJETO <= evento.pos[0] <= posicao[0] + RAIO_OBJETO and \
       posicao[1] - RAIO_OBJETO <= evento.pos[1] <= posicao[1] + RAIO_OBJETO:
        clicando_no_objeto = True

def handle_mouse_up():
    global clicando_no_objeto
    clicando_no_objeto = False

def update_position():
    global posicao, velocidade
    # Atualizar posição, velocidade e aceleração do objeto
    velocidade[0] += aceleracao[0]
    velocidade[1] += aceleracao[1]

    # Adicionar resistência do ar
    velocidade[0] *= (1 - resistencia_ar)
    velocidade[1] *= (1 - resistencia_ar)

    posicao[0] += velocidade[0]
    posicao[1] += velocidade[1]

def check_collisions():
    global posicao, velocidade
    # Verificar colisões com chão e bordas da tela

    # Verificar colisão com o chão
    if posicao[1] >= altura_tela - CHAO_ALTURA - RAIO_OBJETO:
        posicao[1] = altura_tela - CHAO_ALTURA - RAIO_OBJETO
        velocidade[1] = -velocidade[1] * amortecimento  # Inverter a velocidade e aplicar amortecimento

    # Verificar colisão com o topo da tela (limite no céu)
    if posicao[1] < RAIO_OBJETO:
        posicao[1] = RAIO_OBJETO
        velocidade[1] = -velocidade[1] * amortecimento  # Inverter a velocidade e aplicar amortecimento

    # Verificar colisão com as laterais da tela
    if posicao[0] >= largura_tela - RAIO_OBJETO:
        posicao[0] = largura_tela - RAIO_OBJETO
        velocidade[0] = -velocidade[0] * amortecimento  # Inverter a velocidade e aplicar amortecimento

    if posicao[0] < RAIO_OBJETO:
        posicao[0] = RAIO_OBJETO
        velocidade[0] = -velocidade[0] * amortecimento  # Inverter a velocidade e aplicar amortecimento

def draw_on_screen():
    # Limpar a tela e desenhar objetos
    tela.fill(BRANCO)

    # Desenhar o objeto
    pygame.draw.circle(tela, PRETO, (int(posicao[0]), int(posicao[1])), RAIO_OBJETO)

    # Desenhar o chão
    pygame.draw.rect(tela, CHAO_COR, (0, altura_tela - CHAO_ALTURA, largura_tela, CHAO_ALTURA))

    # Desenhar o limite no céu
    pygame.draw.rect(tela, LIMITE_CEU_COR, (0, 0, largura_tela, 1))

    # Atualizar a tela
    pygame.display.flip()

# Loop principal
clicando_no_objeto = False
while True:
    handle_mouse_events()

    if clicando_no_objeto and pygame.mouse.get_pressed()[0]:
        # Calcular a diferença entre a posição do cursor e a posição atual do objeto
        diff_x, diff_y = pygame.mouse.get_pos()[0] - posicao[0], pygame.mouse.get_pos()[1] - posicao[1]
        # Atualizar a posição do objeto com a diferença
        posicao[0] += diff_x
        posicao[1] += diff_y

    update_position()
    check_collisions()
    draw_on_screen()

    pygame.time.Clock().tick(60)
