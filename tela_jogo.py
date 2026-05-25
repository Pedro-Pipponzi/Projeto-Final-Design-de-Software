import pygame
import random
from config import JOGANDO, MORTO, REINICIANDO, VELOCIDADE_INICIAL, FPS, WIDTH, HEIGHT, CHAO_Y
import sprites
from assets import carregar_assets

assets = None


def criar_jogo():
    dino = sprites.Dinossauro()
    all_sprites = pygame.sprite.Group()
    all_obstaculos = pygame.sprite.Group()
    all_sprites.add(dino)
    return dino, all_sprites, all_obstaculos


def tela_jogo(janela):
    global assets
    sprites.assets = carregar_assets()
    assets = sprites.assets

    clock = pygame.time.Clock()
    estado = JOGANDO
    dino, all_sprites, all_obstaculos = criar_jogo()
    velocidade = VELOCIDADE_INICIAL
    frames = 0
    frames_para_proximo = 90
    score = 0
    recorde = 0

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
                obs = sprites.spawnar_obstaculo(velocidade)
                all_sprites.add(obs)
                all_obstaculos.add(obs)
                espaco_minimo = max(36, int(240 // velocidade))
                frames_para_proximo = espaco_minimo + random.randint(0, 40)

            all_sprites.update()

            if pygame.sprite.spritecollide(dino, all_obstaculos, False, pygame.sprite.collide_mask):
                if assets['som_colisao']:
                    assets['som_colisao'].play()
                recorde = max(recorde, score)
                estado = MORTO

        janela.blit(assets['fundo_img'], (0, 0))
        pygame.draw.line(janela, (0, 0, 0), (0, CHAO_Y), (WIDTH, CHAO_Y), 2)
        all_sprites.draw(janela)

        texto_score = assets['fonte'].render('Score: {:05d}'.format(score), True, (255, 255, 255))
        texto_recorde = assets['fonte'].render('Recorde: {:05d}'.format(recorde), True, (255, 255, 0))
        janela.blit(texto_score, (WIDTH - texto_score.get_width() - 20, 20))
        janela.blit(texto_recorde, (WIDTH - texto_recorde.get_width() - 20, 55))

        if estado == MORTO:
            msg = assets['fonte'].render('GAME OVER  |  SPACE para reiniciar', True, (255, 0, 0))
            janela.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.update()
