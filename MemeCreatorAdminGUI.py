from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math


class Application:
    def __init__(self, root):
        self.root = root
        self.size = (700, 700)
        self.setup_gui()
        self.x1, self.x2, self.y2, self.y1 = 0, 0, 0, 0
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
            self.img = self.img.resize((self.size[0], hsize), Image.ANTIALIAS)
        elif self.img.size[1] > self.size[1]:
            hpercent = ((self.size[1]) / float(self.img.size[1]))
            wsize = int((float(self.img.size[0]) * float(hpercent)))
            self.img = self.img.resize((wsize, self.size[1]), Image.ANTIALIAS)
        self.meme = ImageTk.PhotoImage(self.img)
        self.canvas.delete(ALL)
        self.canvas.create_image(self.size[0]/2.0, self.size[1]/2.0, anchor=CENTER, image=self.meme)

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
        self.x2, self.y2 = event.x, event.y
        if self.x2 < self.x1:
            self.x1, self.x2 = self.x2, self.x1
        if self.y2 < self.y1:
            self.y1, self.y2 = self.y2, self.y1
        width, height = (self.x2 - self.x1), (self.y2 - self.y1)
        print("w", width, "h", height)
        if width < 30 or height < 30:
            messagebox.showwarning("Small content area", "Content area is too small, please select larger area")
        else:
            font_size = 40
            font_type = ImageFont.truetype("../MemeCreatorBot/impact.ttf", font_size)

            im = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(im)
            text = "testing text testing text testing text"
            modifiedtext = ''
            words = text.split()
            currstr = ''
            if draw.textsize(text, font=font_type)[0] < width:
                modifiedtext = text
            else:
                for i in words:
                    if draw.textsize(currstr, font=font_type)[0] + draw.textsize(i, font=font_type)[0] < width:
                        currstr += i + ' '
                    else:
                        modifiedtext += currstr + '\n'
                        currstr = i + ' '
                    if words.index(i) == len(words) - 1:
                        modifiedtext += currstr
                    while draw.textsize(modifiedtext, font=font_type)[1] > height or \
                            draw.textsize(modifiedtext, font=font_type)[0] > width:
                        font_size -= 1
                        font_type = ImageFont.truetype("../MemeCreatorBot/impact.ttf", font_size)
            datas = im.getdata()
            new_data = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            im.putdata(new_data)
            W, H = draw.textsize(modifiedtext, font=font_type)
            draw.text(((width - W) / 2.0, (height - H) / 2.0), modifiedtext, fill=(0, 0, 0),
                      font=font_type,
                      spacing=3, align='center')
            im.show()
            self.text_img = ImageTk.PhotoImage(im)
            self.canvas.create_image(self.x1, self.y1, anchor=NW, image=self.text_img)
            del im

    def fix_pos(self, event):
        self.x1, self.y1 = event.x, event.y


root = Tk()
root.title('MemeCreatorBot helper')
Application(root)
root.resizable(0, 0)
root.mainloop()
