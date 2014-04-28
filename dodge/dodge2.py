# Dodge!
# by KidsCanCode 2014
# A Pygame clone of Run! by Thomas Palef: http://www.lessmilk.com/
# For educational purposes only
import pygame
import sys
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (52, 73, 94)
BGCOLOR = GRAY

class SpriteSheet:
    """Utility class to load and parse spritesheets"""
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey([0, 0, 0])
        return image

class Player(pygame.sprite.Sprite):
    speed = 12  # constant speed for player movement

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed_x = 0
        self.speed_y = 0
        # use bfxr.net to get a good sound
        self.explode_snd = pygame.mixer.Sound("snd/Explosion6.wav")
        # We will have animation frames for all 4 directions of movement
        # Load them from the sprite sheet and add to a list
        self.frames_l = []
        self.frames_r = []
        self.frames_u = []
        self.frames_d = []
        self.dir = 'r'
        sprite_sheet = SpriteSheet('dodgemobs.png')
        # use SpriteCutie - http://spritecutie.com/
        image = sprite_sheet.get_image(232, 33, 40, 48)
        self.frames_d.append(image)
        image = sprite_sheet.get_image(288, 33, 40, 48)
        self.frames_d.append(image)
        image = sprite_sheet.get_image(232, 101, 40, 48)
        self.frames_u.append(image)
        image = sprite_sheet.get_image(288, 101, 40, 48)
        self.frames_u.append(image)
        image = sprite_sheet.get_image(344, 33, 40, 48)
        self.frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_l.append(image)
        image = sprite_sheet.get_image(400, 101, 40, 48)
        self.frames_l.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_r.append(image)
        # set starting frame
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect()
        # mask for collisions - works much better than default rects
        self.mask = pygame.mask.from_surface(self.image)
        # start in the middle of the screen
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        # move sprite
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # animate - pick another frame every 50 pixels of movement
        if self.dir == 'r':
            frame = (self.rect.x // 50) % len(self.frames_r)
            self.image = self.frames_r[frame]
        elif self.dir == 'l':
            frame = (self.rect.x // 50) % len(self.frames_l)
            self.image = self.frames_l[frame]
        elif self.dir == 'u':
            frame = (self.rect.y // 50) % len(self.frames_u)
            self.image = self.frames_u[frame]
        else:
            frame = (self.rect.y // 50) % len(self.frames_d)
            self.image = self.frames_d[frame]
        # check for walls
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speed_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0

    def go(self, keys):
        # process keypresses (arrow keys)
        if keys[pygame.K_LEFT]:
            self.dir = 'l'
            player.speed_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.dir = 'r'
            player.speed_x = self.speed
        if keys[pygame.K_UP]:
            self.dir = 'u'
            player.speed_y = -self.speed
        if keys[pygame.K_DOWN]:
            self.dir = 'd'
            player.speed_y = self.speed

    def stop(self, dir):
        # process keyup events
        # this lets us keep moving when more than one arrow key is held down
        if dir in ('L', 'R'):
            self.speed_x = 0
        if dir in ('U', 'D'):
            self.speed_y = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.randrange(6, 10)
        self.frames = []

        # start off the screen - pick an edge
        edge = random.choice(['t', 'b', 'l', 'r'])
        if edge == 'l':
            self.dir = random.randrange(-80, 80)
            self.load_images()
            self.rect.right = 0
            self.rect.y = random.randrange(HEIGHT)
        elif edge == 'r':
            self.dir = random.randrange(100, 260)
            self.load_images()
            self.rect.left = WIDTH
            self.rect.y = random.randrange(HEIGHT)
        elif edge == 't':
            self.dir = random.randrange(190, 350)
            self.load_images()
            self.rect.bottom = 0
            self.rect.x = random.randrange(WIDTH)
        elif edge == 'b':
            self.dir = random.randrange(10, 170)
            self.load_images()
            self.rect.top = HEIGHT
            self.rect.x = random.randrange(WIDTH)

    def load_images(self):
        # load the sprites - pick one of the two mob sprites
        sprite_sheet = SpriteSheet("dodgemobs.png")
        i = random.randrange(2)
        if i == 0:
            image = sprite_sheet.get_image(24, 33, 56, 80)
            image = pygame.transform.rotate(image, -(self.dir+90) % 360)
            self.frames.append(image)
            image = sprite_sheet.get_image(112, 33, 56, 80)
            image = pygame.transform.rotate(image, -(self.dir+90) % 360)
            self.frames.append(image)
        else:
            image = sprite_sheet.get_image(16, 137, 72, 80)
            image = pygame.transform.rotate(image, -(self.dir+90) % 360)
            self.frames.append(image)
            image = sprite_sheet.get_image(104, 137, 72, 80)
            image = pygame.transform.rotate(image, -(self.dir+90) % 360)
            self.frames.append(image)
        # set the starting frame
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def update(self):
        # move sprite
        self.rect.x += self.speed * math.cos(math.radians(self.dir))
        self.rect.y += self.speed * math.sin(math.radians(self.dir))
        # change to the next frame after every 30 pixels of movement
        pos = int((self.rect.x**2 + self.rect.y**2) ** 0.5)
        frame = (pos // 30) % len(self.frames)
        self.image = self.frames[frame]

    def offscreen(self):
        # kill mob when it runs offscreen
        # added some space so new mobs that appear offscreen aren't instakilled
        if self.rect.x < -self.rect.width * 2 or self.rect.x > WIDTH + self.rect.width * 2:
            return True
        elif self.rect.y < -self.rect.height * 2 or self.rect.y > HEIGHT + self.rect.height * 2:
            return True
        else:
            return False

def show_start_screen():
    # Display the starting screen
    screen.fill(BGCOLOR)
    draw_text("DODGE!", 64, WIDTH/2, HEIGHT/4)
    draw_text("Move with the arrow keys", 24, WIDTH/2, HEIGHT/2)
    draw_text("Avoid the mobs", 24, WIDTH/2, HEIGHT*5/8)
    draw_text("Press a key to begin", 24, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    # wait for a keypress to start
    wait_for_key()
    while True:
        if wait_for_key():
            pygame.event.get()
            return

def wait_for_key():
    # utility function to pause waiting for a keypress
    # still allow Esc to exit
    # Actually, we look for KEYUP event, not KEYPRESS
    if len(pygame.event.get(pygame.QUIT)) > 0:
        pygame.quit()
        sys.exit()
    keyup_events = pygame.event.get(pygame.KEYUP)
    if len(keyup_events) == 0:
        return None
    if keyup_events[0].key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyup_events[0].key

def draw_text(text, size, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_go_screen(score):
    # display the Game Over screen
    screen.fill(BGCOLOR)
    draw_text("GAME OVER", 58, WIDTH/2, HEIGHT/4)
    text = "Score: %s" % score
    draw_text(text, 24, WIDTH/2, HEIGHT/2)
    draw_text("Press a key to begin", 24, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    # pause for a moment and then wait for key
    pygame.time.wait(500)
    wait_for_key()
    while True:
        if wait_for_key():
            pygame.event.get()
            return

def show_score(score):
    # display the score on the screen
    text = 'Score: %s' % score
    draw_text(text, 18, 40, 10)

# set screen dimensions
WIDTH = 405
HEIGHT = 540
FPS = 30
# initialize pygame and start the screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge!")
clock = pygame.time.Clock()
# create a timer to count seconds for score
pygame.time.set_timer(pygame.USEREVENT+1, 1000)
running = True
show_start_screen()
while True:
    score = 0
    # create sprite lists - one for all sprites, and one for mobs
    active_sprite_list = pygame.sprite.Group()
    mob_sprite_list = pygame.sprite.Group()
    # create the player object
    player = Player()
    active_sprite_list.add(player)
    # create some mobs
    mobs = []
    for i in range(12):
        mob = Mob()
        mobs.append(mob)
        active_sprite_list.add(mob)
        mob_sprite_list.add(mob)
    # play the game!
    while running:
        clock.tick(FPS)
        # handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # increment the score at every timer event (1 sec)
            elif event.type == pygame.USEREVENT+1:
                score += 1
            elif event.type == pygame.KEYDOWN:
                # lots of possible keydown events
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYUP:
                # keyup should stop movement, but only in that direction
                if event.key == pygame.K_LEFT:
                    player.stop('L')
                if event.key == pygame.K_RIGHT:
                    player.stop('R')
                if event.key == pygame.K_UP:
                    player.stop('U')
                if event.key == pygame.K_DOWN:
                    player.stop('D')
        # handle keys
        player.go(pygame.key.get_pressed())
        # filter mobs and create new ones
        for mob in mobs:
            if mob.offscreen():
                mobs.remove(mob)
                active_sprite_list.remove(mob)
                newmob = Mob()
                mobs.append(newmob)
                active_sprite_list.add(newmob)
                mob_sprite_list.add(newmob)
        # check for hits - using collide_mask instead of default collide_rect
        hits_list = pygame.sprite.spritecollide(player, mob_sprite_list, False,
                                                pygame.sprite.collide_mask)
        # if len(hits_list) > 0:
        #     # sorry, game over
        #     player.explode_snd.play()
        #     running = False
        # update screen
        screen.fill(GRAY)
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        show_score(score)
        pygame.display.flip()

    show_go_screen(score)
    running = True