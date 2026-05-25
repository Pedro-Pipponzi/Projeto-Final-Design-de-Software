import pygame
import os
from config import DIR, WIDTH, HEIGHT


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
