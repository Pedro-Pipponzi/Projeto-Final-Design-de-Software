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
VELOCIDADE_INICIAL = 6

fonte = pygame.font.SysFont(None, 36)


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


class Cacto(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = velocidade
        altura = random.randint(40, 70)
        self.image = pygame.Surface((20, altura))
        self.image.fill((0, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.bottom = CHAO_Y

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()


clock = pygame.time.Clock()
game = True

dino = Dinossauro()
all_sprites = pygame.sprite.Group()
all_obstaculos = pygame.sprite.Group()
all_sprites.add(dino)

velocidade = VELOCIDADE_INICIAL
frames = 0

cacto = Cacto(velocidade)
all_sprites.add(cacto)
all_obstaculos.add(cacto)

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

    frames += 1
    score = frames // 6
    velocidade = VELOCIDADE_INICIAL + score // 80

    for obs in all_obstaculos:
        obs.velocidade = velocidade

    all_sprites.update()

    if len(all_obstaculos) == 0:
        cacto = Cacto(velocidade)
        all_sprites.add(cacto)
        all_obstaculos.add(cacto)

    if pygame.sprite.spritecollide(dino, all_obstaculos, False):
        game = False

    window.fill((255, 255, 255))
    pygame.draw.line(window, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
    all_sprites.draw(window)

    texto = fonte.render('Score: {:05d}'.format(score), True, (0, 0, 0))
    window.blit(texto, (WIDTH - texto.get_width() - 20, 20))

    pygame.display.update()

pygame.quit()
