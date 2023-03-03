import pygame
import random 

pygame.init()

width = 1000
height = 600

fps = 60
clock = pygame.time.Clock()

dark_red = "#bb0026"
ak_green = "#2cc321"

# Hodnoty hry
player_start_lives = 5 
mozkomor_start_speed = 2
mozkomor_speed_acceleration = 0.5
score = 0 

player_lives = player_start_lives
mozkomor_speed = mozkomor_start_speed

# Mozkomor osay
mozkomor_x = random.choice([-1, 1])
mozkomor_y = random.choice([-1, 1])

# Fonty 
big_font = pygame.font.Font("Font/Harry.ttf", 70)
small_font = pygame.font.Font("Font/Harry.ttf", 35)

# Texty
score_text = small_font.render(f"Score: {score}", True, dark_red)
score_text_rect = score_text.get_rect()
score_text_rect.topright = (width - 30, 10)
lives_text = small_font.render(f"Lives: {player_lives}", True, dark_red)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (width - 30, 40)

game_over = big_font.render("Game over", True, ak_green)
game_over_rect = game_over.get_rect()
game_over_rect.center = (width/2, height/2)

click_continue = small_font.render("Click anywhere to continue", True, ak_green)
click_continue_rect = click_continue.get_rect()
click_continue_rect.center = (width/2, height/2 + 70)



# Obrázky
background_img = pygame.image.load("img/hogwarts-castle.jpg")
background_img_rect = background_img.get_rect()
background_img_rect.topleft = (0, 0)

mozkomor_img = pygame.image.load("img/mozkomor.png")
mozkomor_img_rect = mozkomor_img.get_rect()
mozkomor_img_rect.center = (width/2, height/2)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Útok mozkomora")

# Zvuky a hudba v pozadí 
pygame.mixer.music.load("media/bg-music-hp.wav")
pygame.mixer.music.play(-1, 0.0)

success_click = pygame.mixer.Sound("media/expecto-patronum.mp3")
success_click.set_volume(0.1)
miss_click = pygame.mixer.Sound("media/miss_click.wav")
miss_click.set_volume(0.1)

lets_continue = True 
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:                    # Kliknutí myší 
            click_x = event.pos[0]
            click_y = event.pos[1]
            
            if mozkomor_img_rect.collidepoint(click_x, click_y):    # Kliknutí na mozkomora
                success_click.play()
                score += 1
                mozkomor_speed += mozkomor_speed_acceleration

                previous_x = mozkomor_x                             # odraz mozkomora po kliknutí 
                previous_y = mozkomor_y
                while previous_x == mozkomor_x and previous_y == mozkomor_y: # generování jiného směru než byl původní
                    mozkomor_x = random.choice([-1, 1]) 
                    mozkomor_y = random.choice([-1, 1]) 
                
            else:                                                       # Kliknutí mimo mozkomora                                            
                miss_click.play()
                player_lives -= 1 

    # Pohoyb mozkomora
    mozkomor_img_rect.x += mozkomor_x * mozkomor_speed
    mozkomor_img_rect.y += mozkomor_y * mozkomor_speed

    if mozkomor_img_rect.left < 0 or mozkomor_img_rect.right >= width - 0:
        mozkomor_x = -1 * mozkomor_x
    elif mozkomor_img_rect.top < 0 or mozkomor_img_rect.bottom >= height - 0:
        mozkomor_y = -1 * mozkomor_y
   

    # Obrázky 
    screen.blit(background_img, background_img_rect)
    screen.blit(mozkomor_img, mozkomor_img_rect)

    # Updatujeme skóre a životy
    score_text = small_font.render(f"Score: {score}", True, dark_red)
    lives_text = small_font.render(f"Lives: {player_lives}", True, dark_red)

    # Texty
    screen.blit(lives_text, lives_text_rect)
    screen.blit(score_text, score_text_rect)

    # Konec hry
    if player_lives == 0: 
        screen.blit(game_over, game_over_rect)
        screen.blit(click_continue, click_continue_rect)
        pygame.mixer.music.pause()
        pygame.display.update()

        pause = True
        while pause:
            score = 0
            player_lives = player_start_lives
            mozkomor_speed = mozkomor_start_speed
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    lets_continue = False
                    pause = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pause = False
                    mozkomor_img_rect.center = (random.randint(50, 950), random.randint(100, 550))
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])
                    pygame.mixer.music.play()
                    
    

    clock.tick(fps)
    pygame.display.update()

pygame.quit()