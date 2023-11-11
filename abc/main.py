import pygame

#init
pygame.init()

#Display surface objek
window = pygame.display.set_mode((500, 500))

# user input, database input
isRun = True
while isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRun = False
pygame.QUIT 