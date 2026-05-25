import pygame
from funcoes import tela_jogo

pygame.init()
window = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Dino Runner')
tela_jogo(window)
pygame.quit()
