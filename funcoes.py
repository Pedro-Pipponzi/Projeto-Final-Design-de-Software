import pygame
 
pygame.init()
 
WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Runner')
 
game = True
 
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYUP:
            game = False
 
    window.fill((255, 255, 0))
    pygame.display.update()
 
pygame.quit()