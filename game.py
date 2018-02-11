'''
An Luong (aml4dy), Samantha Garcia (smg2jj)
'''

import pygame
import gamebox
import random

'''
required features:
- user input = right & left keys
- graphics/images
- start screen

optional features:
- enemies: bird
- collectables: apples
- health meter: three lives (display in the corner)
- music/sound effects

'''

camera = gamebox.Camera(800, 600)

# Background Stuff
top_border = gamebox.from_color(camera.x, 58, 'white', 800, 2)
bark = gamebox.from_image(camera.x, camera.y, 'https://i.pinimg.com/originals/fd/47/66/fd47660f666b3860bf9b3aee2ef0a32b.jpg')
bark.rotate(90)
splash_background = gamebox.from_image(camera.x, camera.y, "https://previews.123rf.com/images/aopsan/aopsan1205/aopsan120500032/13644442-Green-grass-background-Stock-Photo.jpg")
show_splash = True

# Sounds
caw = gamebox.load_sound('http://static1.grsites.com/archive/sounds/animals/animals010.wav')
apple_bite = gamebox.load_sound('http://pages.cs.wisc.edu/~bahls/all/Bellipax/VehicleDie2.WAV')

# Worm
worm = [gamebox.from_color(camera.x, camera.y, 'lightgreen', 20, 20)]
worm_lives = 3

# Apple & Bird Coordinates
apple_x = random.randint(60, 780)
apple_y = random.randint(80, 580)
bird_x = random.randint(60, 780)
bird_y = random.randint(80, 580)

# Apple & Bird Icons
apple = gamebox.from_image(apple_x, apple_y, "https://www.shareicon.net/data/2017/03/06/880411_apple_512x512.png")
apple.size = (40, 40)
bird = gamebox.from_image(bird_x, bird_y, 'http://cliparting.com/wp-content/uploads/2016/05/Bird-clipart-image-clip-art-cartoon-of-a-blue-bird-standing-up-2.png')
bird.size = (40, 40)

# Collectable Counter
apple_count = 0
apple_counter = gamebox.from_image(30, 29, "https://www.shareicon.net/data/2017/03/06/880411_apple_512x512.png")
apple_counter.width = 50


# Initialized Values
number = 0
speedx = 0
speedy = 0
xchange = 0
ychange = 0

# Game Over Stuff
gameover = gamebox.from_text(camera.x, camera.y - 30, 'GAME OVER', 'Arial', 100, 'white', bold=False)
gameover_lives = gamebox.from_text(camera.x, camera.y + 45, 'no more lives!', 'Arial', 20, 'white')

# Health Meter
hearts = [gamebox.from_image(camera.right - 120, camera.top + 30,'https://upload.wikimedia.org/wikipedia/commons/7/77/Heart_symbol_c00.png'),
          gamebox.from_image(camera.right - 75, camera.top + 30,'https://upload.wikimedia.org/wikipedia/commons/7/77/Heart_symbol_c00.png'),
          gamebox.from_image(camera.right - 30, camera.top + 30,'https://upload.wikimedia.org/wikipedia/commons/7/77/Heart_symbol_c00.png')]
for heart in hearts:
    heart.width = 40

def splash(keys):
    '''
    start screen
    '''
    global show_splash
    camera.draw(splash_background)
    camera.draw(gamebox.from_text(camera.x, camera.y - 90, 'Worm', 'Arial', 100, 'white', bold = True))
    camera.draw(gamebox.from_text(camera.x, camera.y - 20, 'An Luong (aml4dy) & Samantha Garcia (smg2jj)', 'Arial', 30, 'white'))
    camera.draw(gamebox.from_text(camera.x, camera.y + 20, 'use up/down/right/left keys to move the worm', "Arial", 25, 'white'))
    camera.draw(gamebox.from_text(camera.x, camera.y + 50, 'collect apples to grow, avoid birds to keep lives', 'Arial', 25, 'white'))
    camera.draw(gamebox.from_text(camera.x, camera.y + 80, 'press space bar to continue', 'Arial', 25, 'white'))

    if pygame.K_SPACE in keys:
        show_splash = False
    camera.display()

def shift():
    '''
    shifts all the x & y coordinates so that each segment of the worm ends up following the "head" of the worm (worm[0])
    '''
    global worm
    worm_x = [worm[0].x]
    worm_y = [worm[0].y]
    for i in range(1, len(worm)):
        worm_x.append(worm[i].x)
        worm_y.append(worm[i].y)
        worm[i].x = worm_x[i-1]
        worm[i].y = worm_y[i-1]

