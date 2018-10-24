from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk


class Application:
    def __init__(self, root):
        self.root = root
        self.size = (700, 700)
        self.setup_gui()
        self.x1, self.y1 = 0, 0
        self.line1 = 0
        self.root.config(menu=self.menubar)

    def setup_gui(self):
        self.canvas = Canvas(self.root, width=self.size[0], height=self.size[1], bd=2, relief="solid")
        self.canvas.pack(side=TOP)
        self.canvas.bind("<Button-1>", self.fix_pos)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.draw_final_rect)
        self.canvas.bind("<Escape>", self.clear_canvas)
        self.menubar = Menu(root, tearoff=0)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open Image", command=self.open_image)
        filemenu.add_command(label="Close Image", command=self.close_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)

    def open_image(self):
        self.img = Image.open(filedialog.askopenfilename())
        if self.img.size[0] > self.size[0]:
            wpercent = ((self.size[0]) / float(self.img.size[0]))
            hsize = int((float(self.img.size[1]) * float(wpercent)))
            print("wprecent:", wpercent)
            print("hsize:", hsize)
            self.img = self.img.resize((self.size[0], hsize), Image.ANTIALIAS)
        elif self.img.size[1] > self.size[1]:
            hpercent = ((self.size[1]) / float(self.img.size[1]))
            wsize = int((float(self.img.size[0]) * float(hpercent)))
            print("hprecent:", hpercent)
            print("wsize:", wsize)
            self.img = self.img.resize((wsize, self.size[1]), Image.ANTIALIAS)
        self.meme = ImageTk.PhotoImage(self.img)
        self.canvas.delete(ALL)
        self.canvas.create_image(self.size[0]/2, self.size[1]/2, anchor=CENTER, image=self.meme)

    def close_image(self):
        self.canvas.delete(ALL)

    def clear_canvas(self, event):
        self.canvas.delete(self.line1)
        self.canvas.delete(self.line2)
        self.canvas.delete(self.line3)
        self.canvas.delete(self.line4)

    def draw_rect(self, event):
        if self.canvas.find_all() and self.x1 != 0 and self.y1 != 0:
            if self.line1:
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                self.canvas.delete(self.line3)
                self.canvas.delete(self.line4)
            self.line1 = self.canvas.create_line(self.x1, self.y1, event.x, self.y1, dash=(12, 7), width=2)
            self.line2 = self.canvas.create_line(self.x1, self.y1, self.x1, event.y, dash=(12, 7), width=2)
            self.line3 = self.canvas.create_line(event.x, self.y1, event.x, event.y, dash=(12, 7), width=2)
            self.line4 = self.canvas.create_line(self.x1, event.y, event.x, event.y, dash=(12, 7), width=2)

    def draw_final_rect(self, event):
        self.line1
        self.line2
        self.line3
        self.line4

    def fix_pos(self, event):
        self.x1, self.y1 = event.x, event.y



root = Tk()
root.title('MemeCreatorBot helper')
Application(root)
root.resizable(0, 0)
root.mainloop()
