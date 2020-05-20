from PIL import Image, ImageDraw
from os import path, remove
import random
import imageio

class MazeApp:
    def __init__(self, width=400, height=300, t=0.025):
        self.width = width
        self.height = height
        self.t = t
        self.image = Image.new('RGB', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.rects = [[i,j,i+10,j+10] for i in range(0,self.width,10) for j in range(0,self.height,10)]
        self.states = {}
        for i in range(len(self.rects)):
            self.states[i] = False        
    
    def coords_to_index(self, x, y):
        return x*(self.height//10) + (self.height//10 - y - 1)

    def toggle_c(self,x,y,red=False):
        self.toggle(self.coords_to_index(x,y),red)
    
    def toggle(self, i, red):
        if i not in self.states:
            print("Incorrect id")
        elif not red:
            self.states[i] = not self.states[i]
            if self.states[i]:
                color = "white"
            else:
                color = "black"
            self.draw.rectangle(self.rects[i],fill=color) 
        else:
            self.states[i] = False
            self.draw.rectangle(self.rects[i],fill='red') 
    
    def usable(self, x,y):
        if self.coords_to_index(x,y) not in self.states:
            return False
        if 0 in [x,y]:
            return False
        if self.width//10 - 1  == x or self.height//10 - 1 == y:
            return False
        corners = [self.coords_to_index(x+1,y),self.coords_to_index(x-1,y),self.coords_to_index(x,y+1),self.coords_to_index(x,y-1)]
        corners = [i for i in corners if i in range(self.width*self.height)]
        if True in [self.states[elem] for elem in corners]:
            return False
        return True

    def walk(self):
        images = []
        self.position = [1,1]
        self.filled = []
        self.seen = True
        self.last = [self.position]
        while len(self.last) > 0:
            self.toggle_c(self.position[0], self.position[1], red=True)
            options = [[[opt[0]+self.position[0], opt[1]+self.position[1]],[2*opt[0]+self.position[0], 2*opt[1]+self.position[1]]] for opt in [[0,1],[1,0],[0,-1],[-1,0]]]
            options = [opt for opt in options if self.usable(opt[0][0], opt[0][1]) and self.usable(opt[1][0],opt[1][1]) and opt[0] not in self.filled and opt[1] not in self.filled and not self.states[self.coords_to_index(opt[0][0],opt[0][1])] and not self.states[self.coords_to_index(opt[1][0], opt[1][1])]]
            self.filled.append(self.position)
            self.image.save("mazetemp{}.png".format(len(images)))
            images.append("mazetemp{}.png".format(len(images)))
            
            self.toggle_c(self.position[0], self.position[1])
            if len(options) == 0:
                self.position = self.last[0]
                self.last = self.last[1:]
            else:
                self.last = [self.position] + self.last
                self.position = random.choice(options)
                self.filled.append(self.position[0])
                self.toggle_c(self.position[0][0], self.position[0][1], red=True)
                self.image.save("mazetemp{}.png".format(len(images)))
                images.append("mazetemp{}.png".format(len(images)))
                self.toggle_c(self.position[0][0], self.position[0][1])
                self.position = self.position[1]
        
        data = [imageio.imread(i) for i in images]
       
        x = 0
        name = "maze{}.gif".format(x)
        while path.exists(name):
            x += 1
            name = "maze{}.gif".format(x)
        imageio.mimsave(name, data, subrectangles=True, duration=self.t)
        for im in images:
            remove(im)

a = MazeApp()
a.walk()
