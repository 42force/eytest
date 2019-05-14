from tkinter import Frame, Canvas, Button, Label, Scale 
import tkinter.messagebox
from base import Neighbour, Transform, World, Patch, Schelling, Plotcoords
import random
 
class Visual(Frame):
    '''Class that takes a world as argument and present it graphically
    on a tkinter canvas.'''
 
    def __init__(self):
        '''Sets up a simulation GUI in tkinter.
        '''
        Frame.__init__(self)
        self.master.title("The Schelling Segregation Model in Python")
        self.master.wm_resizable(0,0) 
        self.grid()
 
        self.movement_possible = True
    
       # --------------------------------------- #
       # --------- FRAMES FOR GUI -------------- #
       # --------------------------------------- #
 
        # The pane for user values
        self._entryPane = Frame(self,
                                borderwidth = 5,
                                relief = 'sunken')
        self._entryPane.grid(row = 0, column = 0, sticky = 'n')
 
        # The buttons pane
        self._buttonPane = Frame(self,
                                 borderwidth = 5)
                                     
        self._buttonPane.grid(row = 1, column = 0, sticky = 'n')
 
        # A temp pane where graph is located, just for cosmetic reasons
        width, height = 425, 350          
        self._graph = Canvas(self,
                             width = width,
                             height = height,
                             background = "black")
        self._graph.configure(relief = 'sunken', border = 2)
 
        self._graph.grid(row = 3, column = 0)        
 
 
        # The pane where the canvas is located    
        self._animationPane = Frame(self,
                                    borderwidth = 5,
                                    relief = 'sunken')
        self._animationPane.grid(row = 0, column = 1, rowspan=4, pady=10, sticky = "n")
 
       # --------------------------------------- #
       # --------- FILLING THE FRAMES ---------- #
       # --------------------------------------- #
 
        self._canvas()      # Create graphics canvas
 
        self._entry()       # Create entry widgets
 
        self._buttons()     # Create button widgets
         
    def _plot_setup(self, time):
        '''Method for crudely annotating the graph window.'''               
        time = time
 
        # Main plot
        width, height = 425, 350
        y0 = -time/10 
        self._graph = Canvas(self, width = width, height = height, background = "black", borderwidth=5)
        self._graph.grid(row = 3, column = 0)         
        self.trans = Plotcoords(width, height, y0, -0.2, time, 1.3) 
         
        x,y = self.trans.screen(time//2,1.2)
        x1,y1 = self.trans.screen(time//2,1.13)
        self._graph.create_text(x,y,  text = "% Happy", fill = "green",font = "bold 12")
        self._graph.create_text(x1,y1,  text = "% Unhappy", fill = "red",font = "bold 12")
 
        # Line x-axis  
        x, y  = self.trans.screen((-5*(time/100)),-0.05)  
        x1, y  = self.trans.screen(time,-0.05)
        self._graph.create_line(x,y,x1,y, fill = "white", width=1.5)
         
        # Text x-axis
        x_text, y_text  = self.trans.screen(time/2,-0.15)        
        self._graph.create_text(x_text,y_text,  text = "Time", fill = "white",font = "bold 12")
         
         
        # Liney-axis        
        x, y  = self.trans.screen((-0.5*(time/100)),-0.05) 
        x, y1  = self.trans.screen((-5*(time/100)), 1)     
        self._graph.create_line(x, y, x, y1, fill = "white", width=1.5)
 
    def _entry(self):
        '''Method for creating widgets for collecting user input.'''
         
        # N (no of turtles)
        dim = 30*30
        self._N_label = Label(self._entryPane,
                              anchor = 'w',
                              justify = 'left',
                              text = "N:",
                              relief = 'raised',
                              width = 12,
                              height = 1,
                              font = "italic 20")
        self._N_label.grid(row = 0, column = 1, ipady=14)
 
        self._N = Scale(self._entryPane,
                              from_ = 1,
                              to = dim-50,  
                                             
                              resolution = 1,
                              bd = 3,
                              relief = 'sunken',
                              orient = 'horizontal',
                              length = 235,
                              tickinterval = 849)
        self._N.set(400) 
        self._N.grid(row = 0, column = 2)
         
 
        # Ticks (lenght of simulation)
        self._Ticks_label = Label(self._entryPane,
                              anchor = 'w',
                              justify = 'left',
                              text = "Time:",
                              relief = 'raised',
                              width = 12,
                              height = 1,
                              font = "bold 20")
        self._Ticks_label.grid(row = 1, column = 1, ipady=14)
 
        self._Ticks = Scale(self._entryPane,
                              from_ = 10,
                              to = 1000,
                              resolution = 1,
                              bd = 3,
                              relief = 'sunken',
                              orient='horizontal',
                              length = 235,
                              tickinterval= 990)
        self._Ticks.set(500) 
        self._Ticks.grid(row = 1, column = 2)
 
        # % similar wanted
        self._Similar_label = Label(self._entryPane,
                                    anchor = 'w',
                                    justify = 'left',
                                    text = "Similar wanted:",
                                    relief = 'raised',
                                    width = 12,
                                    height = 1,
                                    font = "bold 20")
         
        self._Similar_label.grid(row = 2, column = 1, ipady=14)
 
        self._Similar = Scale(self._entryPane,
                              from_ = 0.0,
                              to = 1.0,
                              resolution = 0.01,
                              bd = 3,
                              relief = 'sunken',
                              orient='horizontal',
                              length = 235,
                              tickinterval= 1)
        self._Similar.set(0.76) 
        self._Similar.grid(row = 2, column = 2)
 
 
    def _buttons(self):
        '''Method for creating button widgets for setting up, running and plotting results from simulation.'''
        width = 7
        height = 1
 
        # The 'Setup' button
        self._setupButton = Button(self._buttonPane,
                             text = "Setup",
                             command = self._setup,
                             width = width,
                             height = height,
                             font = "bold 30",
                             relief = 'raised',
                            borderwidth = 5)
        self._setupButton.grid(row = 0, column = 0)
 
        # The 'Go' button
        self._goButton = Button(self._buttonPane,
                          text = "Go",
                          command = self._go,
                          width = width,
                          height = height,
                          font = "bold 30",
                          relief = 'raised',
                            borderwidth = 5)
        self._goButton.grid(row = 0, column = 1)
 
 
        # The 'Quit' button
        self._quitButton = Button(self._buttonPane,
                              text = "Quit",
                              command = self._quit,
                              width = width,
                             height = height,
                             font = "bold 30",
                            relief = 'raised',
                            borderwidth = 5)
        self._quitButton.grid(row = 1, column = 0, columnspan = 2)
 
 
    def _canvas(self):
        '''Creates the canvas on which everything happens.'''
        # The tick counter information
        self._Tick_counter = Label(self._animationPane,
                                    anchor = 'w',
                                    justify = 'left',
                                    text = "Time:",                                    
                                    width = 5,
                                    font = "bold 20")
        self._Tick_counter.grid(row = 0, column = 0, sticky="e")
 
        self._Tick_counter1 = Label(self._animationPane,                                    
                                    justify = 'center',
                                    text = "",
                                    relief = 'raised',
                                    width = 5,
                                    font = "bold 20")
        self._Tick_counter1.grid(row = 0, column = 1, sticky = 'w')
 
        self.canvas_w, self.canvas_h = 750, 750
         
        self.canvas = Canvas(self._animationPane,
                             width =  self.canvas_w,
                             height = self.canvas_h,
                             background = "black")
 
        self.canvas.grid(row = 1, column = 0, columnspan=2)
 
    def _setup(self):
        '''Method for 'Setup' button.'''       
        ## Clearing the canvas and reset the go button
        self.canvas.delete('all')
        self._goButton['relief'] = 'raised'
        self.N = int(self._N.get())
        self.Ticks = int(self._Ticks.get())
        self.similar = float(self._Similar.get())
        self.data = []  
        self.tick_counter = 0
        self._Tick_counter1['text'] = str(self.tick_counter)
        self._plot_setup(self.Ticks)  
        self.grid_size = 30 
        self.world = World(750,750, self.grid_size)
        self.create_turtles()
        self.neighbouring_turtles()
        self.draw_turtles()
         
    def _go(self):
        '''Method for the 'Go' button, i.e. running the simulation.'''
        self._goButton['relief'] = 'sunken'
        if self.tick_counter <= self.Ticks:
            self._Tick_counter1['text'] = str(self.tick_counter)            
            self.canvas.update()
             
            self._graph.update()
            self._graph.after(0)
 
            # Data collection        
            turtles_unhappy = self.check_satisfaction()                                    
            prop_happy, prop_unhappy = self.calc_prop_happy(self.tick_counter)             
 
            self.data_collection(self.tick_counter, prop_happy, prop_unhappy) 
 
            if self.tick_counter >= 1:
                 
                # HAPPY values (%)
                x0 = self.tick_counter-1
                x1 = self.tick_counter
 
                # Collecting values from stored data
                y0 = self.data[self.tick_counter-1][1]
                y1 = self.data[self.tick_counter][1]
 
                # Transforming to tkinter
                x1, y1 = self.trans.screen(x1, y1)
                x0,y0 = self.trans.screen(x0,y0)
                self._graph.create_line(x0, y0, x1, y1 ,fill = "green", width=1.3, tag = "happy") # Draw "happy lines
                 
                # UNHAPPY values (%)
                x0 = self.tick_counter-1
                x1 = self.tick_counter
 
                # Collecting values from stored data
                y0 = self.data[self.tick_counter-1][2]
                y1 = self.data[self.tick_counter][2]
 
                # Transforming to tkinter
                x1, y1 = self.trans.screen(x1, y1)
                x0,y0 = self.trans.screen(x0,y0)
                self._graph.create_line(x0,y0, x1, y1 ,fill = "red", width=1.1, tag = "unhappy") # Draw unhappy lines                  
             
            if prop_happy < 1:                
                self.turtle_move(turtles_unhappy)                            
                self.update_neighbours()                                     
                self.tick_counter += 1
                self.canvas.after(0, self._go())
 
        self._goButton['relief'] = 'raised'
         
    def _quit(self):
        '''Method for the 'Quit' button.'''
        self.master.destroy()
 
    # ------------------------------------------------------ #
    # ---------- FUNCTIONS CALLED AT EACH TICK ------------- #
    # ------------------------------------------------------ #
 
 
    def turtle_move(self, unhappy_turtles):
        '''Moves all the unhappy turtles (randomly).'''
         
        while unhappy_turtles:
            i = random.randint(0, len(unhappy_turtles)-1)
            turtle = unhappy_turtles.pop(i)
            turtle.move(self)
 
    def update_neighbours(self):
        '''Updates the turtles neigbour attributes. Called
        after all turtles have moved.'''
        for turtle in self.turtles:
            turtle.update_neighbours()
 
    def check_satisfaction(self):
        '''Checks to see if turtles are happy or not.
        Returns a list of unhappy turtles, i.e. turtles
        that should move.
 
        Called before the move method.'''
         
        for turtle in self.turtles:
            turtle.is_happy()
         
        unhappy_turtles = []
        for element in self.turtles:
            if not element.happy:
                unhappy_turtles.append(element)
 
        return unhappy_turtles
 
    def calc_prop_happy(self,i):
        '''Calculates the proportion of happy turtles.'''
        happy = 0
        unhappy = 0
         
        for turtle in self.turtles:
            if turtle.happy:
                happy += 1
            else:
                unhappy += 1
        prop_happy = happy/len(self.turtles)
        prop_unhappy = unhappy/len(self.turtles)
 
        return prop_happy, prop_unhappy
         
    def data_collection(self, i, prop_happy, prop_unhappy):
        '''Method for collecting data at each tick.'''
        self.data.append((i,prop_happy, prop_unhappy))
         
 
# ------------------------------------------------------ #
# ---------- INITIALISATION FUNCTIONS ------------------ #
# ------------------------------------------------------ #
 
    def create_turtles(self):
        '''Method for creating a new list of turtles.
 
        Upon creation they are registered in the World object.'''
        if self.N <= self.grid_size*self.grid_size:
            counter = 0
            self.turtles = []
            while counter < self.N:
                             
                s = "S"+str(counter)
                if counter <= int(self.N/2):
                    color = "green"
                else:
                    color = "red"
                 
                x = random.randint(0, self.grid_size-1)
                y = random.randint(0, self.grid_size-1)
 
                if not self.world.patch_list[x][y]:  
                    new_turtle = Schelling(world = self.world,
                                           x = x,
                                           y = y,
                                           s = s,
                                           color = color,
                                           similar_wanted = self.similar)
 
                    self.world.register(new_turtle)  
                    counter += 1
                    self.turtles.append(new_turtle)   
        else:
            print("Number of turtles exceeds world!")
 
    def draw_turtles(self):
        '''Method for drawing turtles on canvas.
 
           Calls each turtle's own method for drawing.'''
        for turtle in self.turtles:
            turtle.draw(self.canvas)
 
    def neighbouring_turtles(self):
        '''Method for updating turtles' neighbours.
 
           Calls on each turtle's own method for updating neighbours.'''
        for turtle in self.turtles:
            turtle.get_neighbouring_patches()