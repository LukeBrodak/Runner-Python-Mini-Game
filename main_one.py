import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Graphics\Font\Pixeltype.ttf', 50)

sky_surface = pygame.image.load('Graphics\sky.png').convert()
ground_surface = pygame.image.load('Graphics\purple_floor2.png').convert()

score_surf = test_font.render('Cosmic Cartwheels', False, 'gold1').convert()
score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('Graphics\slimeWalk1.png').convert_alpha()
snail_rect = snail_surf.get_rect( bottomright = (800,300))

player_surf = pygame.image.load('Graphics\Player\player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("Collide")


    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    pygame.draw.rect(screen,'Purple3',score_rect)
    pygame.draw.rect(screen,'Purple3',score_rect,10) 

    screen.blit(score_surf,score_rect)

    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surf,snail_rect)
    screen.blit(player_surf,player_rect)

   # if player_rect.colliderect(snail_rect):
   
    #if player_rect.collidepoint((mouse_pos)):
     #   print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)
