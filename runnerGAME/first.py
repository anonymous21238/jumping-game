import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image 
        self.rect


def displayScore():
    current_time = int(2*(pygame.time.get_ticks() - start_time)/1000)
    score_surface = test_font.render(f'SCORE: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
            # screen.blit(fly_frame_1,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200]
        return obstacle_list
    else:
        return[]

def collitions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if obstacle_rect.colliderect(player):
                return False
    return True

def player_animation():
    # play walking animation if the player is on floor 
    # display the jump surface if the player jumps
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        # walking animation
        player_index += 0.1
        player_surf = player_walk[int(player_index)%2]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner') 
clock = pygame.time.Clock()
test_font = pygame.font.Font('runnerGAME/font/Pixeltype.ttf',50)
test_font_2 = pygame.font.Font('runnerGAME/font/Pixeltype.ttf',30)
game_active = False
start_time = 0

sky_surface = pygame.image.load('runnerGAME/graphics/Sky.png').convert()
ground_surface = pygame.image.load('runnerGAME/graphics/ground.png').convert()



#obstacles
#snail
snail_frame_1 = pygame.image.load('runnerGAME/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('runnerGAME/graphics/snail/snail2.png').convert_alpha()
snail_frame = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frame[int(snail_frame_index)]
#fly
fly_frame_1 = pygame.image.load('runnerGAME/graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('runnerGAME/graphics/Fly/Fly2.png').convert_alpha()
fly_frame = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frame[int(fly_frame_index)]

obstacle_rect_list = []

#player
player_walk_1 = pygame.image.load('runnerGAME/graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('runnerGAME/graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('runnerGAME/graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]


player_rect = player_surf.get_rect(midbottom = (80,300))

player_gravity = 0


#score counter
score = 0

#Intro screen
player_stand = pygame.image.load('runnerGAME/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_title = test_font.render('PixelRunner',False,(90,40,0))
game_title_rect = game_title.get_rect(center = (400,80))

text_1 = test_font_2.render('Press Space to run',False,(90,40,0))
text_1_rect = text_1.get_rect(center = (400,325))



#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,300)


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20 
            
            
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if pygame.mouse.get_pressed():
                        player_gravity = -20    
        
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_frame_1.get_rect(bottomleft = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_frame_1.get_rect(center = (randint(900,1100),190)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frame[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frame[fly_frame_index]

        else:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    # snail_rect.left = 800
                    start_time = pygame.time.get_ticks()
        
        
                
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = displayScore()

        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surface,score_rect)


        # snail_rect.x -=4
        # if(snail_rect.right < 0):
        #     snail_rect.left = 800
        # screen.blit(snail_frame_1,snail_rect)
        
        #player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        
        player_animation()
        screen.blit(player_surf,player_rect)

        #obstacle movement
        obstacle_rect_list =  obstacle_movement(obstacle_rect_list)

        #collisions
        game_active = collitions(player_rect,obstacle_rect_list)
        # if snail_rect.colliderect(player_rect):
            # game_active = False
    else:
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_title,game_title_rect)
        if score == 0:
            screen.blit(text_1,text_1_rect)   
        else:
            text_2 = test_font_2.render(f'Score: {score}',False,(90,40,0))
            text_2_rect = text_2.get_rect(center = (400,325))
            screen.blit(text_2,text_2_rect)

        


    pygame.display.update()
    clock.tick(60)