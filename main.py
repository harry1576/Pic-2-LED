from tkinter import Tk, Label, Button,colorchooser,filedialog, Frame
from tkinter.constants import BOTTOM, LEFT, RIGHT, TOP
from PIL import Image, ImageDraw, ImageFont
import random


class LED_Controller_GUI:
        
    def __init__(self, root):
        
        root.title("LED Controller")        
        left_frame = Frame(root)         
        right_frame = Frame(root)         

        self.rows = 20
        self.columns = 30
        self.buttons = []
        
        self.main_button_width = int((self.columns * 9.1)/4) 
        self.main_button_height = int((self.rows * 2)/4)      
     
                 
        for x in range(self.rows):
            for i in range(self.columns):
                LED_Number = i+(self.columns*x)
                self.buttons.append(Button(left_frame, text=str(LED_Number).zfill(3),command=lambda c=LED_Number:self.set_colour(c),font=('Helvetica', 6),width = 3,height =  2))
                self.buttons[-1].grid(row=x, column=i)

        uniform_colour_button = Button(right_frame, text="Global Set ",command=self.uniform_colour_set,width = self.main_button_width,height=self.main_button_height,font=('Helvetica', 6))
        uniform_colour_button.grid(row=0, column=self.columns+1)
        
        random_colour_button = Button(right_frame, text="Randomize",command=self.random_colour,width = self.main_button_width,height=self.main_button_height,font=('Helvetica', 6))
        random_colour_button.grid(row=0, column=self.columns+2)    
        
        random_colour_button = Button(right_frame, text="Imagify",command=self.imagify,width = self.main_button_width,height=self.main_button_height,font=('Helvetica', 6))
        random_colour_button.grid(row=0, column=self.columns+3)  
        
        text_file_generate = Button(right_frame, text="Generate Log",command=self.genLog,width=self.main_button_width,height=self.main_button_height,font=('Helvetica', 6))
        text_file_generate.grid(row=0, column=self.columns+4)   
        
        left_frame.pack(side=TOP)
        right_frame.pack(side=BOTTOM)
       
        
        
    def imagify(self):
        file_path = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.im = Image.open(file_path)
        width, height = self.im.size
        pix = self.im.load()
        colour_list = []
        q = 0
        f= open("log_file.txt","w+")
        if width == height:
            q = 5
        for x in range(self.rows):
            for i in range(q,self.columns-q):
                new_colour = pix[int((width/self.columns)*i),int((height/self.rows)*x)]
                colour_list.append(new_colour)
                LED_Number = i+(self.columns*x)
                self.buttons[LED_Number].configure(bg = self._from_rgb(new_colour))
                f.write("leds[" + str(LED_Number) + "] = CRGB" + str(new_colour) + ";\n") 
                          
    def _from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb       
            
    def set_colour(self,number):
        (rgb, hx) = colorchooser.askcolor()
        rgb = (int(rgb[0]),int(rgb[1]),int(rgb[2]))
        self.buttons[number].configure(bg = self._from_rgb(rgb))
        
    def uniform_colour_set(self):
        (rgb, hx) = colorchooser.askcolor()
        rgb = (int(rgb[0]),int(rgb[1]),int(rgb[2]))
        colour_list = []
        for i in range(0,len(self.buttons)):
            colour_list.append(rgb)
            self.buttons[i].configure(bg = self._from_rgb(rgb))
            
    def random_colour(self):
        colour_list = []
        for i in range(0,len(self.buttons)):
            rgb = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
            colour_list.append(rgb)
            self.buttons[i].configure(bg = self._from_rgb(rgb))    
            
    def genLog(self):
        
        f= open("log_file.txt","w+")
        
        for x in range(self.rows):
            for i in range(0,self.columns):
                LED_Number = i+(self.columns*x)       
                new_colour = self.buttons[LED_Number].cget('bg').lstrip('#')
                
                rgb_colour = tuple(int(new_colour[i:i+2], 16) for i in (0, 2 ,4))
                f.write("leds[" + str(LED_Number) + "] = CRGB" + str(rgb_colour) + ";\n")         
          
        
root = Tk()
my_gui = LED_Controller_GUI(root)
root.mainloop()
