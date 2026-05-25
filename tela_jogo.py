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


def tela_inicio(janela):
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        janela.blit(assets['fundo_img'], (0, 0))
        msg = assets['fonte'].render('Pressione ESPAÇO para começar', True, (255, 255, 255))
        janela.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        pygame.display.update()


def tela_game_over(janela, pontuacao, recorde):
    clock = pygame.time.Clock()
    fonte = assets['fonte']
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        janela.blit(assets['fundo_img'], (0, 0))
        linhas = [
            (fonte.render('GAME OVER', True, (255, 0, 0)),                           HEIGHT // 2 - 60),
            (fonte.render('Score: {:05d}'.format(pontuacao), True, (255, 255, 255)), HEIGHT // 2 - 20),
            (fonte.render('Recorde: {:05d}'.format(recorde), True, (255, 255, 0)),   HEIGHT // 2 + 20),
            (fonte.render('SPACE para reiniciar', True, (255, 255, 255)),            HEIGHT // 2 + 60),
        ]
        for surf, y in linhas:
            janela.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
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
