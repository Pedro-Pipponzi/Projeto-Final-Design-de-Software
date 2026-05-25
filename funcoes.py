import pygame
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Runner')

CHAO_Y = HEIGHT - 50
GRAVIDADE = 0.8
FPS = 60
VELOCIDADE_INICIAL = 6

CINZA = (80, 80, 80)
VERDE_ESCURO = (0, 140, 0)
ROXO = (140, 0, 180)

fonte = pygame.font.SysFont(None, 36)


class Dinossauro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.agachado = False
        self.image = pygame.Surface((40, 60))
        self.image.fill(CINZA)
        self.mask = pygame.mask.from_surface(self.image)
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
        self.image.fill(CINZA)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = antigo_x
        self.rect.bottom = CHAO_Y


class Cacto(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = velocidade
        altura = random.randint(40, 70)
        self.image = pygame.Surface((20, altura))
        self.image.fill(VERDE_ESCURO)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.bottom = CHAO_Y

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()


class ObstaculoVoador(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = velocidade
        if random.random() < 1/3:
            largura = random.randint(40, 65)
            self.image = pygame.Surface((largura, 20))
            self.image.fill(ROXO)
            fundo = CHAO_Y - 35
            self.fases = None
        else:
            self.bloco_larg = 30
            self.gap = 10
            base = random.uniform(0, 2 * math.pi)
            self.fases = [base + 2 * math.pi / 3 * i for i in range(3)]
            self.timer = 0
            self.image = pygame.Surface((self.bloco_larg * 3 + self.gap * 2, 40), pygame.SRCALPHA)
            self._desenhar_blocos()
            fundo = CHAO_Y - 60 + random.randint(1, 10)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.bottom = fundo

    def _desenhar_blocos(self):
        self.image.fill((0, 0, 0, 0))
        for i, fase in enumerate(self.fases):
            x = i * (self.bloco_larg + self.gap)
            oy = int(10 + 10 * math.sin(self.timer * 0.1 + fase))
            pygame.draw.rect(self.image, ROXO, (x, oy, self.bloco_larg, 20))

    def update(self):
        self.rect.x -= self.velocidade
        if self.fases is not None:
            self.timer += 1
            self._desenhar_blocos()
            self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < 0:
            self.kill()


def spawnar_obstaculo(velocidade):
    if random.random() < 0.5:
        return Cacto(velocidade)
    return ObstaculoVoador(velocidade)


clock = pygame.time.Clock()
game = True

dino = Dinossauro()
all_sprites = pygame.sprite.Group()
all_obstaculos = pygame.sprite.Group()
all_sprites.add(dino)

velocidade = VELOCIDADE_INICIAL
frames = 0
frames_para_proximo = 90

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

    frames_para_proximo -= 1
    if frames_para_proximo <= 0:
        obs = spawnar_obstaculo(velocidade)
        all_sprites.add(obs)
        all_obstaculos.add(obs)
        espaco_minimo = max(48, int(300 // velocidade))
        frames_para_proximo = espaco_minimo + random.randint(0, 40)

    all_sprites.update()

    if pygame.sprite.spritecollide(dino, all_obstaculos, False, pygame.sprite.collide_mask):
        game = False

    window.fill((255, 255, 255))
    pygame.draw.line(window, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
    all_sprites.draw(window)

    texto = fonte.render('Score: {:05d}'.format(score), True, (0, 0, 0))
    window.blit(texto, (WIDTH - texto.get_width() - 20, 20))

    pygame.display.update()

pygame.quit()
