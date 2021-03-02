import pygame,time



pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("Connect Four")

background = pygame.image.load("billeder/board.png")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        window.blit(background,(0,0))   

pygame.quit()
