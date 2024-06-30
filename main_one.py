import pygame
from sys import exit
from random import randint, choice
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Graphics/globe1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Graphics/globe2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Graphics/globe3.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('Graphics/blackhole.png').convert_alpha()
            fly_2 = pygame.image.load('Graphics/blackhole2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.y_pos_base = 190
            self.y_offset = 0
            self.time = 0

        else:
            snail_1 = pygame.image.load('Graphics/slimeWalk1.png').convert_alpha()
            snail_2 = pygame.image.load('Graphics/slimeWalk2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.y_pos_base = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), self.y_pos_base))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6

        if hasattr(self, 'y_offset'):
            self.time += 0.1
            self.y_offset = 50 * math.sin(self.time)
            self.rect.y = self.y_pos_base + self.y_offset

        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    score_surf = test_font.render(f'Score: {current_time:.1f}', False, '#EE00FF')
    score_rect = score_surf.get_rect(center=(525, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Cosmic Cartwheels')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Graphics/Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(.15)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Graphics/sky.png').convert()
ground_surface = pygame.image.load('Graphics/purple_floor2.png').convert()

player_stand = pygame.image.load('Graphics/globe1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Planetary Devastation', False, '#FFD700')
game_name_rect = game_name.get_rect(center=(400, 200))

game_message = test_font.render('Press SPACE to bounce again!', False, '#FF1493')
game_message_rect = game_message.get_rect(center=(400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

snail_frame_index = 0
fly_frame_index = 0

snail_frames = [
    pygame.image.load('Graphics/slimeWalk1.png').convert_alpha(),
    pygame.image.load('Graphics/slimeWalk2.png').convert_alpha()
]

fly_frames = [
    pygame.image.load('Graphics/blackhole.png').convert_alpha(),
    pygame.image.load('Graphics/blackhole2.png').convert_alpha()
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.sprite.rect.collidepoint(event.pos) and player.sprite.rect.bottom >= 300:
                    player.sprite.gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.rect.bottom >= 300:
                    player.sprite.gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        if event.type == snail_animation_timer:
            snail_frame_index = (snail_frame_index + 1) % len(snail_frames)
            for obstacle in obstacle_group:
                if obstacle.y_pos_base == 300:
                    obstacle.frames = snail_frames
                    obstacle.image = snail_frames[snail_frame_index]

        if event.type == fly_animation_timer:
            fly_frame_index = (fly_frame_index + 1) % len(fly_frames)
            for obstacle in obstacle_group:
                if obstacle.y_pos_base == 190:
                    obstacle.frames = fly_frames
                    obstacle.image = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill('#722BED')
        screen.blit(player_stand, player_stand_rect)
        obstacle_group.empty()
        player.sprite.rect.midbottom = (80, 300)
        player.sprite.gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, '#FFD700')
        score_message_rect = score_message.get_rect(center=(400, 350))
        screen.blit(game_name, (250, 50))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
