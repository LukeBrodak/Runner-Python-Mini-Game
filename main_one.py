import pygame
from sys import exit

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    score_surf = test_font.render(f'Score: {current_time:.1f}', False, '#EE00FF') 
    score_rect = score_surf.get_rect(center = (525, 50))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Cosmic Cartwheels')
clock = pygame.time.Clock()   
test_font = pygame.font.Font('Graphics\Font\Pixeltype.ttf', 50)
game_active = True
start_time = 0
score = 0

game_over_surface = pygame.image.load('Graphics\gameoverangry.png').convert()
sky_surface = pygame.image.load('Graphics\sky.png').convert()
ground_surface = pygame.image.load('Graphics\purple_floor2.png').convert()

# score_surf = test_font.render('Cosmic Cartwheels', False,'#6E0D25')
# score_rect = score_surf.get_rect(center = (400, 50))



snail_surf = pygame.image.load('Graphics\slimeWalk1.png').convert_alpha()
snail_rect = snail_surf.get_rect( bottomright = (600,300))

player_surf = pygame.image.load('Graphics/vapey.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

player_stand = pygame.image.load('Graphics/vapey.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2.5)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Bouncing Brimstones', False,'#FFD700')
game_name_rect = game_name.get_rect(center = (400,200))

game_message = test_font.render('Press SPACE to bounce again!', False, '#FF1493')
game_message_rect = game_message.get_rect(center = (400, 350))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)


while True:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20 
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer and game_active:
            print('test')

    if game_active:        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen,'#5D0CE9',score_rect)     
        # pygame.draw.rect(screen,'#5D0CE9',score_rect,20)
        # screen.blit(score_surf,score_rect)
        score = display_score()
        

        snail_rect.x -= 5
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf,snail_rect)

        #PLAYER
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        #collisions
        if snail_rect.colliderect(player_rect):
            game_active = False

    else:
        screen.fill('#722BED')
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False,'#FFD700')
        score_message_rect = score_message.get_rect(center = (400, 350))
        screen.blit(game_name,(250,50)) 


        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect) 

   
        # else:
        #   screen.blit(game_over_surface,(0,0))

    pygame.display.update()
    clock.tick(60)
