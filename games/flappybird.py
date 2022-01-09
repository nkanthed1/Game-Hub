import random
import pygame
import sys


#func
score = 0
def make_floor():
    screen.blit(floor,(floor_x,500))
    screen.blit(floor,(floor_x+576,500))

def produce_pipe():
    pipe_difference = random.randrange(250,300,50)
    change_position = random.randrange(325,525,50)
    new_bottom_pipe = pipe.get_rect(midtop = (500,change_position))
    new_top_pipe = pipe.get_rect(midbottom = (500,change_position-pipe_difference))
    return new_bottom_pipe , new_top_pipe

def moving_pipes(x):
    for i in x:
        i.centerx -= 5
    return x

def drawing_pipes(argument):
    for i in argument:
        if i.bottom >= 700:
            screen.blit(pipe,i)
        else:
            proper_pipe_direction = pygame.transform.flip(pipe,False,True)
            screen.blit(proper_pipe_direction,i)

def checking_collisions(pipes):
    for pipe in pipes:
        if bird_box.colliderect(pipe):
            return False


    if bird_box.bottom >=500 or bird_box.top<=-100:
        return False

    return True
def score_display(state):
    if state == "main_game":
        score2 = font.render(str(int(score)), True,(0,5,0))
        score_box = score2.get_rect(center = (245,25))
        screen.blit(score2,score_box)
    if state == "game_over":
        score2 = font.render(str(int(score)), True,(0,5,0))
        score_box = score2.get_rect(center = (250,25))
        screen.blit(score2,score_box)


        high_score2 = font.render(f'High_Score: {int(high_score)}', True,(0,5,0))
        high_score_box = high_score2.get_rect(center = (250,200))
        screen.blit(high_score2,high_score_box)

def change_score(score,high_score):
    if score >= high_score:
        high_score = score
    return high_score


#vars

pygame.init()
gravity = 0.4
move_bird = 0
active_game = True
score = 0
high_score = 0

font = pygame.font.Font('04B_19.TTF',40)

screen = pygame.display.set_mode((500,1500))
frame = pygame.time.Clock()

background = pygame.transform.scale2x( pygame.image.load('background-day.png').convert())

floor = pygame.transform.scale2x(pygame.image.load('base.png').convert())
floor_x = 0

bird =pygame.transform.scale2x (pygame.image.load('bluebird-midflap.png').convert())
bird_box = bird.get_rect(center=(100,300))

pipe =pygame.transform.scale2x (pygame.image.load('pipe-green.png'))

game_over_image = pygame.transform.scale2x(pygame.image.load('message.png').convert_alpha())
game_over_box = game_over_image.get_rect(center =(250,300))


pipe_list = []
SpanningPipes = pygame.USEREVENT
pygame.time.set_timer(SpanningPipes,2000)
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE and active_game:
                move_bird = 0
                move_bird = move_bird - 10
            if i.key == pygame.K_SPACE and active_game == False:
                active_game = True
                pipe_list.clear()
                bird_box.center = (100,350)
                move_bird = 0
                score=0
        if i.type == SpanningPipes:
            pipe_list.extend(produce_pipe())


    floor_x = floor_x-1
    if floor_x <= -350:
            floor_x=0

    screen.blit(floor,(floor_x,600))
    screen.blit(background,(0,-200))
    make_floor()
    if active_game:
                
        move_bird = move_bird + gravity
        bird_box.centery += move_bird
        screen.blit(bird,bird_box)
            

        pipe_list = moving_pipes(pipe_list)
        drawing_pipes(pipe_list)

        active_game=checking_collisions(pipe_list)

        score= score+1
        score_display("main_game")
    else:
        screen.blit(game_over_image,game_over_box)
        high_score = change_score(score,high_score)
        score_display('game_over')
    pygame.display.update()
    frame.tick(50)
