import pygame
from sys import exit
from random import randint

def display_score():
    time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score {time}',False, 'Black')
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -=5
            if obstacle.bottom == 300 : screen.blit(snail_surface,obstacle)
            else : screen.blit(fly_surface,obstacle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles :
        for obstacle in obstacles:
            if player.colliderect(obstacle): return False
    return True

def player_animation():
    global player_surf , player_index

    if player_rect.bottom < 300 :player_surf = player_jump
    else: 
        player_index += 0.2
        if player_index >= len(player_walk) : player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Code Dash")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font\Pixeltype.ttf",50)
game_active = False
start_time = 0
score = 0
icon = pygame.image.load("graphics\icon1.png"    ).convert_alpha()
pygame.display.set_icon(icon)

sky_surface = pygame.image.load('graphics/city.jpg').convert()
grd_surface = pygame.image.load('graphics/marines1.jpg').convert()
#test_surface = test_font.render('Your Game',False,'Black')

#Obstacles
snail_frame1 = pygame.image.load('graphics\snail\snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics\snail\snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_index = 0
snail_surface = snail_frames[snail_index]


fly_frame1 = pygame.image.load("graphics\Fly\Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("graphics\Fly\Fly2.png").convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_index = 0
fly_surface = fly_frames[fly_index]

obstacle_rect_list = []

#Player
player_walk_1 = pygame.image.load("graphics\walk1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics\walk2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics\jump2.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#Intermidiate screen
player_stand = pygame.image.load("graphics\icon1.png"    ).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Code Like Wind',False,'White')
game_name_rect = game_name.get_rect(center = (400,30))

game_msg = test_font.render("Let's Run !!",False,'White')
game_msg_rect = game_msg.get_rect(center = (400,380))

#timmer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer,500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300 :
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000)
    
        if game_active :
            if event.type == obstacle_timer:
                if randint(0,2): obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                else : obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_index == 0 : snail_index = 1
                else: snail_index = 0
                snail_surface = snail_frames[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0 : fly_index = 1
                else: fly_index = 0
                fly_surface = fly_frames[fly_index]        
    
    if game_active :
        #background
        screen.blit(sky_surface,(0,0))
        screen.blit(grd_surface,(0,300))
        score = display_score()
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #obstructions
        #snail_rect.x -= 5
        #if snail_rect.right <= 0 : snail_rect.left = 800
        #screen.blit(snail_surface,snail_rect)

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300 : player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        game_active = collisions(player_rect,obstacle_rect_list)
    else:
        screen.fill((222, 178, 102))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_msg = test_font.render(f'Your Score :{score}',False,'White')
        score_msg_rect = score_msg.get_rect(center = (400,380))
        screen.blit(game_name,game_name_rect)

        if score == 0 : screen.blit(game_msg,game_msg_rect)
        else : screen.blit(score_msg,score_msg_rect)

    
    pygame.display.update()
    clock.tick(60)