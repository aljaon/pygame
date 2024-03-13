import pygame
import numpy as np
import sys
from math import sqrt, cos, sin

#Enemy square
min_time_between_Enemy_spawn = 300
max_enemies = 20
Enemy_speed = 0.3
Enemy_size = 50
Enemy_hp_scale = 10
Enemy_spawn_scale = 10

#Player square
player_speed = 1.0
player_size = 20

#Upgrades
damage_upgrade_cost = 500
weapon_damage_upgrade_multiplier = 1.3

firing_speed_cost = 500
delay_decrease = 2
base_delay = 1024
min_delay = 64
speed_increase = 0.2

weapon_upgrade_cost = 1500

#Enemy that bounces around window
class Enemy():
    
    def __init__(self, col, size_x, size_y, from_x, from_y, to_x, to_y, speed, health):
        
        #Enemy Colour
        self.colour = col
        
        #Enemy size
        self.size_x = size_x
        self.size_y = size_y
        
        #Enemy Initial Position
        self.position_x = from_x
        self.position_y = from_y
        
        #Enemy Speed
        vector_x = to_x - from_x
        vector_y = to_y - from_y
        mag = sqrt(vector_x**2 + vector_y**2)
        self.speed_x = (vector_x / mag) * speed
        self.speed_y = (vector_y / mag) * speed
        
        #Enemy health
        self.current_hp = health
        self.max_hp = health
        
        #Bounce Count
        self.bounces = 0
        
    def update(self, win, win_size_x, win_size_y, dt):
        
        #Return True if Enemy is defeated
        if self.current_hp <= 0:
            return True
        
        #Update Position
        self.position_x += self.speed_x * dt
        self.position_y += self.speed_y * dt
        
        #Update position of square
        self.square = pygame.Rect(self.position_x, self.position_y, self.size_x, self.size_y)
        pygame.draw.rect(win, self.colour, self.square)
        
        #Display health bar
        self.ratio = self.current_hp/self.max_hp
        self.health_green = pygame.Rect(self.position_x, self.position_y - self.size_y/2, self.size_x * self.ratio, self.size_y/10)
        pygame.draw.rect(win, (0, 255, 0), self.health_green)
        self.health_red = pygame.Rect(self.position_x + self.size_x * self.ratio, self.position_y - self.size_y/2, self.size_x * (1.0 - self.ratio), self.size_y/10)
        pygame.draw.rect(win, (255, 0, 0), self.health_red)
        
        #Reflect speed when it touches a side of window
        if  (self.position_x < 0 and self.speed_x < 0) or (self.position_x > win_size_x - self.size_x and self.speed_x > 0):
            self.bounces += 1
            self.speed_x = -self.speed_x
        if (self.position_y < 0 and self.speed_y < 0) or (self.position_y > win_size_y - self.size_y and self.speed_y > 0):
            self.bounces += 1
            self.speed_y = -self.speed_y
        
        return False
    
    def projectile_hit(self, projectile_x, projectile_y, damage):
        
        #Check if projectile is inside Enemy rect
        if (projectile_x > self.position_x and projectile_x < self.position_x + self.size_x and 
            projectile_y > self.position_y and projectile_y < self.position_y + self.size_y):
            
            self.current_hp -= damage
            
            return True
        else:
            return False
        
#Projectiles from player weapon
class player_projectile():
    
    def __init__(self, col, size, pos_x, pos_y, speed_x, speed_y, damage):
        
        #Size
        self.size = size
        
        #Projectile colour
        self.colour = col
        
        #Current position
        self.position_x = pos_x
        self.position_y = pos_y
        
        #Speed
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        #Damage
        self.damage = damage
        
    def update(self, win, dt):
        
        #Update Position
        self.position_x += self.speed_x * dt
        self.position_y += self.speed_y * dt
        
        #Update position of Projectile
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.size)
        
    def collision(self, win_size_x, win_size_y, enemies):
        
        #Check if collision with Enemy occurs
        for i in enemies:
            if i.projectile_hit(self.position_x, self.position_y, self.damage):
                return True
            
        #Check if collision with window border has occured
        if  (self.position_x < 0 and self.speed_x < 0) or (self.position_x > win_size_x - self.size and self.speed_x > 0):
            return True
        if (self.position_y < 0 and self.speed_y < 0) or (self.position_y > win_size_y - self.size and self.speed_y > 0):
            return True
        return False
 
