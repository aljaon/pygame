import pygame
import random
import numpy as np
import sys
from math import sqrt

win_x = 1500 
win_y = 750
number_to_spawn = [1,1,1,2,4,6,9,12,15,15,15,20,25,30,35,40,50,60,70,80]
spawn_range = [(win_x * 1.3, win_x * 1.3), (win_x* 1.1, win_x* 1.1), (win_x, win_x), (win_x, win_x * 1.5)]
spawn_type = [np.array([1]),np.array([1]),np.array([1]),np.array([1]),np.array([1]),np.array([5,1]),np.array([5,1]),np.array([4,1]),np.array([4,1]),np.array([3,1]),np.array([3,1]),np.array([5,1,1]),np.array([5,1,1]),np.array([5,2,1])]


#Units
class unit:
    def __init__(self, col, pos_x, pos_y, radius, health):

        self.colour = col
        self.position_x = pos_x
        self.position_y = pos_y
        self.radius = radius
        self.health = health
        
    def act(self, projectiles, money, dt):
        pass
           
    def draw(self, win):
        pass
        
class passive_generator(unit):
    def __init__(self):
        
        super().__init__(col = (0, 0, 0), pos_x = -1, pos_y = -1, radius = 0, health = 9999999)
        
        self.time_since_last_produce = 0
        
        #Stats
        self.interval = 10000
        self.amount = 25
        
    def act(self, money, dt):
        
        #Delay before money added
        if self.time_since_last_produce >= self.interval:
        
           self.time_since_last_produce = 0
           money[0] += self.amount
             
        else:
           self.time_since_last_produce += dt
           
    def draw(self, win):
        pass      
