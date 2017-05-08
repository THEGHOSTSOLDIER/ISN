import os
import sys
import pygame as pg

CAPTION = "GAME"
SCREEN_SIZE = (700, 500)

class Physics(object):

    def __init__(self):
        self.x_vel = self.y_vel = 0
        self.grav = 0.4
        self.fall = False
      
    def physics_update(self):
        if self.fall:
            self.y_vel += self.grav
        else:
            self.y_vel = 0



class Player(Physics, pg.sprite.Sprite):

    def __init__(self, location, speed):
        Physics.__init__(self)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("pekka.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect(topleft = location)
        self.speed = speed
        self.jump_power = -12.0
        self.jump_cut_magnitude = -3.0
        self.on_moving = False
        self.collide_bellow = False
        self.turn_left = False
        self.turn_right = False
        self.first_right = False

    def check_keys(self, keys):
        self.x_vel = 0
        if keys[pg.K_LEFT]:
            self.x_vel -= self.speed
            self.turn_right = False
            if self.turn_left == False:
                self.image = pg.transform.flip(self.image, 12, 0)
                self.turn_left = True
                self.first_right = True
        if keys[pg.K_RIGHT]:
            self.x_vel += self.speed
            self.turn_left = False
            if self.turn_right == False and self.first_right == True:
                self.image = pg.transform.flip(self.image, 12, 0)
                self.turn_right = True

    def get_position(self, obstacles):
        if not self.fall:
            self.check_falling(obstacles)
        else:
            self.fall = self.check_collisions((0, self.y_vel), 1, obstacles)
        if self.x_vel:
            self.check_collisions((self.x_vel, 0), 0, obstacles)

    def check_falling(self, obstacles):
        if not self.collide_below:
            self.fall = True
            self.on_moving = False


    def check_collisions(self, offset, index, obstacles):
        unaltered = True
        self.rect[index] += offset[index]
        while pg.sprite.spritecollideany(self, obstacles):
            self.rect[index] += (1 if offset[index]<0 else -1)
            unaltered = False
        return unaltered


            

    def check_above(self, obstacles):
        self.rect.move_ip(0, -1)
        collide = pg.sprite.spritecollideany(self, obstacles)
        self.rect.move_ip(0, 1)
        return collide

    def check_below(self, obstacles):
        self.rect.move_ip((0, 1))
        collide = pg.sprite.spritecollide(self, obstacles, False)
        self.rect.move_ip((0, -1))
        return collide

    def jump(self, obstacles):

        if not self.fall and not self.check_above(obstacles):
            self.y_vel = self.jump_power
            self.fall = True
            self.on_moving = False
            #sound.play()

    def jump_cut(self):
        if self.fall:
            if self.y_vel < self.jump_cut_magnitude:
                self.y_vel = self.jump_cut_magnitude

    def pre_update(self, obstacles):
        self.collide_below = self.check_below(obstacles)

    def update(self, obstacles, keys):
        self.check_keys(keys)
        self.get_position(obstacles)
        self.physics_update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Block(pg.sprite.Sprite):

    def __init__(self, color, rect):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.image =pg.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = "normal"

class Control(object):

    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 100.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.player = Player((50, 875), 4)
        self.viewport = self.screen.get_rect()
        self.level = pg.Surface((1000,1000)).convert()
        self.level_rect = self.level.get_rect()
        self.obstacles = self.make_obstacles()
        self.ennemy_image = pg.image.load("pekka.png").convert_alpha()
        self.ennemy_image = pg.transform.scale(self.ennemy_image, (80, 80))
        self.ennemy_rect = self.ennemy_image.get_rect(topleft=(600, 750))
        self.ennemy = self.make_ennemy()

    def make_obstacles(self):
        walls = [Block(pg.Color("black"), (0, 980, 1000, 20)),
                 Block(pg.Color("black"), (0, 0, 20, 1000)),
                 Block(pg.Color("black"), (980, 0, 20, 1000))]

        static = [Block(pg.Color("darkgreen"), (250, 850, 200, 30)),
                  Block(pg.Color("darkgreen"), (600, 750, 200, 30)),
                  Block(pg.Color("darkgreen"), (200, 600, 200, 30)),
                  Block(pg.Color("darkgreen"), (650, 500, 200, 30))]

        return pg.sprite.Group(walls, static)

    def update_viewport(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump(self.obstacles)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()

    def update(self):
        self.keys = pg.key.get_pressed()
        self.player.pre_update(self.obstacles)
        self.player.update(self.obstacles, self.keys)
        self.update_viewport()

    def draw(self):
        self.level.fill(pg.Color("lightblue"))
        self.obstacles.draw(self.level)
        self.player.draw(self.level)
        self.screen.blit(self.level, (0, 0), self.viewport)

                    

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)

class ennemy(object):

    def __init__(self):
        self.image = pg.image.load("pekka.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(topleft=(600, 750))
    def aff(self):
        self.level.blit(self.image, self.ennemy_rect)

            
"""if __name__ == "__main__":"""
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.mouse.set_visible(False)
pg.display.set_caption(CAPTION)
pg.display.set_mode(SCREEN_SIZE)
#sound = pg.mixer.Sound("big_jump.ogg")
run = Control()
run.main_loop()
pg.quit()
sys.exit()