#Player weapon
class Weapon():
    
    def __init__(self, projectile_col, projectile_size, projectile_fire_delay, projectile_speed, projectile_damage, type):
        
        #weapon type
        self.type = type
        
        #Projectile colour
        self.colour = projectile_col
        
        #Projectile apparent size (Visual only)
        self.size = projectile_size
        
        #Time since last fire
        self.time_since_last = 0
        
        #Speed of projectile
        self.speed = projectile_speed
        self.fire_delay = projectile_fire_delay
        self.speed_count = 1
        
        #Damage to Enemy
        self.damage = projectile_damage
        self.damage_updgrade_count = 1
        
        #Projectiles
        self.projectiles = []
        
    def shoot(self, from_x, from_y, to_x, to_y, dt):
        
        self.time_since_last += dt
        
        if self.time_since_last > self.fire_delay:
            
            self.time_since_last = 0    
            
            #Create new Projectile after setting x and y speed parameters based on from and to
            vector_x = to_x - from_x
            vector_y = to_y - from_y
            mag = sqrt(vector_x**2 + vector_y**2)
            speed_x = (vector_x / mag) * self.speed
            speed_y = (vector_y / mag) * self.speed
            
            #One projectile
            if self.type == 0:  
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x, speed_y, self.damage))
            #3 projectiles in cone
            if self.type == 1: 
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x * cos(-0.3927) - speed_y * sin(-0.3927), speed_x * sin(-0.3927) + speed_y * cos(-0.3927), self.damage))
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x, speed_y, self.damage))
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x * cos(0.3927) - speed_y * sin(0.3927), speed_x * sin(0.3927) + speed_y * cos(0.3927), self.damage))
            #5 projectiles in cone
            elif self.type == 2:
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x * cos(-0.7854) - speed_y * sin(-0.7854), speed_x * sin(-0.7854) + speed_y * cos(-0.7854), self.damage))
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x * cos(-0.3927) - speed_y * sin(-0.3927), speed_x * sin(-0.3927) + speed_y * cos(-0.3927), self.damage))
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x, speed_y, self.damage))
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x * cos(0.3927) - speed_y * sin(0.3927), speed_x * sin(0.3927) + speed_y * cos(0.3927), self.damage))
                self.projectiles.append(player_projectile(self.colour, self.size, from_x, from_y, speed_x * cos(0.7854) - speed_y * sin(0.7854), speed_x * sin(0.7854) + speed_y * cos(0.7854), self.damage))
                
    def update_and_collision(self, window, window_size_x, window_size_y, enemies, dt):
        
        i = 0
        while i < len(self.projectiles):
            self.projectiles[i].update(window, dt)
            if self.projectiles[i].collision(window_size_x, window_size_y, enemies):
                self.projectiles.pop(i)
            else:
                i += 1
                
    def upgrade_damage(self):
        self.damage_updgrade_count += 1
        self.damage += 1
        self.damage *= weapon_damage_upgrade_multiplier 
    def upgrade_speed(self):
        self.speed_count += 1
        self.speed += speed_increase  
        self.fire_delay /= delay_decrease
        
        if self.fire_delay < min_delay:
            self.fire_delay = min_delay
    def upgrade_weapon(self):
        self.type += 1
                            
