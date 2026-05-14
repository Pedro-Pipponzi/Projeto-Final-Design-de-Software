import pygame

pygame.init()

WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Runner')

CHAO_Y = HEIGHT - 50

DINO_LARGURA = 40
DINO_ALTURA = 60
dino_x = 80
dino_y = CHAO_Y - DINO_ALTURA

CACTO_LARGURA = 20
CACTO_ALTURA = 50
cacto_x = 600
cacto_y = CHAO_Y - CACTO_ALTURA

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYUP:
            game = False

    window.fill((255, 255, 255))
    pygame.draw.line(window, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
    pygame.draw.rect(window, (80, 80, 80), (dino_x, dino_y, DINO_LARGURA, DINO_ALTURA))
    pygame.draw.rect(window, (0, 150, 0), (cacto_x, cacto_y, CACTO_LARGURA, CACTO_ALTURA))

    pygame.display.update()

pygame.quit()
