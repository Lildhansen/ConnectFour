import pygame,time


pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((640,480)) #each row = 91,43
pygame.display.set_caption("Connect Four")

#class Background(pygame.sprite.Sprite):
 #   def __init__(self, image_file, location):
  #      pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
   #     self.image = pygame.image.load(image_file)
    #    self.rect = self.image.get_rect()
     #   self.rect.left, self.rect.top = location

bg = pygame.image.load('billeder/bg.png')

running = True

pygame.draw.rect(window,(255,255,255),(0,0,0,0))

while running:
    pygame.display.update()
    window.blit(bg,[0,0])

    for event in pygame.event.get(): 
        
        if event.type == pygame.QUIT:
            running = False
        

pygame.quit()
