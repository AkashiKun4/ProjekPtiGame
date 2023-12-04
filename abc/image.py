import pygame
import sys

pygame.init()
widht, height = 500, 500
backgroundColor = 33, 33, 33

screen = pygame.display.set_mode((widht, height))

menuImg = pygame.image.load('Mainmenu.png')
mainMenu = pygame.transform.scale(menuImg, (500, 500))

color = (0, 40, 170)
player_x = 0
player_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        
    screen.blit(mainMenu,(player_x, player_y))

    pygame.display.update()