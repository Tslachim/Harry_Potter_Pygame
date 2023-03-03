import pygame
import random

pygame.init()

# Proměnné 
height = 700
width = 1000
dark_red = "#97001b"
gold = "#e3cd0a"

# Nastavení FPS rychlost celé hry 
fps = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Harry Potter and Goblet Fire")
icon = pygame.image.load("img/Hedwik.ico")
pygame.display.set_icon(icon)

# Nastavení hry
player_start_lives = 3         # Měníme v průběhu hry
player_speed = 5                # Neměníme
egg_speed = 5                   # Měníme
egg_speed_acceleration = 0.4    # Neměníme
egg_behind_border = 100         # Neměníme
goblet_speed = 35
score = 0            

player_lives = player_start_lives
egg_current_speed = egg_speed

# Fonty
font_big = pygame.font.Font("Font/Harry.ttf", 60)
font_small = pygame.font.Font("Font/Harry.ttf", 40)

# Text
game_name = font_big.render("Harry Potter and Goblet of fire", True, gold)
game_name_rect = game_name.get_rect()
game_name_rect.center = (width/2, 60)

gameover = font_big.render("Game over", True, gold)
gameover_rect = gameover.get_rect()
gameover_rect.center = (width/2, height/2 - 60)

continue_text = font_small.render("If you want to play again, press any key", True, dark_red)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width/2, height/2 + 40)

victory_text = font_big.render("You win", True, gold)
victory_text_rect = victory_text.get_rect()
victory_text_rect.center = (width/2, height/2 - 60)

# Zvuky 
pygame.mixer.music.load("media/bg-music-hp.wav")
pygame.mixer.music.play(-1, 0.0)

loose_life_sound = pygame.mixer.Sound("media/boom.wav")
loose_life_sound.set_volume(0.1)

take_egg_sound = pygame.mixer.Sound("media/take_egg.wav")
take_egg_sound.set_volume(0.1)

# Obrázky
egg_img = pygame.image.load("img/egg-icon.png")
egg_img_rect = egg_img.get_rect()
egg_img_rect.x = width + egg_behind_border
egg_img_rect.y = random.randint(198, height - 48)

harry_img = pygame.image.load("img/Harry_Potter.png")
harry_img_rect = harry_img.get_rect()
harry_img_rect.center = (35, height/2)

goblet_img = pygame.image.load("img/Goblet.png")
goblet_img_rect = goblet_img.get_rect()
goblet_img_rect.center = (width, 120)

"""broom_img = pygame.image.load("img/broom.png")
broom_img_rect = broom_img.get_rect()
broom_img_rect.x = width + egg_behind_border
broom_img_rect.y = random.randint(198, height - 48)"""

"""hedwika_img = pygame.image.load("img/Hedwika.png")
hedwika_img_rect = hedwika_img.get_rect()
hedwika_img_rect.x = width + egg_behind_border
hedwika_img_rect.y = random.randint(198, height - 48)

death_img = pygame.image.load("img/death.png")
death_img_rect = death_img.get_rect()
death_img_rect.x = width + egg_behind_border
death_img_rect.y = random.randint(198, height - 48)"""

# Hlavní cyklus
lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    # Stisk a pohyb
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and harry_img_rect.top > 120:
        harry_img_rect.y -= player_speed
    elif keys[pygame.K_DOWN] and harry_img_rect.bottom < height:
        harry_img_rect.y += player_speed

    # Pohyb vejce a nechycení vejce
    if egg_img_rect.x < 10:      # Vejce je za okrajem
        player_lives -= 1           # ubrat život
        egg_img_rect.x = width + egg_behind_border      # pozice nového vejce
        egg_img_rect.y = random.randint(198, height - 48)
        loose_life_sound.play()
    else:
        egg_img_rect.x -= egg_current_speed
    
    # Kolize s Vejcem 
    if harry_img_rect.colliderect(egg_img_rect):
        score += 1
        egg_current_speed += egg_speed_acceleration
        egg_img_rect.x = width + egg_behind_border
        egg_img_rect.y = random.randint(198, height - 48)
        take_egg_sound.play()
        goblet_img_rect.x -= goblet_speed

    # Černá obrazovka/ skrytí starých obrázků 
    screen.fill("Black")

    # Obrázky 
    screen.blit(harry_img, harry_img_rect)
    screen.blit(egg_img, egg_img_rect)
    screen.blit(goblet_img, goblet_img_rect)

    # Vypsání textů
    score_text = font_small.render(f"Score: {score}", True, dark_red)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (100, 60)

    lives_text = font_small.render(f"Lives: {player_lives}", True, dark_red)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.center = (width - 100, 60)

    gameover_score = font_small.render(f"Your score: {score}", True, gold)
    gameover_score_rect = gameover_score.get_rect()
    gameover_score_rect.center = (width/2, height/2,)

    # Tvary
    pygame.draw.line(screen, gold, (0,120), (width,120), 5)

    screen.blit(lives_text, lives_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(game_name, game_name_rect)

    # Vítězství ve hře
    if goblet_img_rect.left <= 10:
        screen.blit(victory_text, victory_text_rect)
        screen.blit(gameover_score, gameover_score_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.mixer.music.stop()
        pygame.display.update()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_start_lives
                    egg_current_speed = egg_speed
                    harry_img_rect.y = height/2
                    goblet_img_rect.center = (width, 120)
                    pause = False
                    pygame.mixer.music.play(-1, 0.0)

                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False

    # Kontrola konce hry
    if player_lives == 0:
        screen.blit(gameover, gameover_rect)
        screen.blit(gameover_score, gameover_score_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_start_lives
                    egg_current_speed = egg_speed
                    harry_img_rect.y = height/2
                    goblet_img_rect.center = (width, 120)
                    pause = False
                    pygame.mixer.music.play(-1, 0.0)

                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False


    pygame.display.update()
    clock.tick(fps)

pygame.quit()