#Player that can be controlled with keys
class Player():
    
    def __init__(self, col, window_x, window_y):
        
        #Score
        self.score:int = 0
        self.money:int = 0
        
        #Player Cube Size
        self.size_x = player_size
        self.size_y = player_size
        
        #Player colour
        self.colour = col
        
        #Player speed
        self.speed = player_speed
        
        #Reset
        self.reset(window_x, window_y)
        
    def move(self, win_size_x, win_size_y, keys, dt):
        
        #Resultant position change
        dx:float = 0.0
        dy:float = 0.0
        
        #Move left
        if keys[pygame.K_a] and self.position_x > 0:
            dx -= self.speed * dt
        #Move right
        if keys[pygame.K_d] and self.position_x < win_size_x - self.size_x:   
            dx += self.speed * dt
        #Move up
        if keys[pygame.K_w] and self.position_y > 0:   
            dy -= self.speed * dt
        #Move down
        if keys[pygame.K_s] and self.position_y < win_size_y - self.size_y:   
            dy += self.speed * dt
        
        #If moving in both axis divide both by sqrt(2) to keep magnitude = speed
        if dx != 0.0 and dy != 0.0:
            self.position_x += dx/sqrt(2)
            self.position_y += dy/sqrt(2)
        else:
            self.position_x += dx
            self.position_y += dy
    
    def update(self, win):    
        self.square = pygame.Rect(self.position_x, self.position_y, self.size_x, self.size_y)
        pygame.draw.rect(win, self.colour, self.square)
        
    #Check if player is inside an Enemy block
    def collision(self, Enemy):
        for i_Enemy in Enemy:
            
            if (self.position_x < i_Enemy.position_x + i_Enemy.size_x and
                self.position_x + self.size_x > i_Enemy.position_x and
                self.position_y < i_Enemy.position_y + i_Enemy.size_y and
                self.position_y + self.size_y > i_Enemy.position_y):
                
                return True
            
        return False
    
    #Run at start of new game
    def reset(self, window_size_x, window_size_y):
        
        self.score = 0
        self.money = 0
        
        self.position_x = window_size_x/2
        self.position_y = window_size_y/2
        self.square = pygame.Rect(self.position_x, self.position_y, self.size_x, self.size_y)
        
        #Player weapon at start
        self.weapon = Weapon(projectile_col=(255, 0, 0), projectile_size = 5, projectile_fire_delay=1024, projectile_speed = 1, projectile_damage = 1, type = 0)
        
