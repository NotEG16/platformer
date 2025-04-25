import json

import pygame as pg
import pytmx

pg.init()
pg.mixer.init() 


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 1.5

font = pg.font.Font(None, 36)


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.load_animation()
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.bottom = y + 80

        self.current_image = 0
        self.interval = 200
        self.timer = pg.time.get_ticks()

    def load_animation(self):
        tile_size = 64
        tile_scale = 4

        self.images = []

        num_images = 8
        spritesheet = pg.image.load("sprites/Green Portal Sprite Sheet.png")


        for i in range (num_images):
            x = i * tile_size 
            y = 0 
            rect = pg.Rect(x, y, tile_size, tile_size) 

            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

            self.images.append(image)


    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:    
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.timer = pg.time.get_ticks()


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.load_animation()
        self.image = self.images[0]
        self.rect = self.image.get_rect()


        self.rect.x = x
        self.rect.y = y

        self.current_image = 0
        self.interval = 200
        self.timer = pg.time.get_ticks()

    def load_animation(self):
        tile_size = 16
        tile_scale = 4

        self.images = []

        num_images = 5
        spritesheet = pg.image.load("sprites/Coin_Gems/MonedaD.png")


        for i in range (num_images):
            x = i * tile_size 
            y = 0 
            rect = pg.Rect(x, y, tile_size, tile_size) 

            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

            self.images.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:    
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.timer = pg.time.get_ticks()


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()

        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE


