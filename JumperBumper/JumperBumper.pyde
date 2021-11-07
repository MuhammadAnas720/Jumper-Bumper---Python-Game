# play the game by changing storage settings to 2000MB for best results.


# INSTRUCTIONS
# use RIGHT and LEFT arrow keys to navigate and change lanes
# Use UP to jump
# Avoid the Obstacles
# Catch the Boosters for benefit.
# Booster Repair, gives an extra life to car 
# Booster Speed, lets car run without obstalces for few seconds

# We hope you you become a pro, and stick in till longer (higher difficulty) to enjoy the real difficulty of the game :)


# libraries imported or essential variables are initialized
add_library('minim')
import os, random
path = os.getcwd()
player= Minim(this)
WIDTH = 1200
HEIGHT = 600
lanes = ['left','centre','right'] # for 3 lanes in game

# class for the player car of the game
class Car:
    def __init__(self, img, i = 1, x = WIDTH/2, y = HEIGHT - 250, w = 240, h = 160):
        # define values of x, y, image, car lane, width, height, jump status, and gravity acceleration
        self.x = x
        self.y = y
        self.img = loadImage(path + '/image/' + img)
        self.i = i   # self.i vriable throughout is used as the index value for lanes list, to refer to lane of the game
        self.lane = lanes[self.i]
        self.w = w
        self.h = (w*2)/3
        self.jump = False
        self.vy = 0
        self.jump_sound=player.loadFile(path +"/sounds/" + "jump.mp3")
    
    #gravity when car is up in air and down on ground
    def gravity(self):
        if self.y >= HEIGHT-250:
            self.vy=0
        else:
            self.vy += 2
            if (HEIGHT-250) - self.y <= self.vy:
                self.y = HEIGHT-250
                self.jump = False
            else:
                self.y += self.vy
   # create the car of player, depending on what lane it is
    def create_car(self):
        self.lane = lanes[self.i]
        if self.lane == 'left':
            self.x = WIDTH/2 - 3*(self.w/2)
        if self.lane == 'centre':
            self.x = WIDTH/2 - (self.w/2)
        if self.lane == 'right':
            self.x = WIDTH/2 + (self.w/2)
        # to draw the car iage using values
        image(self.img, self.x, self.y, self.w, self.h)
        
        self.gravity()
        # to make the car jump  
        if self.jump==True and self.y == HEIGHT - 250:
           self.vy = -25
           self.y += self.vy
           self.jump_sound.rewind()
           self.jump_sound.play()
    # to chnange lane of car whenever possible
    def change_lane(self, dir):
        if dir == "left" and self.i > 0:
            self.i -= 1
        elif dir == "right" and self.i < 2:
            self.i += 1    

# class for all other objects of the game
class Object:
    def __init__(self, img, i = 1, r = 1, x = WIDTH/2, y = HEIGHT/4, w = 10, h = 10, v = 0):
        # define values of image, r, i, x, y, width, height, velocity, and lane
        self.img = loadImage(path + '/image/' + img)
        self.r = r   #self.r method is used to identify object, and will be used to identify bonuses
        self.i = i
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v   # velocity of the ojects
        self.lane = lanes[self.i]
        
    # method to display the objects created
    def display(self):
        # in the came, the user car will stay at a parituclar y value, and it is the objects that will come toward the screen, making it seem car is moving forward
        # with the 3d dynamics of the game, it is crucial to move objects backward in perspective (small and slow when away, bigger and faster when nearer)
        # Hence, the following display method is used for these
        
        vals = [(WIDTH/2 + 10)  - (self.y/10 + self.w), WIDTH/2, (WIDTH/2 - 10)  + (self.y/10  + self.w)]  # preset values and formulas the object's x value would rely on depending on what lane they are at
        # incrementation of velocity, y value, x value, and object width to ake it move back in perspective 
        self.v += 0.025        
        self.y += self.v
        self.w *= (1.005**(self.y/30))
        self.x = vals[self.i]
        
        # after it reaches near to screen, a change in these values is required to suit the game display
        if self.w > 120:
            self.v += 0.25
            self.y += self.v
            self.w *= (1.00001**(self.y/60))
            self.x = vals[self.i]
        # to display the image of objects, with varying sizes
        image(self.img, self.x - (self.w)/2, self.y , self.w, (self.w*6)/10)

