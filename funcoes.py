import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Runner')

CHAO_Y = HEIGHT - 50
GRAVIDADE = 0.8
FPS = 60

CACTO_LARGURA = 20
cacto_altura = 50
cacto_vel = 6
cacto_x = WIDTH
cacto_y = CHAO_Y - cacto_altura

fonte = pygame.font.SysFont(None, 36)
frames = 0


class Dinossauro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.agachado = False
        self.image = pygame.Surface((40, 60))
        self.image.fill((80, 80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.bottom = CHAO_Y
        self.vel_y = 0
        self.no_chao = True

    def update(self):
        self.vel_y += GRAVIDADE
        self.rect.bottom += self.vel_y
        if self.rect.bottom >= CHAO_Y:
            self.rect.bottom = CHAO_Y
            self.vel_y = 0
            self.no_chao = True

    def pular(self):
        if self.no_chao and not self.agachado:
            self.vel_y = -15
            self.no_chao = False

    def agachar(self, ativo):
        if ativo == self.agachado or not self.no_chao:
            return
        self.agachado = ativo
        antigo_x = self.rect.x
        if ativo:
            self.image = pygame.Surface((40, 30))
        else:
            self.image = pygame.Surface((40, 60))
        self.image.fill((80, 80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = antigo_x
        self.rect.bottom = CHAO_Y


clock = pygame.time.Clock()
game = True

dino = Dinossauro()
all_sprites = pygame.sprite.Group()
all_sprites.add(dino)

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.pular()
            if event.key == pygame.K_DOWN:
                dino.agachar(True)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                dino.agachar(False)

    all_sprites.update()

    cacto_x -= cacto_vel
    if cacto_x + CACTO_LARGURA < 0:
        cacto_x = WIDTH
        cacto_altura = random.randint(40, 70)
        cacto_y = CHAO_Y - cacto_altura

    frames += 1
    score = frames // 6

    window.fill((255, 255, 255))
    pygame.draw.line(window, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
    all_sprites.draw(window)
    pygame.draw.rect(window, (0, 150, 0), (cacto_x, cacto_y, CACTO_LARGURA, cacto_altura))

    texto = fonte.render('Score: {:05d}'.format(score), True, (0, 0, 0))
    window.blit(texto, (WIDTH - texto.get_width() - 20, 20))

    pygame.display.update()

pygame.quit()


