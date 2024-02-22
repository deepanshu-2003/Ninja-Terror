import pygame
from os.path import join
from levels import level_data
pygame.init()

# ------------------Game Variables-----------------------
WIDTH, HEIGHT = 900, 500
exit_game = False
FPS = 60
bg_image_no = 0
clock = pygame.time.Clock()
player_x_vel = 25
player_y_vel = 40
life = 3
level=1
background_moves=0
score_font = pygame.font.Font(None, 36)
down_movement, right_movement, left_movement, can_jump = True, True, True, True
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Terror")

# =====================Some Methods==============================

def draw_sprites(sprite_name, direction=False):
    sprite_size = {"Idle": [60, 100], "Attack": [100, 100], "Run": [80, 100], "Glide": [90, 100], "Jump": [90, 100]}
    width, height = sprite_size[sprite_name][0], sprite_size[sprite_name][1]
    sprites = []
    for i in range(10):
        sprite = pygame.image.load(join("assets", "Ninja", sprite_name, sprite_name + "__00" + str(i) + ".png")).convert_alpha()
        if direction:
            flipped_horizontal = pygame.transform.flip(sprite, True, False)
            sprite = flipped_horizontal
        resized_sprite = pygame.transform.scale(sprite, (width, height))
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        surface.blit(resized_sprite, (0, 0))
        sprites.append(surface)
    return sprites

def move_background_forward():
    global bg_image_no
    if bg_image_no == 21:
        bg_image_no = 0
    else:
        bg_image_no += 1

def move_background_backward():
    global bg_image_no
    if bg_image_no == 0:
        bg_image_no = 21
    else:
        bg_image_no -= 1

# ---------------- Player class---------------------------
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.rect_x = self.rect_y = 0
        self.direction = "right"
        self.animation_speed = 1
        self.animation_count = 0
        self.fall_count = 1
        self.sprites = draw_sprites("Idle")
        self.mask = None

    def stay(self):
        if self.animation_count != 0:
            if self.direction == "left":
                self.sprites = draw_sprites("Idle", True)
            else:
                self.sprites = draw_sprites("Idle")

    def move_left(self):
        global background_moves
        if left_movement:
            if player.rect.left - 100 < 200:
                background_moves-=1
                move_background_backward()
                for i in game_objects:
                    i.x += player_x_vel
                for j in coins:
                    j.x += player_x_vel
                home.x+=player_x_vel
                for i in spikes:
                    i.x+=player_x_vel
            else:
                self.rect_x -= player_x_vel
        self.sprites = draw_sprites("Run", True)
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self):
        global background_moves
        if right_movement:
            if player.rect.right + 400 > WIDTH:
                background_moves+=1
                move_background_forward()
                for i in game_objects:
                    i.x -= player_x_vel
                for j in coins:
                    j.x -= player_x_vel
                home.x-=player_x_vel
                for i in spikes:
                    i.x-=player_x_vel
            else:
                self.rect_x += player_x_vel
        self.sprites = draw_sprites("Run")
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_down(self):
        global down_movement
        if down_movement:
            self.rect_y += player_y_vel  # Gravity implementation
            if self.direction == "left":
                self.sprites = draw_sprites("Jump", True)
            else:
                self.sprites = draw_sprites("Jump")

    def jump(self, jump_count):
        global down_movement, can_jump
        if can_jump:
            if self.direction == "left":
                self.sprites = draw_sprites("Jump", True)
            else:
                self.sprites = draw_sprites("Jump")
            self.rect_y -= player_y_vel
            if jump_count < 4:
                if possible_up(self, game_objects):
                    draw_assets()
                    self.jump(jump_count + 1)
            down_movement = True

    def attack(self):
        if self.direction == "left":
            self.sprites = draw_sprites("Attack", True)
        else:
            self.sprites = draw_sprites("Attack")
        if self.animation_count < 9:
            draw_assets()
            self.attack()

    def draw(self):
        animation_index = self.animation_count % 10
        self.mask = pygame.mask.from_surface(self.sprites[animation_index])
        self.rect = self.sprites[animation_index].get_rect()
        self.rect.x, self.rect.y = self.rect_x, self.rect_y
        window.blit(self.sprites[animation_index], (self.rect.x, self.rect.y))
        if self.animation_count > 9:
            self.animation_count = 0
        else:
            self.animation_count += self.animation_speed