# class to display the road lines for raod track
# As subsequent white lines move back to the screen, the effect of car moving forward is enhanced 
class Road(Object):
    def __init__(self, x = WIDTH / 2, y = (HEIGHT/4), w = 10, h = 8, v = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
    # again the display of white lines requires them to move back into perspective, and hance their formular make them do so
    # rectangles of same color as road are created, and move back, on a pre drawn white line    
    def display(self):
        self.v += 0.1
        self.y += self.v
        self.w = self.y - HEIGHT/4 + 15
        self.h += 0.2
        self.x = (WIDTH/2) - (self.w/2)
        fill(140)
        noStroke()
        rect(self.x,self.y, self.w, self.h)
    
# class for the main game
class Game(list):
    def __init__(self):
        self.car= Car('Car.png')  # instantiates the player car
        self.score = 0   # sets the score attribute
        self.collision = 0  # set collision value to 0, which means no collision   
        self.speed = 50   # game speed describes game difficulty level (that is probability of creation of objects). The lower the speed, more difficult the game
        self.bg_image= loadImage(path + '/image/' + "bg.png")    # backgorund image loaded into attribute
        self.b1 = loadImage(path + '/image/' + 'bonus1-small.png')   # bonus 1 display image loaded
        self.b2 = loadImage(path + '/image/' + 'bonus2-small.png')   # bonus 2 display image loaded
        self.side = loadImage(path + '/image/' + 'side.png')   # instructions for arrows key display image loaded
        self.up = loadImage(path + '/image/' + 'up.png')   # UP arrow key display image loaded
        self.gameover= player.loadFile(path + "/sounds/gameover.wav")   # game over sound
        self.objects_list = ['Car1.png', 'Car2.png', 'barrier.png', 'pole.png', 'police.png', 'barrier2.png', 'sign.png']   # list containing the obstructions objects image name list 
        self.bonus_list = ['bonus1.png','bonus1.png', 'bonus2.png']   # list containing the bonus objects image name list. 
        #Bonus1 is twice, since the probability of its occurence should be double the probability for bonus2
        self.roadlines = []  # list for road lines
        self.bonus=[]    # list containing bonuses
        self.time = 0  # time attribute used for a particular bonus oject
        self.new = True  # allows if new obstracles can be created
    
    # as the game progresses, the difficulty level increases
    # this decrements score attribute after set instances
    # the lower the score attribute value, the greater difficulty, as more objects would be created        
    def speed_incrementer(self):
        if self.score >= 3400:
            self.speed = 1
        elif self.score >= 2300:
            self.speed = 2
        elif self.score >= 1500:
            self.speed = 3
        elif self.score >= 1100:
            self.speed = 4
        elif self.score >= 700:
            self.speed = 5
        elif self.score >= 0:
            self.speed = 40
            
    # this creates the grey rectangles (for road lines, to cause a break in the pre drawn white lines), after every 12 frames
    def create_lines(self):
        if (frameCount % 12) == 0:
            self.roadlines.append(Road())  # appende to the road lines list
    # road lines displayed        
    def display_lines(self):
        for t in self.roadlines:
            t.display()
    # road lines deleted after they pass the screen to save memory and stop game from slowing down        
    def delete_lines(self):
        for t in self.roadlines:
            if t.y > 2*HEIGHT:
                self.remove(t)
    
    # to create bonus objects
    def create_bonus(self):
        for t in self:
            if t.y < (HEIGHT/4) + 3:   # makes sure no bonuses are created on top of an existing object  
                return 
        r1 = random.randint(0,8)   # sets a probability for bonus creation
        if r1 < 3:   # for probability of 1/3, a random bonus will be created in a random lane  
            i = random.randint(0,2)
            self.bonus.append(Object(self.bonus_list[r1], i, r1))  # appended to bonus list
    
    # create or not create (depending on probability, an obstacle in each of 3 lanes) 
    def create_obstacles(self):
        for t in self:
            if t.y < (HEIGHT/4) + 8:  # makes sure there's reasonable gap between objects
                return    
        self.r1 = random.randint(0, 9) 
        if self.r1 < 7:  # probability of 7/10 of creating an object in a lane
            self.append(Object(self.objects_list[self.r1], 0))  # object created in respective lane and appended in game class which is a list by inheritance
        self.r2 = random.randint(0,9)
        if self.r2 < 7:
            self.append(Object(self.objects_list[self.r2], 1))
        self.r3 = random.randint(0,9)
        if self.r3 < 7:
            self.append(Object(self.objects_list[self.r3], 2))
    # delete obstacle when they disappear from screen to save memory
    def delete_obstacles(self):
        for t in self:
            if t.y > HEIGHT:
                self.remove(t)
    # delete bonuses when they disappear from screen to save memory            
    def delete_bonus(self):
        for t in self.bonus:
            if t.y > HEIGHT:
                self.bonus.remove(t)
        
    # to call function create a set of 3 obstacles and bonuses
    def new_obstacles(self):
        if self.new == True:
            period = [3, 7, 13, 17, 23]   # a list of prime numbers. Required to randomize the occurence of obstacles with random and different distances
            i = random.randint(0,4)
            if (self.score % (period[i]*self.speed)) == 0: # to create objects at random distances, and 
                # at decreasing distances with increasing difficulty, to make it difficult with time
                self.create_obstacles()
                self.create_bonus()
    
    # to display both objects
    def display_objects(self):
        for t in self:
            t.display()
        for x in self.bonus:
            x.display()
    
    # to display bonus 1 on side, when user has it        
    def display_bonus(self):
        image(self.b1, WIDTH - 100, HEIGHT/4 + 80, 70, 70)
    # when user has bonus 2, no obstacles are created for a few seconds. this is for that
    def no_obstacles(self):
        image(self.b2, WIDTH - 100, HEIGHT/4, 70, 70)   #display bonus 2 on side, when user has it     
        self.time += 1    # a clock for this bonus particularly
        if self.time < 400:
            self.new = False  # no new objects will be created in this time
        else:
            self.new = True
            self.time = 0
               
    # checks collision of car into both objects, and responds respectively         
    def check_collision(self):
        # checks collision into bonuses
        for x in self.bonus:
            if x.y + ((x.w)/3) >= HEIGHT - 260 and self.car.y == HEIGHT - 250 and x.y < HEIGHT - 275:  # values for appropriate collision
                if x.i == 0 and self.car.lane == 'left':  # matches lane of car and object to check collision
                    if x.r <= 1:    #checks type of bonus
                        self.collision = -4    # this is extra life bonus, so substracts the value of collision attribute. gives extra life to the player
                    if x.r == 2:
                        self.new = False   # this is speed bonus, stopping obstacle creation

                if x.i == 1 and self.car.lane == 'centre':    # matches lane of car and object to check collision
                    if x.r <= 1:
                        self.collision = -4    
                    if x.r == 2:
                        self.new = False
                                                                    
                if x.i == 2 and self.car.lane == 'right':     # matches lane of car and object to check collision
                     if x.r <= 1:
                        self.collision = -4    
                     if x.r == 2:
                        self.new = False                         
        # checks collision into obstacles
        for t in self:
            if t.y + ((t.w)/3) >= HEIGHT - 260 and self.car.y == HEIGHT - 250 and t.y < HEIGHT - 275:
                if t.i == 0 and self.car.lane == 'left':    # matches lane of car and object to check collision
                    self.collision += 1    # if collides, increments collision attribute. 
                    
                if t.i == 1 and self.car.lane == 'centre':
                    self.collision += 1
                                        
                if t.i == 2 and self.car.lane == 'right':
                    self.collision += 1
        
        # game ends when collision occurs. checks that and plays the game over sound    
        # the value to check is set to 4, as collision attribute increments 4 times if it collides once. this is perhaps due to multiple times it is called       
        if self.collision >= 4:
            self.gameover.rewind()
            self.gameover.play()
    
    # displays the instructions in an animated interface at the start of the game. during this time, minimal objects are created so player can focus on instructions and get ready            
    def display_intructions(self):
        if self.score < 150:   # instruction 1 displayed for first 150 frames or scores of game
            fill(0,0,0)
            textSize(35)
            text("USE", 30,200)
            text("TO CHANGE LANES", 210,200)
            image(self.side, 100, 115, 100, 100)    # arrow key image
        elif 150 < self.score < 300:    # instruction 2 displayed for next 150 frames or scores of game
            fill(0,0,0)
            textSize(35)
            text("USE", 30,200)
            text("TO JUMP", 210,200)
            image(self.up, 130, 150, 50, 50)   # up arrow keys image
        elif 300 < self.score < 450:   # instruction 3 displayed for next 150 frames or scores of game
            fill(0,0,0)
            textSize(35)
            text("AVOID THE OBSTACLES", 30,200)
        elif 450 < self.score < 700:   # instruction 4 displayed for next 250 frames or scores of game
            fill(0,0,0)
            textSize(35)
            text("CATCH THE BONUSES", 30,200)
            textSize(25)
            text("EXTRA REPAIR LIFE", 120,265)
            text("CLEAR THE PATH", 120,350)
            image(self.b1, 40, 220, 70, 70)   # displays the bonuses to user knows
            image(self.b2, 40, 310, 70, 70)
    
    # display when game ends
    def end_display(self):
        fill(0,0,0)
        textSize(40)
        text("GAME OVER", 500,230)
        textSize(30)
        text("Score:" + str(self.score), 500, 260)
        textSize(20)
        text("Click anywhere to begin new game", 500, 280)
        
    # display background    
    def display_background(self):
        # the blue sky background
        fill (12, 150, 228)
        rect(0,0,WIDTH, HEIGHT/4)
        # the green grass background
        fill(30, 183, 66)
        rect(0,HEIGHT/4, WIDTH, HEIGHT)
        # the skyscrappers background image
        image(game.bg_image,250,0,WIDTH-500, HEIGHT/4)
        # the road draw as a quadrilateral shape for perspective view
        fill(140)
        quad(0, HEIGHT , WIDTH, HEIGHT , WIDTH/2 + 20, HEIGHT/4, WIDTH/2 - 20, HEIGHT/4)
        # the white lines draw as quadrilateral shapes for perspective views
        fill(255)
        quad(WIDTH/3, HEIGHT, (WIDTH/3) + (15), HEIGHT, WIDTH/2, HEIGHT/4, WIDTH/2, HEIGHT/4)
        quad(2*WIDTH/3, HEIGHT, (2*WIDTH/3) - (15), HEIGHT, WIDTH/2, HEIGHT/4, WIDTH/2, HEIGHT/4)
        
    # calculate and display score    
    def scorer(self):
        fill (0,0,0)
        textSize(20)
        text("Score:" + str(self.score), 10, 20)
        if (frameCount%1) == 0:
            self.score += 1
    
    # the main game display
    def display(self):
        # following calls and displays all above mentioned display methods in their required orders
        self.display_background()
        self.display_intructions()
        self.scorer()
        self.speed_incrementer()
        self.create_lines()
        self.display_lines()
        self.display_objects()
        self.car.create_car()
        self.new_obstacles()
        self.delete_bonus()
        self.delete_obstacles()
        self.delete_lines    
        self.check_collision()
        # following displays icons of 2 bonuses on right that the user has picked and also calls function to apply the feature of bonuses
        if self.collision < 0:
            self.display_bonus()
        if self.new == False:
            self.no_obstacles()

# instantiates the game object
game= Game()    
        
def setup():
    frameRate(100)  # required for higher game definition
    size(WIDTH, HEIGHT)
    
def draw():
    if game.collision >= 4:  # if car collides and has no extra life, game ends
        game.end_display()
        
    else:
        game.display()   # display the main game

# to restart a new game with mouse click
def mouseClicked():
    global game
    if game.collision >= 4:
        game = Game()
        
# arrow keys press recorded and respective method called    
def keyPressed():
    if keyCode == LEFT:
        game.car.change_lane("left")
    elif keyCode == RIGHT:
        game.car.change_lane("right")
    elif keyCode == UP:
            game.car.jump= True 
            
# UP arrow key press recorded and respective method called     
def keyReleased():
    if keyCode == UP:
        game.car.jump=False
