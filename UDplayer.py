import pygame

print('UDplayer Initialized')

pygame.init()

################ VARIABLES

size = [512,512]

################

screen = pygame.display.set_mode(size)

gameloop = True
while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False

    pygame.display.init()
    screen.fill((200,200,200))

    pygame.display.update()