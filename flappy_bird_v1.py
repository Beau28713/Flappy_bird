import pygame, sys
import random
import Window# My window mod

main_screen = Window.window(576, 800, "Sprite")

BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0) 
BLUE = pygame.Color(0,0,255)

# Variables
gravity = .25
bird_mov_down = 0
game_playing = True
FPS = 100
frame_rate = pygame.time.Clock()
score = 0
final_score = 0

# Fonts
game_font = pygame.font.Font(r'Assets\04B_19.TTF', 40)

back_ground = pygame.image.load(r'Assets\flappy-bird-assets\sprites\background-day.png').convert()#  Convert runs code more smothly
back_ground = pygame.transform.scale2x(back_ground)

floor_surface = pygame.image.load(r'Assets\flappy-bird-assets\sprites\base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_surface_x_pos = 0

bird_surface = []
bird_surface.append(pygame.transform.scale2x(pygame.image.load(r'Assets\flappy-bird-assets\sprites\bluebird-downflap.png').convert()))
bird_surface.append(pygame.transform.scale2x(pygame.image.load(r'Assets\flappy-bird-assets\sprites\bluebird-midflap.png').convert()))
bird_surface.append(pygame.transform.scale2x(pygame.image.load(r'Assets\flappy-bird-assets\sprites\bluebird-upflap.png').convert()))
current_bird_image = 0
bird_image = bird_surface[current_bird_image]
bird_surface_rect = bird_image.get_rect(center= (100, 400))
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

pipe_surface = pygame.image.load(r'Assets\flappy-bird-assets\sprites\pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [300, 400, 500]

# Create a user event to spawn the pipes and then set a timer to do it 
# Every 1.2 seconds (1200mS)
PIPESPAWN = pygame.USEREVENT
pygame.time.set_timer(PIPESPAWN, 1200)

def draw_floor_surface():
    main_screen.blit(floor_surface, (floor_surface_x_pos, 750))
    main_screen.blit(floor_surface , (floor_surface_x_pos + 576, 750))

def pipe_create():
    random_pipe_height = random.choice(pipe_height)
    build_top_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_height))
    build_bottom_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_height - 300))
    return build_bottom_pipe, build_top_pipe

def move_pipe(list_of_pipes_rects):
    for pipe_rect in list_of_pipes_rects:
        pipe_rect.centerx -= 5# Decrese the center x position of each rect by 5 each time
    return list_of_pipes_rects

def draw_pip(list_of_pipes_rects):
    for pipe_rect in list_of_pipes_rects:
        if pipe_rect.bottom >= 800:
            main_screen.blit(pipe_surface, pipe_rect)

        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            main_screen.blit(flip_pipe, pipe_rect)

def check_collisions(list_of_pipes_rect):
    for pipes_rect in list_of_pipes_rect:
        if bird_surface_rect.colliderect(pipes_rect):
            return False

    if bird_surface_rect.top < -50 or bird_surface_rect.bottom > 750:
       return False

    return True

def bird_beak_up_down(bird):
    bird_rotated = pygame.transform.rotate(bird, bird_mov_down *2)
    return bird_rotated

def animate_bird():
    new_bird_image = bird_surface[current_bird_image]
    new_bird_image_rect = new_bird_image.get_rect(center = (100, bird_surface_rect.centery))
    return new_bird_image, new_bird_image_rect

def game_score():
    score_surface = game_font.render(str(int(score)), True, (255,255,255))
    score_surface_rect = score_surface.get_rect(center=(288, 100))
    main_screen.blit(score_surface, score_surface_rect)

def game_over():
    game_over_surface = game_font.render('Game Over', True, (255,255,255))
    game_over_surface_rect = game_over_surface.get_rect(center=(288, 200))
    main_screen.blit(game_over_surface, game_over_surface_rect)

    final_score_surface = game_font.render(str(int(final_score)), True, (255,255,255))
    final_score_surface_rect = final_score_surface.get_rect(center=(288, 100))
    main_screen.blit(final_score_surface, final_score_surface_rect)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(), sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_playing:
                bird_mov_down = 0
                bird_mov_down -= 10
            if event.key == pygame.K_SPACE and game_playing == False:
                game_playing = True
                pipe_list.clear()
                bird_surface_rect.center = (100, 400)
                bird_mov_down = 0

        if event.type == PIPESPAWN:
            pipe_list.extend(pipe_create())

        if event.type == BIRD_FLAP:
            if current_bird_image < 2:
                current_bird_image += 1
            else:
                current_bird_image = 0

            bird_image, bird_surface_rect = animate_bird()
   
    pygame.display.flip()
    
    main_screen.blit(back_ground, (0,0))

    if game_playing :
        # Bird
        bird_mov_down += gravity
        bird_surface_rect.centery += bird_mov_down
        rotate_beak_up_down = bird_beak_up_down(bird_image)
        main_screen.blit(rotate_beak_up_down, bird_surface_rect)
        game_playing = check_collisions(pipe_list)

        #Pipe
        pipe_list = move_pipe(pipe_list)
        draw_pip(pipe_list)

        # Score
        score += .01
        final_score = score
        game_score()

    if not game_playing:
        game_over()
        score = 0
        

    # Floor
    floor_surface_x_pos -= 1
    draw_floor_surface()

    if floor_surface_x_pos <= -576:
        floor_surface_x_pos = 0
    
    frame_rate.tick(FPS)