class Crab(pg.sprite.Sprite):
    def __init__(self, map_pixel_width, map_pixel_height, start_pos, end_pos):
        super().__init__()

        self.load_animations()
        self.image = self.animation[0]
        self.current_image = 0
        self.current_animation = self.animation

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos # characeter inital position
        
        self.right_edge = start_pos[0]
        self.left_edge = end_pos[0] + self.image.get_width()
       
        

        #speed and gravity
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_pixel_width * TILE_SCALE
        self.map_height = map_pixel_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 300

        self.direction = "right"
        self.hp = 1


    def load_animations(self):
        tile_size = 32
        tile_scale = 4

        self.animation = []

        image = pg.image.load("sprites/Sprite Pack 2/9 - Snip Snap Crab/Movement_(Flip_image_back_and_forth) (32 x 32).png")
        image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

        

        self.animation.append(image)
        self.animation.append(pg.transform.flip(image, True, False))


    def update(self, platforms):

    
       
        if self.rect.left <= self.right_edge:
            self.direction = "right"
            self.velocity_x = 2
        elif self.rect.right >= self.left_edge:
            self.direction = "left"
            self.velocity_x = -2

            

        new_x = self.rect.x + self.velocity_x    
        if 0  <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x        
        

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

       
    

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
                
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.velocity_x = 0

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
                self.velocity_x = 0



        #animations
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Octopus(pg.sprite.Sprite):
    def __init__(self, map_pixel_width, map_pixel_height, start_pos, end_pos):
        super().__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_left
        self.image = self.current_animation[0]
        self.current_image = 0
        
        self.timer = pg.time.get_ticks()
        self.interval = 300

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos # characeter inital position
        
        self.right_edge = start_pos[0]
        self.left_edge = end_pos[0] + self.image.get_width()
       
        

        #speed and gravity
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_pixel_width * TILE_SCALE
        self.map_height = map_pixel_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 300

        self.direction = "left"

        self.hp = 1

       

    def load_animations(self):
        tile_size = 16
        tile_scale = 4

        self.idle_animation_left = []
        num_images = 2


        spritesheet = pg.image.load("sprites/Sprite Pack 2/3 - Octi/Idle_&_Movement (16 x 16).png")
        

        for i in range (num_images):
            x = i * tile_size
            y = 0

            rect = pg.Rect(x, y, tile_size, tile_size)    


            image = spritesheet.subsurface(rect)
        image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

        self.idle_animation_left.append(image)

        self.idle_animation_left.append(image)
        self.idle_animation_right = [pg.transform.flip(image, True, False) for image in self.idle_animation_left]

        self.move_animation_left = []
        spritesheet = pg.image.load("sprites/Sprite Pack 2/3 - Octi/Idle_&_Movement (16 x 16).png")

        num_images = 2

        for i in range(num_images):
            x = i * tile_size
            y = 0

            rect = pg.Rect(x, y, tile_size, tile_size)

            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

            self.move_animation_left.append(image)
            self.move_animation_right = [pg.transform.flip(image, True, False) for image in self.move_animation_left]


    def update(self, platforms):

    
       
        if self.rect.left <= self.right_edge:
            self.direction = "right"
            self.velocity_x = 2
        elif self.rect.right >= self.left_edge:
            self.direction = "left"
            self.velocity_x = -2

        if self.direction == "left":
            self.current_animation = self.move_animation_left
        elif self.direction == "right":
            self.current_animation = self.move_animation_right
    



        new_x = self.rect.x + self.velocity_x    
        if 0  <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x        
        

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

       
    

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
                
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.velocity_x = 0

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
                self.velocity_x = 0



        #animations
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10


        self.image = pg.image.load("sprites/ball.png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()

        if self.direction == "right":
            self.rect.x = player_rect.right - 50
        else:
            self.rect.x = player_rect.left + 50

        self.rect.y = player_rect.centery + 15


    def update(self):

        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed   
            

class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super().__init__()

        #continuing animation
        self.load_animation()
        self.current_animation = self.idle_animation_right
        self.image = self.current_animation[0]
        self.current_image = 0


        self.timer = pg.time.get_ticks()
        self.interval = 200

        self.direction = "right"

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

        #initial speed and gravity:
        self.velocity_x = 0
        self.velocity_y = 0

        self.gravity = 2

        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000       


    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()
            

    def load_animation(self):
        tile_size = 32
        tile_scale = 4

        self.idle_animation_right = []
        num_images = 5

        spritesheet = pg.image.load("sprites/Sprite Pack 3/3 - Robot J5/Idle (32 x 32).png")


        for i in range (num_images):
            x = i * tile_size # starter coordinates x of the images sprite
            y = 0 #starter coordinates y of the images sprite

            rect = pg.Rect(x, y, tile_size, tile_size) #rectangle that says how long is image

            #"cut out" the player from the picture
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

            self.idle_animation_right.append(image) # adding image to list  

            self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        #movement animetion
        self.move_animation_right = []
        spritesheet = pg.image.load("sprites/Sprite Pack 3/3 - Robot J5/Running (32 x 32).png")
        num_images = 3

        for i in range (num_images):
            x = i * tile_size
            y = 0

            rect = pg.Rect(x, y, tile_size, tile_size) 

            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))

            self.move_animation_right.append(image)

            self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]

       
    def update(self, platforms):

        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
            

        if keys[pg.K_a]:
            self.velocity_x = -10
            if self.current_animation != self.move_animation_left:    
                self.current_animation = self.move_animation_left
            self.direction = "left"
        elif keys[pg.K_d]:
            self.velocity_x = 10
            if self.current_animation != self.move_animation_right:
                self.current_animation = self.move_animation_right
            self.direction = "right"
        else:
            if self.current_animation == self.move_animation_left:
                self.current_animation  = self.idle_animation_left
                self.direction = "left"
                self.current_image = 0
            elif self.current_animation == self.move_animation_right:
                self.current_animation = self.idle_animation_right
                self.current_image = 0
                self.direction = "right"
            
            
            self.velocity_x = 0

       

        #BORDER
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x
 

        #gravitation
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        #collision with platforms
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
                
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.velocity_x = 0

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
                self.velocity_x = 0


        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

    def jump(self):
        self.velocity_y = -45 
        self.is_jumping = True      


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Platformer")
        self.level = 1

         

        self.setup()
        


    def setup(self):
        self.collected_coins = 0
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False

        self.background = pg.image.load("background.png")

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.portals = pg.sprite.Group()

        self.pick_up_sound = pg.mixer.Sound("coin_pick_up.wav")
        self.pick_up_sound.set_volume(0.3)

      

        self.tmx_map = pytmx.load_pygame(f"maps/level{self.level}.tmx")

        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        
        
        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)

        
        


        for layer in self.tmx_map:
            if layer.name == "platforms":
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                        
                    if tile:
                        platform = Platform(tile,
                                            x * self.tmx_map.tilewidth,
                                            y * self.tmx_map.tileheight,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
            if layer.name == "coins":
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        coin = Coin(x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight * TILE_SCALE)

                        self.all_sprites.add(coin)
                        self.coins.add(coin)
            if layer.name == "portal":
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        portal = Portal(x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight * TILE_SCALE)
                        
                        self.all_sprites.add(portal)
                        self.portals.add(portal)


        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4


        with open(f"maps/level{self.level}_enemies.json", "r") as json_file:
            data = json.load(json_file)

        for enemy in data["enemies"]:
            if enemy["name"] == "Crab":
                x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                crab = Crab(self.map_pixel_width, self.map_pixel_height, [x1, y1], [x2, y2])
                self.enemies.add(crab)
                
               
                self.all_sprites.add(crab)
                

            if enemy["name"] == "Octopus":
                x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth    

                octopus = Octopus(self.map_pixel_width, self.map_pixel_height, [x1, y1], [x2, y2])

                self.enemies.add(octopus)
                self.all_sprites.add(octopus)

            


        self.run()

    
    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            pg.display.flip()
        pg.quit()
        quit()


    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

            if self.mode == "game_over":
                if event.type == pg.KEYDOWN:
                    self.setup() 

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LSHIFT:
                    ball = Ball(self.player.rect, self.player.direction)
                    self.balls.add(ball)
                    self.all_sprites.add(ball)


    def update(self):

        if self.player.hp <= 0:
            self.mode = "game_over"
            return
        
        
        if self.player.rect.top >= self.map_pixel_height:
            self.player.hp = 0
            return

        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()
               


        self.player.update(self.platforms)
        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)

        self.balls.update()
        self.coins.update()
        self.portals.update()


        pg.sprite.groupcollide(self.balls, self.enemies, True, True)

        pg.sprite.groupcollide(self.balls, self.platforms, True, False)


        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.collected_coins += 1
            self.pick_up_sound.play()
            
            

        
        for ball in self.balls.sprites():
            if ball.rect.left <= 0:
                ball.kill()
            elif ball.rect.right >= self.map_pixel_width:
                ball.kill()


        hits = pg.sprite.spritecollide(self.player, self.portals, False)
        for hit in hits:
            if self.collected_coins >= 5:
                self.level += 1
                self.setup()
            



        #camera continuation
        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))
        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))

    
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        pg.draw.rect(self.screen, pg.Color("red"), (10, 10, self.player.hp * 10, 10))
        pg.draw.rect(self.screen,pg.Color("black"), (10, 10, 100, 10), 1)

        if self.mode == "game_over":
            text = font.render(str("Game Over"), True, "red")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)   

        coin_screen = font.render(str(f"Coins: {self.collected_coins}"), True, "black")
        coin_rect = coin_screen.get_rect(center=(50, 50))
        self.screen.blit(coin_screen, coin_rect)  

                     

if __name__ == "__main__":
    game = Game()