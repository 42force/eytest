import random
import tkinter.messagebox

 
class Neighbour(dict):
    '''Takes a World object as parameter and returns the neigbours of each x & y coordinates in the world.
 
    Is a dictionary with self(x,y) as 'keys' and neigbors x,y as 'values' (which is
    a list consisting of individual neighbour coordinates stored as  x,y tuples).
    '''                         
 
    def __init__(self, world):
        '''At initialisation a dictionary consisting of neigbours all x,y
        values are created.
 
        Neighbour grid:        
        -------------------------
        |(-1,1 )| (0,1 )| (1,1 )|
        -------------------------
        |(-1,0 )| (x,y )| (1,0 )|
        -------------------------
        |(-1,-1)| (0,-1)| (1,-1)|
        ------------------------- '''
         
        dict.__init__({})
        self.world = world
        self.xy = self.world.x_y_list()    
        self.inhabited = world.inhabited()
 
        offset = [(-1, 1),
                  ( 0, 1),
                  ( 1, 1),
                  (-1, 0),
                  ( 1, 0),
                  (-1,-1),
                  ( 0,-1),
                  ( 1,-1)]
 
        for x,y in self.xy:
            tmp = []
            for i in range(len(offset)):
                x1 = x + offset[i][0]
                y1 = y + offset[i][1]
                if 0 <= x1 < self.world.grid_size and 0 <= y1 < self.world.grid_size:
                    tmp.append((x1,y1))
            self[(x,y)] = tmp
 
    def neighbours_xy(self, x, y):
        '''Returns a list of neigbouring x,y values (tuple).
 
        Takes x,y as parameters.
        '''
        try:
            return self[x,y]
        except KeyError as err:
            print(str(err) + " is outside world's coordinate system.")
 
     
    def __str__(self):
        '''Prints the neigbour dictionary.'''
        s = ""
        for key in sorted(self):
            s += str(key) + ":" + str(self[key]) + "\n"
        return s
 
 
class Transform(dict):
    '''Class that takes a World object as input and sets up a dictionary
    with both cartesian and tkinter coordinates.
    '''                          
    def __init__(self, world):
        '''Stores world and set up dictionary containing both
        cartesian and tkinter coordinates.'''
        dict.__init__({})
        self.world = world
        self._x_y_dict()
         
 
    def _x_y_dict(self):
        '''A dictionary consisting of tuples with x, y values.
 
        The lower left corner is 0,0 (cartesian) and their
        respective x, y coordinates in tkinter.'''
        self._graphics_list()
        self._xy_coords_orig()
        self._xy_coords_tkinter()
         
         
        for i in range(len(self.x_y_orig)):
            self[self.x_y_orig[i]] = self.x_y_tkinter[i]
 
    def _xy_coords_orig(self):
        self.x_y_orig = []
        for x in range(self.world.grid_size):
            for y in range(self.world.grid_size):
                self.x_y_orig.append((x,y))        
 
    def _xy_coords_tkinter(self):
        self.x_y_tkinter = []
        for key in sorted(self.visual_dict):
            for i in range(self.world.grid_size):
                self.x_y_tkinter.append((key,self.visual_dict[key][i]))
 
    def _graphics_list(self):
        '''A method for creating a list/dictionary of which to
        create a graphics interface from.'''
 
        self.visual_list = [[0 for row in range(self.world.grid_size)] for row in range(self.world.grid_size)]
        for x in range(self.world.grid_size):
            count = self.world.height - self.world.counter_y
            for y in range(self.world.grid_size):
                self.visual_list[x][y] = count
                count -= self.world.counter_y
 
  
        x = 0
        self.visual_dict = {}
        for element in self.visual_list:
            self.visual_dict[x] = element
            x += self.world.counter_x
                 
    def tkinter_coords(self, x, y):
        '''Returns tkinter x, y values (tuple)
 
        Takes cartesian x,y as parameters.'''
        try:
            return self[x,y]
        except KeyError as err:
            print(str(err) + " is outside world's coordinate system.")
 
    def __str__(self):
        '''Prints the coordinates dictionary.
        'keys' are cartesian while 'values' are tkinter.'''
        s = ""
        for key in sorted(self):
            s += str(key) + ":" + str(self[key]) + "\n"
        return s
 