class generator(unit):
    
    cost = 50
    
    def __init__(self, pos_x, pos_y):
        
        super().__init__(col = (255, 255, 255), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        super().__init__(col = (255, 255, 255), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        
        self.time_since_last_produce = 0
        
        #Stats
        self.initial_interval = random.randint(4000, 8000)
        self.regular_interval = 24000
        self.amount = 25
        
    def act(self, enermies, projectiles, money, dt):

        #Initial delay
        if self.initial_interval != 0 and self.time_since_last_produce >= self.initial_interval:
            
           self.initial_interval = 0
           self.time_since_last_produce = 0 #Set to 0 after intital delay so not used anymore
           money[0] += self.amount
           
        #Every other delay
        elif self.time_since_last_produce >= self.regular_interval:
        
            self.time_since_last_produce = 0
            money[0] += self.amount
        
        #Change colour based on time before delay is over     
        else:
            self.time_since_last_produce += dt
            
            interval = self.regular_interval
            if self.initial_interval != 0:
                interval = self.initial_interval
                
            r = self.time_since_last_produce / interval

            if r <= 0.25:
                self.colour = (255, 255, 255)
            elif r <= 0.50:
                self.colour = (170, 255, 255)
            elif r <= 0.75:
                self.colour = (85, 255, 255)
            else:
                self.colour = (0, 255, 255)

        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False  
        
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)     
class fast_generator(unit):
    
    cost = 150
    
    def __init__(self, pos_x, pos_y):
        
        super().__init__(col = (255, 255, 255), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        super().__init__(col = (255, 255, 255), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        
        self.time_since_last_produce = 0
        
        #Stats
        self.initial_interval = random.randint(4000, 8000)
        self.regular_interval = 24000
        self.amount = 50
        
    def act(self, enermies, projectiles, money, dt):

        #Initial delay
        if self.initial_interval != 0 and self.time_since_last_produce >= self.initial_interval:
            
           self.initial_interval = 0
           self.time_since_last_produce = 0 #Set to 0 after intital delay so not used anymore
           money[0] += self.amount
           
        #Every other delay
        elif self.time_since_last_produce >= self.regular_interval:
        
            self.time_since_last_produce = 0
            money[0] += self.amount
        
        #Change colour based on time before delay is over     
        else:
            self.time_since_last_produce += dt
            
            interval = self.regular_interval
            if self.initial_interval != 0:
                interval = self.initial_interval
                
            r = self.time_since_last_produce / interval

            if r <= 0.25:
                self.colour = (255, 255, 255)
            elif r <= 0.50:
                self.colour = (255, 170, 255)
            elif r <= 0.75:
                self.colour = (255, 85, 255)
            else:
                self.colour = (255, 0, 255)

        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False  
        
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)
class shooter_1(unit):
    
    cost = 100
    
    def __init__(self, pos_x, pos_y):

        super().__init__(col = (255, 255, 0), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        
        #Attack speed of unit
        self.attack_delay = 1500
        
        #Damage
        self.damage = 10
        
        #Time since last attack
        self.time_since_last_attack = 0
        
    def act(self, enermies, projectiles, money, dt):
        
        #Append new projectile after each attack_delay is reached and there is at least one enermy in the same row
        if any(enermy.position_y == self.position_y and enermy.position_x < win_x for enermy in enermies) and self.time_since_last_attack >= self.attack_delay:
            
           projectiles.append(projectile(col = (255, 255, 255), initial_pos_x = self.position_x, initial_pos_y = self.position_y, radius = 10, vel = (1, 0), damage = self.damage))
           self.time_since_last_attack = 0
           
        else:
            
           self.time_since_last_attack += dt
           
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
           
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)
class shooter_2(unit):
    
    cost = 200
    
    def __init__(self, pos_x, pos_y):

        super().__init__(col = (255, 150, 0), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        
        #Attack speed of unit
        self.attack_delay = 1500
        
        #Damage
        self.damage = 10
        
        #Second Shot
        self.shots = 2
        self.delay_between_other_shot = 100
        
        #Time since last attack
        self.time_since_last_attack = 0
        self.current_shot = 0
        
    def act(self, enermies, projectiles, money, dt):
        
        #Append new projectile after each attack_delay is reached and there is at least one enermy in the same row
        if self.current_shot == 0 and (any(enermy.position_y == self.position_y and enermy.position_x < win_x for enermy in enermies) and self.time_since_last_attack >= self.attack_delay):
            
           projectiles.append(projectile(col = (255, 255, 255), initial_pos_x = self.position_x, initial_pos_y = self.position_y, radius = 10, vel = (1, 0), damage = self.damage))
           self.current_shot += 1
           self.time_since_last_attack = 0
        
        #Second shot   
        elif self.current_shot >= 1:
            
            #Fire if delay time is reached
            if self.time_since_last_attack >= self.delay_between_other_shot:
                
                projectiles.append(projectile(col = (255, 255, 255), initial_pos_x = self.position_x, initial_pos_y = self.position_y, radius = 10, vel = (1, 0), damage = self.damage))
                self.current_shot += 1
                self.time_since_last_attack = 0
                
                #If max shots are reached reset and set to 0
                if self.current_shot >= self.shots:
                    self.current_shot = 0
                    
            else:
                self.time_since_last_attack += dt
        else:
           self.time_since_last_attack += dt
           
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
           
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)
class shooter_3(unit):
    
    cost = 400
    
    def __init__(self, pos_x, pos_y):

        super().__init__(col = (252, 0, 0), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        
        #Attack speed of unit
        self.attack_delay = 1500
        
        #Damage
        self.damage = 10
        
        #Second Shot
        self.shots = 4
        self.delay_between_other_shot = 100
        
        #Time since last attack
        self.time_since_last_attack = 0
        self.current_shot = 0
        
    def act(self, enermies, projectiles, money, dt):
        
        #Append new projectile after each attack_delay is reached and there is at least one enermy in the same row
        if self.current_shot == 0 and (any(enermy.position_y == self.position_y and enermy.position_x < win_x for enermy in enermies) and self.time_since_last_attack >= self.attack_delay):
            
           projectiles.append(projectile(col = (255, 255, 255), initial_pos_x = self.position_x, initial_pos_y = self.position_y, radius = 10, vel = (1, 0), damage = self.damage))
           self.current_shot += 1
           self.time_since_last_attack = 0
        
        #Second shot   
        elif self.current_shot >= 1:
            
            #Fire if delay time is reached
            if self.time_since_last_attack >= self.delay_between_other_shot:
                
                projectiles.append(projectile(col = (255, 255, 255), initial_pos_x = self.position_x, initial_pos_y = self.position_y, radius = 10, vel = (1, 0), damage = self.damage))
                self.current_shot += 1
                self.time_since_last_attack = 0
                
                #If max shots are reached reset and set to 0
                if self.current_shot >= self.shots:
                    self.current_shot = 0
                    
            else:
                self.time_since_last_attack += dt
        else:
           self.time_since_last_attack += dt
           
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
           
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)
class mine(unit):
    
    cost = 25
    
    def __init__(self, pos_x, pos_y):

        super().__init__(col = (0, 0, 0), pos_x = pos_x, pos_y = pos_y, radius = 20, health = 100)
        
        #Time to arm
        self.arm_time = 14000
        self.time_since_placed = 0
        
        #Damage
        self.damage = 1800
        
    def act(self, enermies, projectiles, money, dt):
        
        #Wait arm time
        if self.arm_time < self.time_since_placed:
            
           self.arm_time += dt
        
        #Replace with static projectile after armed
        elif self.arm_time >= self.time_since_placed:
                
                projectiles.append(projectile(col = self.colour, initial_pos_x = self.position_x, initial_pos_y = self.position_y, radius = 20, vel = (0, 0), damage = self.damage))
                
                return True   
           
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
           
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)

#Units you can buy names and costs
avaliable_units = ["Generator", "Fast Generator", "Shooter", "Double Shooter", "Quad Shooter"]
unit_costs = [generator.cost, fast_generator.cost, shooter_1.cost, shooter_2.cost, shooter_3.cost]


#Enermies
class enermy():
    def __init__(self, col, initial_pos_x, initial_pos_y, size):
        
        #Graphic
        self.square = pygame.Rect(initial_pos_x, initial_pos_y, size, size)
        
        self.col = col
        self.position_x = initial_pos_x
        self.position_y = initial_pos_y
        self.size = size
        
    def act():
        pass
    
    def draw():
        pass
class easy_enermy(enermy):
    
    def __init__(self, initial_pos_x, initial_pos_y):    
        
        super().__init__((0, 0, 0), initial_pos_x, initial_pos_y, 30)

        self.health = 100
        self.damage = 1
        self.velocity_x = -0.035
        
    def act(self, units, dt):
        
        #Is this enermy attacking a unit?
        attacking = False

        for key, unit in units.items():
            
            if sqrt((unit.position_x - self.position_x)**2 + (unit.position_y - self.position_y)**2) <= (unit.radius + self.size):
                unit.health -= 1
                attacking = True
                break     
        if attacking == False:
            self.position_x += dt * self.velocity_x
                
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
                 
    def draw(self, win):
        pygame.draw.circle(win, self.col, (self.position_x, self.position_y), self.size)
class medium_enermy(enermy):
    
    def __init__(self, initial_pos_x, initial_pos_y):    
        
        super().__init__((255, 150, 0), initial_pos_x, initial_pos_y, 30)

        self.health = 280
        self.damage = 1
        self.velocity_x = -0.035
        
    def act(self, units, dt):
        
        if self.health <= 100:
            self.col = (0, 0, 0)
        
        #Is this enermy attacking a unit?
        attacking = False
        for key, unit in units.items():
            
            if sqrt((unit.position_x - self.position_x)**2 + (unit.position_y - self.position_y)**2) <= (unit.radius + self.size):
                unit.health -= 1
                attacking = True
                break     
        if attacking == False:
            self.position_x += dt * self.velocity_x
               
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
                 
    def draw(self, win):
        pygame.draw.circle(win, self.col, (self.position_x, self.position_y), self.size)
class hard_enermy(enermy):
    
    def __init__(self, initial_pos_x, initial_pos_y):    
        
        super().__init__((190, 190, 190), initial_pos_x, initial_pos_y, 30)

        self.health = 650
        self.damage = 1
        self.velocity_x = -0.035
        
    def act(self, units, dt):
        
        if self.health <= 100:
            self.col = (0, 0, 0)
        
        #Is this enermy attacking a unit?
        attacking = False
        for key, unit in units.items():
            
            if sqrt((unit.position_x - self.position_x)**2 + (unit.position_y - self.position_y)**2) <= (unit.radius + self.size):
                unit.health -= 1
                attacking = True
                break     
        if attacking == False:
            self.position_x += dt * self.velocity_x
               
        #Delete when health becomes less than 0
        if self.health <= 0:
            return True 
        
        else:      
            return False
                 
    def draw(self, win):
        pygame.draw.circle(win, self.col, (self.position_x, self.position_y), self.size)
                    

#Projectiles          
class projectile:
    def __init__(self, col, initial_pos_x, initial_pos_y, radius, vel, damage):
        
        #Colour
        self.colour = col
        
        #Movement             
        self.position_x = initial_pos_x
        self.position_y = initial_pos_y
        self.radius = radius
        self.velocity = vel
        
        #Damage
        self.damage = damage
        
    def act(self, enermies, dt):
        
        self.position_x += dt * self.velocity[0]
        self.position_y += dt * self.velocity[1]
        
        #Has projectile made contact with an enermy?     
        i = 0
        while i < len(enermies):
                
            #Check if projectile has hit enermy and if so delete by returning true
            if sqrt((enermies[i].position_x - self.position_x)**2 + (enermies[i].position_y - self.position_y)**2) <= (enermies[i].size + self.radius):
                    
                enermies[i].health -= self.damage
                return True
                
            else:
                i += 1  
        return False
        
    def draw(self, win):
         pygame.draw.circle(win, self.colour, (self.position_x, self.position_y), self.radius)


class tile:
    def __init__(self, from_x, from_y, width, height, col, col2, board):
        
        self.colour = col
        self.colour_highlight = col2
        
        self.centre = (from_x + width/2, from_y + height/2)

        self.square = pygame.Rect(from_x, from_y, width, height)
        pygame.draw.rect(board, self.colour, self.square)
        
    def draw_highlight(self, win):
        pygame.draw.rect(win, self.colour_highlight, self.square)
               
class Game():
    
    def __init__(self, w_col, win_x, win_y, top_space, rows, columns, c1, c2, c1_h, c2_h):
        
        #Grid size
        self.top_space = top_space
        self.win_x = win_x
        self.win_y = win_y
        self.columns = columns
        self.rows = rows
        
        #Tiles
        self.board = pygame.Surface((win_x, win_y))
        pygame.draw.rect(self.board, (255,255,255), pygame.Rect(0, 0, self.win_x, self.top_space))
        
        self.tiles = list()
        for row_index in range(rows):
            self.tiles.append(list())
            for column_index in range(columns):
                if (row_index + column_index) % 2 == 0:
                    self.tiles[row_index].append(tile(column_index * win_x/columns, self.top_space + row_index * (win_y - self.top_space)/rows, win_x/columns, (win_y - self.top_space)/rows, c1, c1_h, self.board))
                else:
                    self.tiles[row_index].append(tile(column_index * win_x/columns, self.top_space + row_index * (win_y - self.top_space)/rows, win_x/columns, (win_y - self.top_space)/rows, c2, c2_h, self.board))

        
        
        #Used to find tile mouse is hovered over
        self.mouse_rows_below_index = list()
        self.mouse_columns_below_index = list()
        for row_index in range(rows):
            self.mouse_rows_below_index.append(self.top_space + row_index * (win_y - self.top_space)/rows)
        for column_index in range(columns):
            self.mouse_columns_below_index.append(column_index * win_x/columns)
        
        #Money
        self.money = [100]
        
        #Wave
        self.wave = 0
        
        #Units
        self.passive_generator = passive_generator()
        self.units = {}
        
        #Select unit
        self.unit_select = 0
        
        #Mouse
        self.hover_row = -1
        self.hover_column = -1
        
        #Projectiles
        self.projectiles = []
        
        #Enermies
        self.enermies = []
        
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
            
    def events(self):

        #Units
        self.passive_generator.act(self.money, self.dt)
        to_remove = []
        for key, unit in list(self.units.items()):
            if unit.act(self.enermies, self.projectiles, self.money, self.dt) == True:
                to_remove.append(key)
            else:
                unit.draw(self.window)

        for key in to_remove:
            self.units.pop(key)
        
        
        #Add in Enermies
        if len(self.enermies) == 0:
            
            number_to_add = number_to_spawn[self.wave] if self.wave < len(number_to_spawn) else number_to_spawn[len(number_to_spawn) - 1]
            spawn_area = spawn_range[self.wave] if self.wave < len(spawn_range) else spawn_range[len(spawn_range) - 1]
            type_to_spawn = spawn_type[self.wave] if self.wave < len(spawn_type) else spawn_type[len(spawn_type) - 1]

            for i in range(number_to_add):
                
                x = random.uniform(spawn_area[0], spawn_area[1])
                y = random.choice(self.mouse_rows_below_index) + ((self.win_y - self.top_space)/self.rows) / 2
                
                enermy_type = np.random.choice(len(type_to_spawn), p=type_to_spawn/sum(type_to_spawn))

                if enermy_type == 0:
                    self.enermies.append(easy_enermy(x, y))
                elif enermy_type == 1:
                    self.enermies.append(medium_enermy(x, y))
                elif enermy_type == 2:
                    self.enermies.append(hard_enermy(x, y))
                    
            self.wave += 1
                
        i = 0
        while i < len(self.enermies):

            self.enermies[i].draw(self.window)

            if self.enermies[i].position_x < 0:
                raise Exception("Game over")
            
            #Remove enermies if they are killed or off-screen or have no health
            if self.enermies[i].act(self.units, self.dt):
                self.enermies.pop(i)
            else:
                i += 1
                      
        #Projectiles
        i = 0
        while i < len(self.projectiles):
            
            self.projectiles[i].draw(self.window)
            
            #Delete projectiles if they go off-screen or hit an enermy
            if self.projectiles[i].act(self.enermies, self.dt) or self.projectiles[i].position_x < 0 or self.projectiles[i].position_x > self.win_x or self.projectiles[i].position_y < 0 or self.projectiles[i].position_y > self.win_y:
                self.projectiles.pop(i)
            
            else:
                i += 1
                 
    def inputs(self):
        
        #Get button/mouse responses
        keys=pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
            
        #Get tile mouse is hovering
        self.hover_row  = -1
        self.hover_column = -1
        if mouse_y > self.top_space:
            while self.hover_column < self.columns - 1 and self.mouse_columns_below_index[self.hover_column + 1] < mouse_x:
                self.hover_column += 1
            while self.hover_row < self.rows - 1 and self.mouse_rows_below_index[self.hover_row + 1] < mouse_y:
                self.hover_row += 1
        
            
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
                
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    #Left Click to create unit
                    if event.button == 1:
                        if self.hover_row > -1 and self.hover_column > -1 and (self.hover_row, self.hover_column) not in self.units:
                            if avaliable_units[self.unit_select] == avaliable_units[0] and self.money[0] >= generator.cost:
                                self.units[(self.hover_row, self.hover_column)] = generator(pos_x = self.tiles[self.hover_row][self.hover_column].centre[0], pos_y = self.tiles[self.hover_row][self.hover_column].centre[1])
                                self.money[0] -= generator.cost
                            elif avaliable_units[self.unit_select] == avaliable_units[1] and self.money[0] >= fast_generator.cost:
                                self.units[(self.hover_row, self.hover_column)] = fast_generator(pos_x = self.tiles[self.hover_row][self.hover_column].centre[0], pos_y = self.tiles[self.hover_row][self.hover_column].centre[1])
                                self.money[0] -= fast_generator.cost
                            elif avaliable_units[self.unit_select] == avaliable_units[2] and self.money[0] >= shooter_1.cost:
                                self.units[(self.hover_row, self.hover_column)] = shooter_1(pos_x = self.tiles[self.hover_row][self.hover_column].centre[0], pos_y = self.tiles[self.hover_row][self.hover_column].centre[1])
                                self.money[0] -= shooter_1.cost
                            elif avaliable_units[self.unit_select] == avaliable_units[3] and self.money[0] >= shooter_2.cost:
                                self.units[(self.hover_row, self.hover_column)] = shooter_2(pos_x = self.tiles[self.hover_row][self.hover_column].centre[0], pos_y = self.tiles[self.hover_row][self.hover_column].centre[1])
                                self.money[0] -= shooter_2.cost
                            elif avaliable_units[self.unit_select] == avaliable_units[4] and self.money[0] >= shooter_3.cost:
                                self.units[(self.hover_row, self.hover_column)] = shooter_3(pos_x = self.tiles[self.hover_row][self.hover_column].centre[0], pos_y = self.tiles[self.hover_row][self.hover_column].centre[1])
                                self.money[0] -= shooter_3.cost
                                
                                
                            #Debug
                            #elif avaliable_units[self.unit_select] == "None":
                            #    self.enermies.append(easy_enermy(self.tiles[self.hover_row][self.hover_column].centre[0], self.tiles[self.hover_row][self.hover_column].centre[1]))
                                    
                    #Right click to remove unit
                    elif event.button == 3 and (self.hover_row, self.hover_column) in self.units :
                        del self.units[(self.hover_row, self.hover_column)]
                    
                    #Mouse Wheel        
                    elif event.button == 4:
                        self.unit_select += 1
                    elif event.button == 5:
                        self.unit_select -= 1
                    
                    #Have avaliable unit index cycle if reach an out of bound index from mousewheel
                    if self.unit_select >= len(avaliable_units):
                        self.unit_select = 0
                    elif self.unit_select < 0:
                        self.unit_select = len(avaliable_units) - 1
                                
    def run(self):
        while True:
        
            #Clock
            self.dt = self.clock.tick(60)        

            #Draw tiles
            self.window.blit(self.board, self.board.get_rect())
            if self.hover_row > -1 and self.hover_column > -1:
                self.tiles[self.hover_row][self.hover_column].draw_highlight(self.window)
        
            #Player inputs
            self.inputs()
            
            #Game events
            try:
                self.events()
            except Exception as exc:
                print(f"Game over: You suvived {self.wave} waves")
                break
            
            #Display
            score_display = self.my_font.render(f'Wave: {self.wave}    Money: £{self.money[0]}   Unit(Mousewheel): {avaliable_units[self.unit_select]} £{unit_costs[self.unit_select]}', True, (0, 0, 0))
            self.window.blit(score_display, (0,0))                  
            
            #Update display   
            pygame.display.flip()

if __name__ == "__main__": 
    game = Game(w_col = (255, 255, 255), win_x = 1500, win_y = 750, top_space = 30, rows = 6, columns = 10, c1 = (0, 255, 0), c2 = (0, 255, 150), c1_h = (0, 100, 0), c2_h = (0, 100, 0))
    game.run()
