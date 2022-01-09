import pygame 
import sys
import random


pygame.init()
frame_rate = pygame.time.Clock()



width= 500
length = 700
screen = pygame.display.set_mode((width,length))

ball = pygame.Rect(width/2,length/2,25,25)
player1 = pygame.Rect(width-20,length/2-70,15,80)
player2 = pygame.Rect(20,length/2-70,15,80) 

background = pygame.Color('grey11')
white = (255,255,255)
horizontal_ball_spped = 8 * random.choice((-1,1))
vertical_ball_spped =8 * random.choice((-1,1,))
playing_speed = 0
player2_speed = 8

def player_2_robot():
    if player2.top < ball.y:
        player2.top += player2_speed
    if player2.bottom >ball.y:
        player2.bottom -= player2_speed
    if player2.top <=0:
        player2.top = 0
    if player2.bottom >= length:
        player2.bottom = length

def ball_center():
    global vertical_ball_spped , horizontal_ball_spped
    ball.center = (width/2,length/2)
    vertical_ball_spped *= random.choice((-1,1))
    horizontal_ball_spped *= random.choice((-1,1,))




def animation_player():
    player1.y = player1.y + playing_speed
    if player1.top <=0:
        player1.top = 0
    if player1.bottom >= length:
        player1.bottom = length

def animtion_ball():
    global horizontal_ball_spped 
    global vertical_ball_spped

    ball.x += horizontal_ball_spped
    ball.y += vertical_ball_spped


    if ball.top<= 0 or ball.bottom >= length:
        vertical_ball_spped *=-1
    if ball.left<= 0 or ball.right >= width:
        ball_center()

    if ball.colliderect(player1) or ball.colliderect(player2):
        horizontal_ball_spped *=-1

while True:
    for argument in pygame.event.get():
        if argument.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if argument.type == pygame.KEYDOWN:
            if argument.key == pygame.K_DOWN:
                playing_speed = playing_speed + 8
            if argument.key == pygame.K_UP:
                playing_speed = playing_speed - 8
        if argument.type == pygame.KEYUP:
            if argument.key == pygame.K_DOWN:
                playing_speed = playing_speed - 8
            if argument.key == pygame.K_UP:
                playing_speed = playing_speed + 8


    animtion_ball()
    animation_player()
    player_2_robot()



    screen.fill(background)
    pygame.draw.ellipse(screen,white,ball)
    pygame.draw.rect(screen,white,player1)
    pygame.draw.rect(screen,white,player2)
    pygame.draw.aaline(screen,white,(width/2,0),(width/2,length))


    
    pygame.display.flip()
    frame_rate.tick(40)