class World(object):
    '''A n X n grid as a spatial representation of a world where things happen.'''
      
    def __init__(self, width, height, n = 2):
        self.width = width
        self.height = height
        self.grid_size = n
 
        self.counter_x = self.width/self.grid_size               
        self.counter_y = self.height/self.grid_size              
        self.coordinates = Transform(self)                       
        self.patch_list = [[0 for row in range(n)] for row in range(n)] 
         
        self.neighbour = Neighbour(self)                 
         
    def patches(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if not self.patch_list[x][y]:  
                    new_patch = Patch(world = self, x = x, y = y, s = 'P')                    
                    self.register(new_patch)
 
    def x_y_tkinter(self, x, y):
        '''Returns the tkinter coordinates from cartesian x,y,
        i.e. it calls on a method in Transform.'''
        return self.coordinates.tkinter_coords(x,y)
 
    def x_y_list(self):
        '''Returns the list of the world's x,y coordinates (cartesian).'''
        return self.coordinates.x_y_orig
 
    def inhabited(self):
        '''Returns the list of cells with patches.'''
        return self.patch_list
 
    def register(self, patch):
        '''Register a patch in the World, i.e. put the patch at it's
        coordinates in the World's patch_list.'''
        x = patch.x
        y = patch.y
        self.patch_list[x][y] = patch
 
    def remove(self, patch):
        '''Remove a patch from the World, i.e. put remove the patch from
        it's current coordinates in the World's patch_list by replacing it with zero.'''
 
        x = patch.x
        y = patch.y
        self.patch_list[x][y] = 0
 
class Patch(object):
    '''A class that defines separate entity called Patch.
 
    They inhabit a world and conceptualises a patch in an artificial
    n x n spatial environment.
    '''
    def __init__(self, world, x = 0, y = 0, s = "P", color = 'dark green'):
        '''Initialise the patches and their position.'''
        self.world = world
        self.name = s
        self.x = x
        self.y = y
        self.color = color
        self.x_draw, self.y_draw = self.world.x_y_tkinter(self.x,self.y)      
        self.get_neighbours()      
 
    def position(self):
        '''Return coordinates of current position.'''
        return self.x, self.y, self.x_draw, self.y_draw
 
    def draw(self, canvas, text1 = False):
        '''Method for drawing a patch.
 
        text1 is a helper parameter to check coordinates,
        both cartesian and tkinter.'''
 
 
        x = self.x_draw
        y = self.y_draw
        canvas.create_rectangle(x,y,\
                                x+self.world.counter_x, \
                                y+self.world.counter_y, \
                                fill = self.color, tag = self.name)        
        # Debugging    
        if text1:
            font = 'Arial ' + str(int(self.world.counter_y//6))
            font1 = 'Arial ' + str(int(self.world.counter_y//7))
 
            canvas.create_text(x+5,y+(self.world.counter_y/10), \
                                     text = "(" + str(self.x) + "," + str(self.y)+ ")", \
                                     anchor = 'nw',justify = 'center',font = font)
            canvas.create_text(x+5,y+self.world.counter_y-(self.world.counter_y/1.5), \
                                     text = "(" + str(int(x)) + "," + str(int(y))+ ")", \
                                     anchor = 'nw',justify = 'center', font = font1)
 
            c, c1 = canvas.coords(self.name)[0], canvas.coords(self.name)[1]
            c = int(c)
            c1 = int(c1)
            canvas.create_text(x+5,y+self.world.counter_y-(self.world.counter_y/2.5), \
                               text = "(" + str(c) + "," + str(c1) + ")", \
                                     anchor = 'nw',justify = 'center', font = font1)
 
    def draw_move(self, canvas, x_old, y_old, text1 = False):
        '''Move using canvas.move method'''
         
 
        canvas.move(self.name, self.x_draw-x_old, self.y_draw-y_old)
 
        # Debugging    
        if text1 == True:
            x = self.x_draw
            y = self.y_draw
 
            font = 'Arial ' + str(int(self.world.counter_y//6))
            font1 = 'Arial ' + str(int(self.world.counter_y//7))
 
            canvas.create_text(x+5,y+(self.world.counter_y/10), \
                                     text = "(" + str(self.x) + "," + str(self.y)+ ")", \
                                     anchor = 'nw',justify = 'center',font = font)
            canvas.create_text(x+5,y+self.world.counter_y-(self.world.counter_y/1.5), \
                                     text = "(" + str(int(x)) + "," + str(int(y))+ ")", \
                                     anchor = 'nw',justify = 'center', font = font1)
 
            c, c1 = canvas.coords(self.name)[0], canvas.coords(self.name)[1]
            c = int(c)
            c1 = int(c1)
            canvas.create_text(x+5,y+self.world.counter_y-(self.world.counter_y/2.5), \
                               text = "(" + str(c) + "," + str(c1) + ")", \
                                     anchor = 'nw',justify = 'center', font = font1)
 
 
    def get_neighbours(self):
        '''Method for getting the Patch's neighbours x, y coordinates.
 
        Stores them in a list.'''
        self.neighbours = self.world.neighbour.neighbours_xy(self.x, self.y)   
 
    def get_neighbouring_patches(self):
        '''Method for creating a list containing neighbouring pathces.
 
        Stores them in a list.'''
 
        self.neighbours_patches = []
        for x,y in self.neighbours:
            if self.world.patch_list[x][y]:                
 
                patch = self.world.patch_list[x][y]
             
                self.neighbours_patches.append(patch)
             
    def set_color(self, color):
        '''Method to set the color.'''
        self.color = color
 
    def __str__(self):
        '''String representation when printing object.'''
        x, y, z, w = self.position()
        s = self.name + ":" + "(" + str(x) + "," + str(y) + ")"
        return s
 
class Schelling(Patch):
    '''An object that inherits from the Patch class.
 
       Added functionality consist of movement.'''
     
    def __init__(self, world, x = 0, y = 0, s = "S", color = 'dark green', similar_wanted = 0.3):
        Patch.__init__(self, world, x, y, s, color)
        self.happy = False
        self.percent_similar = similar_wanted        
   
    def move(self, visual, debug = False):
        '''Move method - can move to random location in the world.
 
        When debug = True helpful info for checking
        if everything works as intended is printed.'''
         
        if not any(0 in element for element in self.world.patch_list):   
            
            tkinter.messagebox.showwarning("Warning", "No place to move!")          
            visual.movement_possible = False
            visual.master.destroy()
            quit()
 
        else:# new x,y
            x = random.randint(0, self.world.grid_size-1)
            y = random.randint(0, self.world.grid_size-1)
             
            while self.world.patch_list[x][y] != 0:
                x = random.randint(0, self.world.grid_size-1)
                y = random.randint(0, self.world.grid_size-1)
             
 
            if debug:
                print('Move, {}, from ({},{}) to ({},{}) '.format(\
                    self.name, self.x, self.y, x, y))
 
            # Remove from previous location
            self.world.remove(self)
             
            # Update patch
            self.x, self.y = x, y                                            
            x_old, y_old = self.x_draw, self.y_draw
 
            self.x_draw, self.y_draw = self.world.x_y_tkinter(self.x,self.y) 
 
            # Register and draw patch at new coordinates
            self.world.register(self)
            self.draw_move(visual.canvas, x_old, y_old)
 
    def update_neighbours(self):
        '''A method that update the Schelling's neigbours attributes,
        i.e. both x,y for neighbours and list of neigbouring pathces.'''
        self.get_neighbours()                                            
        self.get_neighbouring_patches()                                  
 
    def is_happy(self):
        '''Method to check if whether Schelling is happy or not, i.e.
        if a given percentage or above of neighbouring objects are similar
        to itself, the object is happy.
        '''      
        no_neighbours = len(self.neighbours_patches)               
         
        if no_neighbours > 0:                                      
            similar = 0
            for other in self.neighbours_patches:
                if other.color == self.color:
                    similar += 1
            prop_similar = similar/no_neighbours                 
 
            if prop_similar >= self.percent_similar:              
                                                                   
                self.happy = True
            else:
                self.happy = False
        else:
             
            self.happy = False
         
class Plotcoords:
 
    """Internal class for 2-D coordinate transformations.
 
       Adopted from graphics.py by Jonh Zelle for use with the book
       'Python Programming: An Introduction to Computer Science' Link:
       http://mcsp.wartburg.edu/zelle/python. """
     
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
         
    def screen(self,x,y):        
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)