# -----------------------------Object class ---------------------------------------------
class Tiles(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        width, height = 50, 50
        self.x, self.y = x, y
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.image = pygame.image.load(join("assets", "Tiles", name + ".png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.blit(self.image, (0, 0))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self):
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.surf)
        window.blit(self.surf, (self.x, self.y))

# ---------------------OBJECT ----------------------------------
class Object(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height):
        self.x, self.y = x, y
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.image = pygame.image.load(join("assets", "Object", name + ".png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.blit(self.image, (0, 0))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self):
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.surf)
        window.blit(self.surf, (self.x, self.y))

# --------------------home class--------------------------
class Home(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x, self.y = x, y
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.image.load(join("assets", "Object", "home.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.blit(self.image, (0, 0))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self):
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.surf)
        window.blit(self.surf, (self.x, self.y))

# ----------------------Coin class -------------------------
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        width, height = 30, 30
        self.x, self.y = x, y
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.image.load(join("assets", "Object", "coin.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.blit(self.image, (0, 0))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self):
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.surf)
        window.blit(self.surf, (self.x, self.y))

# --------------------Spikes class--------------------
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x, self.y = x, y
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.image.load(join("assets", "Object", "spikes.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.blit(self.image, (0, 0))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self):
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.surf)
        window.blit(self.surf, (self.x, self.y))

# -------------------Heart class-------------------------
class HeartIcon(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x, self.y = x, y
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.image.load(join("assets", "Object", "heart.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.blit(self.image, (0, 0))
        self.rect = self.surf.get_rect()

    def draw(self):
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        window.blit(self.surf, (self.x, self.y))

# -----------------------Drawing our background---------------------
def draw_background(width, height, x, y, *args):
    path = ""
    for i in args:
        path = join(path, i)
    image = pygame.image.load(path)

    # Resize the image while preserving its aspect ratio
    resized_image = pygame.transform.scale(image, (width, height))

    window.blit(resized_image, (x, y))  # (0,0) --> position

# ----------------------------------creating objects ---------------------------------------
player = Player(100, 100, 50, 50)
tile_x, tile_y = 0, 400
score = 0
# ----------------------level 1 ---------------------
heart_icon = HeartIcon(WIDTH - 50, 10, 30, 30)



def generate_tiles(tile_type, start_x, start_y, iterations, increment):
    tiles = []
    for i in range(iterations):
        tile = Tiles(tile_type, start_x + i * increment, start_y)
        tiles.append(tile)
    return tiles

def generate_positions(start_x, start_y, iterations, increment):
    positions = []
    for i in range(iterations):
        positions.append((start_x + i * increment, start_y))
    return positions

def load_level(level_data):
    game_objects = []
    coins = []
    spikes = []

    # Load tiles
    for tile_config in level_data.get("tiles", []):
        tile_type = tile_config["type"]
        start_x = tile_config["start_x"]
        start_y = tile_config["start_y"]
        iterations = tile_config.get("iterations", 1)
        direction = tile_config.get("direction", "increment")
        amount = tile_config.get("amount", 50)

        if direction == "increment":
            increment = amount
        else:
            increment = -amount

        tiles = generate_tiles(tile_type, start_x, start_y, iterations, increment)
        game_objects.extend(tiles)

    # Load coins
    for coin_config in level_data.get("coins", []):
        start_x = coin_config["start_x"]
        start_y = coin_config["start_y"]
        iterations = coin_config.get("iterations", 1)
        direction = coin_config.get("direction", "increment")
        amount = coin_config.get("amount", 30)

        if direction == "increment":
            increment = amount
        else:
            increment = -amount

        coin_positions = generate_positions(start_x, start_y, iterations, increment)
        coins.extend([Coin(x, y) for x, y in coin_positions])

    # Load spikes
    for spike_config in level_data.get("spikes", []):
        start_x = spike_config["start_x"]
        start_y = spike_config["start_y"]
        iterations = spike_config.get("iterations", 1)
        direction = spike_config.get("direction", "increment")
        amount = spike_config.get("amount", 50)

        if direction == "increment":
            increment = amount
        else:
            increment = -amount

        spike_positions = generate_positions(start_x, start_y, iterations, increment)
        spikes.extend([Spike(x, y, 50, 50) for x, y in spike_positions])

    # Load home
    home_config = level_data.get("home", {})
    home = Home(home_config["start_x"], home_config["start_y"],
                home_config["width"], home_config["height"])

    return game_objects, coins, spikes, home

game_objects,coins,spikes,home=load_level(level_data[level-1]) 






# ------------------------collision Control---------------------
def home_collision(pl, h):
    global level,game_objects,coins,spikes,home,background_moves,exit_game
    if pygame.sprite.collide_mask(pl, h) and player.rect.left > h.rect.left+45:
        draw_assets()
        font = pygame.font.Font(None, 74)
        text = font.render("Victory!!", True, (255,0,0))
        score_show = font.render("Your score : "+str(score), True, (255,0,0))
        level_show = font.render("Level "+str(level)+" Passed", True, (255,0,0))
        window.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 -200))
        window.blit(score_show, (WIDTH // 2 - 150, HEIGHT // 2 -150))
        window.blit(level_show, (WIDTH // 2 - 150, HEIGHT // 2 -100))
        pygame.display.update()
        pygame.time.delay(2000)  # Display the victory message for 2 seconds
        if(level==2):
            exit_game=True
        else:
            level+=1
            background_moves=0
            player.rect_x,player.rect_y=0,0
            game_objects,coins,spikes,home=load_level(level_data[level-1])

def spike_collision(pl, spikes):
    global life,background_moves
    for spike in spikes:
        if pygame.sprite.collide_mask(pl, spike):
            life -= 1
            if life > 0:
                # Reset player position to the initial position
                player.rect_x, player.rect_y = 100, 100
                for i in range(background_moves):
                    for i in game_objects:
                        i.x += player_x_vel
                    for j in coins:
                        j.x += player_x_vel
                    home.x+=player_x_vel
                    for i in spikes:
                        i.x+=player_x_vel
                background_moves=0
            else:
                game_over()

def game_over():
    global exit_game
    # Display game over message and handle exit or restart
    # You can add your game over logic here
    font = pygame.font.Font(None, 74)
    text = font.render("OOPS!! Game Over...", True, (255,0,0))
    score_show = font.render("Your score : "+str(score), True, (255,0,0))
    window.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 -200))
    window.blit(score_show, (WIDTH // 2 - 150, HEIGHT // 2 -150))
    pygame.display.update()
    pygame.time.delay(3000)  #Display game over for 2 seconds
    exit_game = True
def possible_down(pl, args):
    movement = True
    for i in args:
        pl.rect.bottom += player_y_vel
        if pygame.sprite.collide_mask(pl, i):
            movement = False
            break
        pl.rect.bottom -= player_y_vel
    return movement

def possible_up(pl, args):
    movement = True
    for i in args:
        pl.rect.top -= player_y_vel
        if pygame.sprite.collide_mask(pl, i):
            movement = False
            break
        pl.rect.top += player_y_vel
    return movement

def possible_right(pl, args):
    movement = True
    for i in args:
        pl.rect.right += player_x_vel
        if pygame.sprite.collide_mask(pl, i):
            movement = False
            break
        pl.rect.right -= player_x_vel
    return movement

def possible_left(pl, args):
    movement = True
    for i in args:
        pl.rect.left -= player_x_vel
        if pygame.sprite.collide_mask(pl, i):
            movement = False
            break
        pl.rect.left += player_x_vel
    return movement
def display_level_text():
    global level
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level {level}", True, (255, 0, 0))
    window.blit(text, (WIDTH  - 250, HEIGHT - 490))

def vertical_collision(pl, args):
    global down_movement, right_movement, can_jump
    if possible_up(pl, args):
        can_jump = True
    else:
        can_jump = False
    if possible_down(pl, args):
        down_movement = True
    else:
        down_movement = False
    for i in args:
        if pygame.sprite.collide_mask(pl, i):
            if not possible_down(pl, args):
                player.rect.bottom = i.rect.top
                player.rect_x, player.rect_y = player.rect.x, player.rect.y
                down_movement = False

def horizontal_collision(pl, args):
    global right_movement, left_movement
    if possible_right(pl, args):
        right_movement = True
    else:
        right_movement = False
    if possible_left(pl, args):
        left_movement = True
    else:
        left_movement = False

def coin_collision(pl, coins):
    global score
    for coin in coins:
        if pygame.sprite.collide_mask(pl, coin):
            coins.remove(coin)
            score += 10

# -------------------Drawing our assets-----------------------------
def draw_assets():
    draw_background(WIDTH, HEIGHT, 0, 0, "assets", "Background", f"background{bg_image_no}.jpg")
    player.draw()
    for i in game_objects:
        i.draw()
    for coin in coins:
        coin.draw()
    home.draw()
    for spike in spikes:
        spike.draw()
    # Draw life
    for i in range(life):
        heart_icon.x = WIDTH - 50 - i * 40  # Adjust the spacing
        heart_icon.draw()

    score_text = score_font.render(f"Score: {score}", True, (255, 0, 0))
    window.blit(score_text, (10, 10))  # Adjust the position as needed
    display_level_text()
    pygame.display.update()

# --------------------------------------------------------------------


while not exit_game:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
            break

    player.move_down()
    draw_assets()
    player.stay()
    vertical_collision(player, game_objects)
    horizontal_collision(player, game_objects)
    coin_collision(player, coins)
    home_collision(player, home)  # Check collision with the home object
    spike_collision(player, spikes)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()

    if keys[pygame.K_RIGHT]:
        player.move_right()

    if keys[pygame.K_UP]:
        player.animation_count = 0
        player.jump(0)

    if keys[pygame.K_SPACE]:
        player.animation_count = 0
        player.attack()

pygame.quit()
quit()
