import pygame
import random
from config import VELOCIDADE_INICIAL, FPS, WIDTH, HEIGHT, CHAO_Y
import sprites
from assets import carregar_assets

assets = None


def criar_jogo():
    dino = sprites.Dinossauro()
    all_sprites = pygame.sprite.Group()
    all_obstaculos = pygame.sprite.Group()
    all_sprites.add(dino)
    return dino, all_sprites, all_obstaculos


def _desenhar_painel(janela, grupos):
    pad = 24
    espaco_entre = 10
    todas = [s for grupo in grupos for s in grupo]
    separadores = len(grupos) - 1

    box_w = max(s.get_width() for s in todas) + pad * 2
    box_h = (sum(s.get_height() for s in todas)
             + espaco_entre * (len(todas) - 1)
             + separadores * 16
             + pad * 2)
    box_x = WIDTH // 2 - box_w // 2
    box_y = HEIGHT // 2 - box_h // 2

    fundo = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    fundo.fill((0, 0, 0, 190))
    janela.blit(fundo, (box_x, box_y))
    pygame.draw.rect(janela, (255, 255, 255), (box_x, box_y, box_w, box_h), 2)

    y = box_y + pad
    for g, grupo in enumerate(grupos):
        for surf in grupo:
            janela.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
            y += surf.get_height() + espaco_entre
        if g < separadores:
            y += 16


def tela_inicio(janela):
    clock = pygame.time.Clock()
    fonte_hist = pygame.font.SysFont(None, 30)
    historia = [
        fonte_hist.render('Você invadiu a terra do ChupaCabra,', True, (220, 220, 220)),
        fonte_hist.render('roubou seu chapeu e seu bebê Vermelinho.', True, (220, 220, 220)),
        fonte_hist.render('CORRA', True, (255, 80, 80)),
    ]
    instrucao = [assets['fonte'].render('Pressione ESPAÇO para começar', True, (255, 255, 0))]
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        janela.blit(assets['fundo_img'], (0, 0))
        _desenhar_painel(janela, [historia, instrucao])
        pygame.display.update()


def tela_game_over(janela, pontuacao, recorde):
    clock = pygame.time.Clock()
    fonte = assets['fonte']
    titulo = [fonte.render('GAME OVER', True, (255, 60, 60))]
    resultados = [
        fonte.render('Score: {:05d}'.format(pontuacao), True, (255, 255, 255)),
        fonte.render('Recorde: {:05d}'.format(recorde), True, (255, 255, 0)),
    ]
    instrucao = [fonte.render('SPACE para reiniciar', True, (180, 180, 180))]
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        janela.blit(assets['fundo_img'], (0, 0))
        _desenhar_painel(janela, [titulo, resultados, instrucao])
        pygame.display.update()


def tela_jogo(janela):
    global assets
    sprites.assets = carregar_assets()
    assets = sprites.assets

    clock = pygame.time.Clock()
    recorde = 0

    if not tela_inicio(janela):
        return

    while True:
        dino, all_sprites, all_obstaculos = criar_jogo()
        velocidade = VELOCIDADE_INICIAL
        frames = 0
        frames_para_proximo = 90
        score = 0

        while True:
            clock.tick(FPS)

            quit_game = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dino.pular()
                    if event.key == pygame.K_DOWN:
                        if not dino.no_chao:
                            dino.rect.bottom = CHAO_Y
                            dino.vel_y = 0
                            dino.no_chao = True
                        dino.agachar(True)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dino.agachar(False)

            if quit_game:
                return

            frames += 1
            score = frames // 6
            velocidade = VELOCIDADE_INICIAL + score // 30

            for obs in all_obstaculos:
                obs.velocidade = velocidade

            frames_para_proximo -= 1
            if frames_para_proximo <= 0:
                obs = sprites.spawnar_obstaculo(velocidade)
                all_sprites.add(obs)
                all_obstaculos.add(obs)
                espaco_minimo = max(36, int(240 // velocidade))
                frames_para_proximo = espaco_minimo + random.randint(0, 40)

            all_sprites.update()

            janela.blit(assets['fundo_img'], (0, 0))
            pygame.draw.line(janela, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
            all_sprites.draw(janela)

            texto_score = assets['fonte'].render('Score: {:05d}'.format(score), True, (255, 255, 255))
            texto_recorde = assets['fonte'].render('Recorde: {:05d}'.format(recorde), True, (255, 255, 0))
            janela.blit(texto_score, (WIDTH - texto_score.get_width() - 20, 20))
            janela.blit(texto_recorde, (WIDTH - texto_recorde.get_width() - 20, 55))

            pygame.display.update()

            if pygame.sprite.spritecollide(dino, all_obstaculos, False, pygame.sprite.collide_mask):
                if assets['som_colisao']:
                    assets['som_colisao'].play()
                recorde = max(recorde, score)
                break

        if not tela_game_over(janela, score, recorde):
            return