#Main window
class Game():
    
    def __init__(self, w_col, win_x, win_y, p_col):
        
        #Player
        self.player = Player(p_col, win_x, win_y)
        
        #enemies
        self.enemies = []
        self.time_since_last_spawn = 0
        
        #Background colour
        self.background_colour = w_col
        
        #Window Size
        self.window_size_x = win_x
        self.window_size_y = win_y
        
        #Pygame and Window Setup
        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((win_x, win_y))
        self.clock = pygame.time.Clock()
        
        #Score text
        self.my_font = pygame.font.SysFont('Comic Sans MS', 20)
        
    def quit(self):
            pygame.quit()
            sys.exit()
            
    def run(self):
        while True:
            
            #Clock
            dt = self.clock.tick(120) 
            self.time_since_last_spawn += dt
            
            #Fill
            self.window.fill(self.background_colour)
            
            #Events
            keys=pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
                                
            for event in pygame.event.get():
                
                #Quit
                if event.type == pygame.QUIT:
                    self.quit()
                    
                #Pause
                if keys[pygame.K_ESCAPE] and event.type == pygame.KEYUP:    
            
                        paused = True
                        
                        while paused:
                        
                            keys=pygame.key.get_pressed()
                            
                            for event in pygame.event.get():
                                if keys[pygame.K_ESCAPE] and event.type == pygame.KEYUP:
                                    paused = False
                                if event.type == pygame.QUIT:
                                    self.quit()
                            dt = self.clock.tick(120)
                
                #Mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    #Upgrade weapon
                    if self.player.money >= damage_upgrade_cost and 300 <= mouse_x <= 600 and 0 <= mouse_y <= 40: 
                        self.player.money -= damage_upgrade_cost
                        self.player.weapon.upgrade_damage() 
                    if self.player.weapon.fire_delay > min_delay and self.player.money >= firing_speed_cost and 650 <= mouse_x <= 1050 and 0 <= mouse_y <= 40: 
                        self.player.money -= firing_speed_cost
                        self.player.weapon.upgrade_speed() 
                    if self.player.weapon.type != 2 and self.player.money >= weapon_upgrade_cost and 1100 <= mouse_x <= 1400 and 0 <= mouse_y <= 40: 
                        self.player.money -= weapon_upgrade_cost
                        self.player.weapon.upgrade_weapon()

            #Upgrade button 1            
            if 300 <= mouse_x <= 600 and 0 <= mouse_y <= 40: 
                pygame.draw.rect(self.window, (170,170,170), [300,0,300,40]) 
            else: 
                pygame.draw.rect(self.window, (100,100,100), [300,0,300,40]) 
            upgrade_button_1 = self.my_font.render(f'Upgrade Damage (£{damage_upgrade_cost}) = {self.player.weapon.damage_updgrade_count}' , True , (255,255,255)) 
            self.window.blit(upgrade_button_1, (310,0)) 
            
            #Upgrade button 2
            if 650 <= mouse_x <= 1050 and 0 <= mouse_y <= 40: 
                pygame.draw.rect(self.window, (170,170,170), [650,0,400,40]) 
            else: 
                pygame.draw.rect(self.window, (100,100,100), [650,0,400,40]) 
            upgrade_button_2 = self.my_font.render(f'Upgrade Projectile Speed (£{firing_speed_cost}) = {self.player.weapon.speed_count}' , True , (255,255,255)) 
            self.window.blit(upgrade_button_2, (660,0)) 
            
            #Upgrade button 3
            if 1100 <= mouse_x <= 1400 and 0 <= mouse_y <= 40: 
                pygame.draw.rect(self.window, (170,170,170), [1100,0,300,40]) 
            else: 
                pygame.draw.rect(self.window, (100,100,100), [1100,0,300,40]) 
            upgrade_button_3 = self.my_font.render(f'Upgrade Weapon (£{weapon_upgrade_cost}) = {self.player.weapon.type + 1}' , True , (255,255,255)) 
            self.window.blit(upgrade_button_3, (1110,0))  
            
            #Shoot weapon at mouse location
            self.player.weapon.shoot(self.player.position_x, self.player.position_y, mouse_x, mouse_y, dt)
            
            #Add 1 Enemy after set period * len(self.enemies), up to a max of max_enemies or Enemy_spawn_scale * current_score whichever is less. HP set to 1 + score/Enemy_hp_scale
            if self.time_since_last_spawn > len(self.enemies) * min_time_between_Enemy_spawn and len(self.enemies) < max_enemies and self.player.score >= Enemy_spawn_scale * len(self.enemies):
                
                #Make spawn at a random corner of window
                spawn_x = self.window_size_x * np.random.randint(0, 2)
                spawn_y = self.window_size_y * np.random.randint(0, 2)
                
                self.enemies.append(Enemy((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)), Enemy_size, Enemy_size, spawn_x, spawn_y, self.player.position_x, self.player.position_y, Enemy_speed, 1 + self.player.score/Enemy_hp_scale))
                
                self.time_since_last_spawn = 0
                
            #Player movement and update position
            self.player.move(self.window_size_x, self.window_size_y, keys, dt)
            self.player.update(self.window) 
            
            #Update player weapon projectiles and collisions
            self.player.weapon.update_and_collision(self.window, self.window_size_x, self.window_size_y, self.enemies, dt)
                    
            #Update enemies and score
            i = 0
            while i < len(self.enemies):
                if self.enemies[i].update(self.window, self.window_size_x, self.window_size_y, dt) == True:
                    self.player.score += int(self.enemies[i].max_hp)
                    self.player.money += 100
                    self.enemies.pop(i)
                    
                    #Play sound
                    pygame.mixer.Sound("Enemy_Defeated.wav").play()
                    
                else:
                    i += 1
            
            #Check player is not inside an Enemy
            if self.player.collision(self.enemies):
                pygame.mixer.Sound("Game_Over.wav").play()
                print(f"You scored: {self.player.score}")
                self.enemies.clear()
                self.player.reset(self.window_size_x, self.window_size_y)
                
            #Display current score
            score_display = self.my_font.render(f'Score: {str(self.player.score)}      Money: £{self.player.money}', True, (0, 0, 0))
            self.window.blit(score_display, (0,0))    
            
            #Update display   
            pygame.display.flip()
            
if __name__ == "__main__":    
    game = Game(w_col = (255, 255, 255), win_x = 1500, win_y = 750, p_col = (0, 255, 0))
    game.run()
