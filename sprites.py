import pygame
import random
import math
from config import CHAO_Y, GRAVIDADE, WIDTH

assets = None


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