def border():
    '''
    if the worm runs off the screen, it'll appear on the other side of the screen
    (e.g. if it runs off the right, it'll appear on the left)
    '''
    global worm
    while worm[0].x <= 0:
        worm[0].x = 790

    while worm[0].x >= 799:
        worm[0].x = 1

    while worm[0].y <= 62:
        worm[0].y = 590

    while worm[0].y >= 599:
        worm[0].y = 63

def touch_apple():
    global worm, apple, new_b_y, new_b_x, new_a_y, new_a_x, bird, apple_count, apple_counter_num

    apple_counter_num = gamebox.from_text(30, 35, str(apple_count), 'Arial', 27, 'black', bold=False)

    if worm[0].touches(apple):
        apple_player = apple_bite.play()
        apple_count += 1
        worm.append(gamebox.from_color(worm[-1].x + 100, worm[-1].y, 'green', 20, 20))

        new_b_x = random.randrange(100 - bird.x, 700 - bird.x)
        new_b_y = random.randrange(160 - bird.y, 500 - bird.y)

        new_a_x = random.randrange(100 - apple.x, 700 - apple.x)
        new_a_y = random.randrange(160 - apple.y, 500 - apple.y)

        bird.move(new_b_x, new_b_y)

        # prevents apple from being too close to bird
        while abs(new_a_x - new_b_x) <= 40:
            new_a_x = random.randrange(100 - apple.x, 700 - apple.x)
        while abs(new_a_y - new_b_y) <= 40:
            new_a_y = random.randrange(160 - apple.y, 500 - apple.y)

        apple.move(new_a_x, new_a_y)

def touch_bird():
    global worm, bird, new_b_x, new_b_y, worm_lives, hearts

    if worm[0].touches(bird):
        cawplayer = caw.play()
        worm_lives -= 1

        new_b_x = random.randrange(100 - bird.x, 700 - bird.x)
        new_b_y = random.randrange(160 - bird.y, 500 - bird.y)

        # prevents the bird from being too close to the apple
        while abs(apple.x - new_b_x) <= 100:
            new_b_x = random.randrange(100 - bird.x, 700 - bird.x)
        while abs(apple.y - new_b_y) <= 100:
            new_b_y = random.randrange(160 - bird.y, 500 - bird.y)

        bird.move(new_b_x, new_b_y)

        if worm_lives > 0:
            hearts.pop(0)
        elif worm_lives <= 0:
            camera.clear('black')
            camera.draw(gameover)
            camera.draw(gameover_lives)
            gamebox.pause()

def tick(keys):
    global apple, apple_x, apple_y, apple_count, apple_counter_num
    global show_splash
    global bird, hearts, bird_x, bird_y
    global speedx, speedy
    global worm, worm_lives, xchange, ychange

    if show_splash:
        splash(keys)
        return

    camera.draw(bark)

    border()

    # prevents initial apple & bird from being too close to each other or to the initial worm
    if (abs(apple_x - bird_x) <= 90) or (abs(apple_x - worm[0].x) <= 90):
        apple_x = random.randint(65, 780)

    if (abs(apple_y - bird_y) <= 90) or (abs(apple_y - worm[0].y) <= 90):
        apple_y = random.randint(80, 580)

    if (abs(bird_x - worm[0].x) <= 90):
        bird_x = random.randint(60, 780)

    if (abs(bird_y - worm[0].y) <= 90):
        bird_y = random.randint(80, 580)

    if len(hearts) > 0:
        camera.draw(bird)
        camera.draw(apple)
        for heart in hearts:
            camera.draw(heart)

    camera.draw(top_border)

    if pygame.K_UP in keys:
        ychange = -10
        xchange = 0
    if pygame.K_DOWN in keys:
        ychange = 10
        xchange = 0
    if pygame.K_RIGHT in keys:
        xchange = 10
        ychange = 0
    if pygame.K_LEFT in keys:
        xchange = -10
        ychange = 0

    shift()
    worm[0].x += xchange
    worm[0].y += ychange

    for i in range(len(worm)):
        camera.draw(worm[i])

    touch_apple()
    camera.draw(apple_counter)
    camera.draw(apple_counter_num)
    touch_bird()

    camera.display()

gamebox.timer_loop(30, tick)



