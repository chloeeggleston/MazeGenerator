import tkinter as tk
import random
import time

class MazeApp(tk.Frame):
    def __init__(self, width=400, height=300, master=None):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, self.height, self.width, fill="black")
        start = [[i,j,i+10,j+10] for i in range(0,self.width,10) for j in range(0,self.height,10)]
        self.rects = []
        for e in start:
            self.canvas.create_rectangle(e[0],e[1],e[2],e[3],fill='black', outline='black')
        self.states = {}
        for i in range(2, self.width*self.height+2):
            self.states[i] = False

    def toggle(self, i, red):
        if i not in range(2,self.width*self.height+2):
            print("Incorrect id")
        elif not red:
            self.states[i] = not self.states[i]
            if self.states[i]:
                color = "white"
            else:
                color = "black"
            self.canvas.itemconfig(i, fill=color, outline=color)
        else:
            self.states[i] = False
            self.canvas.itemconfig(i, fill="red", outline="red")

    def coords_to_index(self, x, y):
        return x*(self.height//10) + (self.height//10 - y - 1) + 2

    def toggle_c(self,x,y,red=False):
        self.toggle(self.coords_to_index(x,y),red)

    def usable(self, x,y):
        if 0 in [x,y]:
            return False
        if self.width//10 - 2 == x or self.height//10 - 2 == y:
            return False
        corners = [self.coords_to_index(x+1,y),self.coords_to_index(x-1,y),self.coords_to_index(x,y+1),self.coords_to_index(x,y-1)]
        corners = [i for i in corners if i in range(2,self.width*self.height+2)]
        if True in [self.states[elem] for elem in corners]:
            return False
        return True

    def walk(self):
        self.position = [1,1]
        self.filled = []
        self.seen = True
        self.last = [self.position]
        while len(self.last) > 0:
            self.toggle_c(self.position[0], self.position[1], red=True)
            options = [[opt[0]+self.position[0], opt[1]+self.position[1]] for opt in [[0,1],[1,0],[0,-1],[-1,0]]]
            options = [opt for opt in options if self.usable(opt[0], opt[1]) and self.coords_to_index(opt[0],opt[1]) in self.states and opt not in self.filled and not self.states[self.coords_to_index(opt[0],opt[1])]]
            self.filled.append(self.position)
            time.sleep(0.01)
            self.canvas.update()
            self.toggle_c(self.position[0], self.position[1])
            if len(options) == 0:
                self.position = self.last[0]
                self.last = self.last[1:]
            else:
                self.last = [self.position] + self.last
                self.position = random.choice(options)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(master=root)
    app.master.after(0, app.walk)
    app.mainloop()
