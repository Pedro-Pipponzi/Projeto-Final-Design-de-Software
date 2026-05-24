import pygame

pygame.init()

WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Runner')

CHAO_Y = HEIGHT - 50
GRAVIDADE = 0.8
FPS = 60

DINO_LARGURA = 40
DINO_ALTURA_NORMAL = 60
DINO_ALTURA_AGACHADO = 30
dino_x = 80
dino_bottom = CHAO_Y
vel_y = 0
no_chao = True
agachado = False

CACTO_LARGURA = 20
CACTO_ALTURA = 50
cacto_x = 600
cacto_y = CHAO_Y - CACTO_ALTURA

fonte = pygame.font.SysFont(None, 36)
frames = 0

clock = pygame.time.Clock()
game = True

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and no_chao and not agachado:
                vel_y = -15
                no_chao = False
            if event.key == pygame.K_DOWN and no_chao:
                agachado = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                agachado = False

    vel_y += GRAVIDADE
    dino_bottom += vel_y

    if dino_bottom >= CHAO_Y:
        dino_bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    frames += 1
    score = frames // 6

    altura_atual = DINO_ALTURA_AGACHADO if agachado else DINO_ALTURA_NORMAL
    dino_y = dino_bottom - altura_atual

    window.fill((255, 255, 255))
    pygame.draw.line(window, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
    pygame.draw.rect(window, (80, 80, 80), (dino_x, dino_y, DINO_LARGURA, altura_atual))
    pygame.draw.rect(window, (0, 150, 0), (cacto_x, cacto_y, CACTO_LARGURA, CACTO_ALTURA))

    texto = fonte.render('Score: {:05d}'.format(score), True, (0, 0, 0))
    window.blit(texto, (WIDTH - texto.get_width() - 20, 20))

    pygame.display.update()

pygame.quit()
