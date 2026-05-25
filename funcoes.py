import pygame
import random
import math
import os

pygame.init()

WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Runner')

CHAO_Y = HEIGHT - 50
GRAVIDADE = 0.8
FPS = 60
VELOCIDADE_INICIAL = 6

JOGANDO = 'jogando'
MORTO = 'morto'
REINICIANDO = 'reiniciando'

DIR = os.path.dirname(os.path.abspath(__file__))


def _carregar_som(nome):
    caminho = os.path.join(DIR, nome)
    if os.path.exists(caminho):
        return pygame.mixer.Sound(caminho)
    return None

def _carregar_frame(nome):
    img = pygame.image.load(os.path.join(DIR, nome)).convert()
    img.set_colorkey(img.get_at((0, 0)))
    return img

def _escalar(img, tamanho):
    resultado = pygame.transform.scale(img, tamanho)
    resultado.set_colorkey(img.get_colorkey())
    return resultado

def carregar_assets():
    a = {}

    a['som_pulo'] = _carregar_som('som_pulo.wav')
    a['som_colisao'] = _carregar_som('som_colisao.wav')

    pygame.mixer.music.load(os.path.join(DIR, 'musicafundo.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    _f1 = _carregar_frame('bonecoframe1.jpeg')
    _f2 = _carregar_frame('bonecoframe2.jpeg')
    _fa = _carregar_frame('bonecoagachado.jpeg')
    a['player_frames'] = [_escalar(_f1, (40, 60)), _escalar(_f2, (40, 60))]
    a['player_agachado'] = _escalar(_fa, (40, 30))

    a['cacto_dente'] = _carregar_frame('obstaculo 1.jpeg')
    a['cacto_fogo_frames'] = [
        _carregar_frame('obstaculo2(1.jpeg'),
        _carregar_frame('obstaculo2(2).jpeg'),
    ]

    a['voador_parado'] = _carregar_frame('voador parado.jpeg')
    a['voador_frames'] = [
        _carregar_frame('voador dinamico.jpeg'),
        _carregar_frame('voador dinamico2.jpeg'),
    ]

    fundo = pygame.image.load(os.path.join(DIR, 'teladefundo.jpeg')).convert()
    a['fundo_img'] = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

    a['fonte'] = pygame.font.SysFont(None, 36)

    return a


assets = carregar_assets()


class Dinossauro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.agachado = False
        self.frame_idx = 0
        self.anim_timer = 0
        self.image = assets['player_frames'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.bottom = CHAO_Y
        self.vel_y = 0
        self.no_chao = True

    def update(self):
        if not self.agachado:
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.frame_idx = (self.frame_idx + 1) % len(assets['player_frames'])
                self.image = assets['player_frames'][self.frame_idx]
                self.mask = pygame.mask.from_surface(self.image)

        self.vel_y += GRAVIDADE
        self.rect.bottom += self.vel_y
        if self.rect.bottom >= CHAO_Y:
            self.rect.bottom = CHAO_Y
            self.vel_y = 0
            self.no_chao = True

    def pular(self):
        if self.no_chao:
            if self.agachado:
                self.agachar(False)
            self.vel_y = -15
            self.no_chao = False
            if assets['som_pulo']:
                assets['som_pulo'].play()

    def agachar(self, ativo):
        if ativo == self.agachado or not self.no_chao:
            return
        self.agachado = ativo
        antigo_x = self.rect.x
        if ativo:
            self.image = assets['player_agachado']
        else:
            self.image = assets['player_frames'][self.frame_idx]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = antigo_x
        self.rect.bottom = CHAO_Y


class Cacto(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = velocidade
        self.anim_timer = 0
        self.anim_frame = 0
        if random.random() < 0.5:
            self.fogo = False
            self.image = assets['cacto_dente']
        else:
            self.fogo = True
            self.image = assets['cacto_fogo_frames'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.bottom = CHAO_Y

    def update(self):
        self.rect.x -= self.velocidade
        if self.fogo:
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(assets['cacto_fogo_frames'])
                self.image = assets['cacto_fogo_frames'][self.anim_frame]
                self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < 0:
            self.kill()


class ObstaculoVoador(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = velocidade
        if random.random() < 1/3:
            self.image = assets['voador_parado']
            fundo = CHAO_Y - 35
            self.fases = None
        else:
            self.anim_timer = 0
            self.anim_frame = 0
            self.bloco_larg = assets['voador_frames'][0].get_width()
            self.bloco_alt = assets['voador_frames'][0].get_height()
            self.gap = 10
            base = random.uniform(0, 2 * math.pi)
            self.fases = [base + 2 * math.pi / 3 * i for i in range(3)]
            self.timer = 0
            surf_larg = self.bloco_larg * 3 + self.gap * 2
            surf_alt = self.bloco_alt + 20
            self.image = pygame.Surface((surf_larg, surf_alt), pygame.SRCALPHA)
            self._desenhar_blocos()
            fundo = CHAO_Y - 60 + random.randint(1, 10)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.bottom = fundo

    def _desenhar_blocos(self):
        self.image.fill((0, 0, 0, 0))
        frame = assets['voador_frames'][self.anim_frame]
        for i, fase in enumerate(self.fases):
            x = i * (self.bloco_larg + self.gap)
            oy = int(10 + 10 * math.sin(self.timer * 0.1 + fase))
            self.image.blit(frame, (x, oy))

    def update(self):
        self.rect.x -= self.velocidade
        if self.fases is not None:
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(assets['voador_frames'])
            self.timer += 1
            self._desenhar_blocos()
            self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < 0:
            self.kill()


def spawnar_obstaculo(velocidade):
    if random.random() < 0.5:
        return Cacto(velocidade)
    return ObstaculoVoador(velocidade)


def criar_jogo():
    dino = Dinossauro()
    all_sprites = pygame.sprite.Group()
    all_obstaculos = pygame.sprite.Group()
    all_sprites.add(dino)
    return dino, all_sprites, all_obstaculos


clock = pygame.time.Clock()
estado = JOGANDO

dino, all_sprites, all_obstaculos = criar_jogo()

velocidade = VELOCIDADE_INICIAL
frames = 0
frames_para_proximo = 90
score = 0

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if estado == JOGANDO:
                if event.key == pygame.K_SPACE:
                    dino.pular()
                if event.key == pygame.K_DOWN:
                    if not dino.no_chao:
                        dino.rect.bottom = CHAO_Y
                        dino.vel_y = 0
                        dino.no_chao = True
                    dino.agachar(True)
            elif estado == MORTO:
                if event.key == pygame.K_SPACE:
                    estado = REINICIANDO
        if event.type == pygame.KEYUP and estado == JOGANDO:
            if event.key == pygame.K_DOWN:
                dino.agachar(False)

    if estado == REINICIANDO:
        dino, all_sprites, all_obstaculos = criar_jogo()
        velocidade = VELOCIDADE_INICIAL
        frames = 0
        frames_para_proximo = 90
        score = 0
        estado = JOGANDO

    if estado == JOGANDO:
        frames += 1
        score = frames // 6
        velocidade = VELOCIDADE_INICIAL + score // 30

        for obs in all_obstaculos:
            obs.velocidade = velocidade

        frames_para_proximo -= 1
        if frames_para_proximo <= 0:
            obs = spawnar_obstaculo(velocidade)
            all_sprites.add(obs)
            all_obstaculos.add(obs)
            espaco_minimo = max(36, int(240 // velocidade))
            frames_para_proximo = espaco_minimo + random.randint(0, 40)

        all_sprites.update()

        if pygame.sprite.spritecollide(dino, all_obstaculos, False, pygame.sprite.collide_mask):
            if assets['som_colisao']:
                assets['som_colisao'].play()
            estado = MORTO

    window.blit(assets['fundo_img'], (0, 0))
    pygame.draw.line(window, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
    all_sprites.draw(window)

    texto = assets['fonte'].render('Score: {:05d}'.format(score), True, (255, 255, 255))
    window.blit(texto, (WIDTH - texto.get_width() - 20, 20))

    if estado == MORTO:
        msg = assets['fonte'].render('GAME OVER  |  SPACE para reiniciar', True, (255, 0, 0))
        window.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    pygame.display.update()

pygame.quit()
