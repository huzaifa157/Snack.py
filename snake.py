import pygame
import random
import os

pygame.mixer.init() 
 #for music
pygame.init()

screen_width = 1280
screen_height = 720

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green= (0,255,0)
yellow = (255,255,0) 
cyan = (0,255,255)
dark_purple = (75, 0, 130)  # Dark Purple
N_green =(57, 255 ,20)


game_window = pygame.display.set_mode((screen_width,screen_height))



pygame.display.set_caption("Snake Game By Huzaifa")
pygame.display.update()



# Load sounds
bite_sound = pygame.mixer.Sound('bite.mp3')
game_over_sound = pygame.mixer.Sound('Game_over.wav')
pygame.mixer.music.set_volume(0.6)

# Play background music 

pygame.mixer.music.load('Music_bgm.mp3')
pygame.mixer.music.play(-1)       # -1 means the music will loop indefinitely

bg1 = pygame.image.load("Snack.bg.png")
bg1 = pygame.transform.scale(bg1, (screen_width,screen_height))

bg0 = pygame.image.load("intro.png.webp")
bg0 = pygame.transform.scale(bg0, (screen_width,screen_height))

bg2 = pygame.image.load("out.png")
bg2 = pygame.transform.scale(bg2, (screen_width,screen_height))

opacity_surface = pygame.Surface((screen_width, screen_height)).convert_alpha()
opacity_surface.set_alpha(150)
opacity_surface.fill((255, 255, 255, 50))

font = pygame.font.SysFont(None,55)
clock = pygame.time.Clock()
 

#writing text in screen like score
def text_screen(text, color,x,y):
    screen_text =font.render(text,True,color)
    game_window.blit(screen_text,[x,y])

# draw snack in the screen 
def plot_snk (game_window, color, snk_list , snack_size):
    for snack_x , snack_y in snk_list:
        pygame.draw.rect(game_window, color, [snack_x, snack_y,snack_size,snack_size]) 


def Welcome():
    
    exit = False
    while not exit:
        game_window.fill(white)
        game_window.blit(bg0,(0,0))
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                 
        pygame.display.update()
        clock.tick(30)


def game_loop():
    
    exit = False
    game_over = False

    snack_x = 45
    snack_y = 55

    velocity_x = 0
    velocity_y = 0
    velocity_init = 10

    snack_size = 35
    fps = 60

    score = 0

    snk_list = []
    snk_length = 1


    food_x = random.randint(20, screen_width - snack_size)
    food_y = random.randint(20, screen_height - snack_size)


#checking highscore file 
    if (not os.path.exists("high_score.text")):
        with open("high_score.text","w") as f:
            f.write("00")
    
    with open("high_score.text", "r") as f:
        highScore = int(f.read())
   
    while not exit:
        if game_over:
            with open("high_score.text", "w") as f :
                f .write(str(highScore))

# Game_over screen

            game_window.blit(bg2,(0,0))
            text_screen("Score: " + str( score )+   "   HighScore:" + str(   highScore),dark_purple, 420, 470)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Welcome()
                    
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        velocity_x = velocity_init
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -velocity_init
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -velocity_init
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = velocity_init
                        velocity_x = 0

                        # cheatcode
                    if event.key == pygame.K_q:
                        score+=10

            snack_x += velocity_x
            snack_y+= velocity_y
            
            if abs(snack_x - food_x)< snack_size and abs(snack_y - food_y)< snack_size:
                score+=10
                bite_sound.play()
               

                food_x = random.randint(20, screen_width - snack_size)
                food_y = random.randint(20, screen_height - snack_size)
                snk_length+=10
                if score>int(highScore):
                    highScore = score

            game_window.blit(bg1,(0,0))
            game_window.blit(opacity_surface, (0, 0))
            #snack head remains before increment

            head =[]
            head.append(snack_x)
            head.append(snack_y)
            snk_list.append(head)
            if len(snk_list)> snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
              
                game_over_sound.play()

            if snack_x < 0 or snack_x > screen_width or snack_y < 0 or snack_y > screen_height:
                game_over = True

                game_over = True
                game_over_sound.play()
               

        
            plot_snk (game_window, N_green, snk_list, snack_size)

            #food
            pygame.draw.rect(game_window, yellow, [food_x, food_y, snack_size,snack_size])
            text_screen("Score:"+ str(score)+ "   HighScore: "+str(highScore), cyan,10,5)
            

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
Welcome()
    