from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


class Application:
    def __init__(self, root):
        self.root = root
        self.size = (300, 300)
        self.setup_gui()
        self.x1, self.x2, self.y2, self.y1 = 0, 0, 0, 0
        self.line1 = 0
        self.areas_info = dict()
        self.root.config(menu=self.menubar)

    def setup_gui(self):
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(side=LEFT)
        self.canvas = Canvas(self.canvas_frame, width=self.size[0], height=self.size[1], bd=2, relief="solid")
        self.canvas.bind("<Button-1>", self.fix_pos)
        self.canvas.bind("<B1-Motion>", self.draw_rect)
        self.canvas.bind("<ButtonRelease-1>", self.draw_final_rect)
        self.root.bind("<Escape>", self.clear_canvas)
        hbar = Scrollbar(self.canvas_frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.canvas.xview)
        vbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=self.size[0] - 200, height=self.size[1])
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(expand=True, fill=BOTH)
        self.menubar = Menu(self.root, tearoff=0)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open Image", command=self.open_image)
        filemenu.add_command(label="Close Image", command=self.close_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)

    def open_image(self):
        self.img = Image.open(filedialog.askopenfilename())
        self.canvas.config(width=self.img.width, height=self.img.height)
        if not self.canvas.find_all():
            self.toolbar = Frame(self.root)
            self.toolbar.pack(side=RIGHT)
            self.add_area_button = Button(self.toolbar, text="Add content area")
            self.add_area_button.pack()
            self.save_area_button = Button(self.toolbar, text="Save config for current content area")
            self.save_area_button.bind("<Button-1>", self.save_area)
            self.save_area_button.pack()
            self.rotate_label = Label(self.toolbar, text="Set the rotation of the area")
            self.rotate_label.pack()
            self.rotation = Scale(self.toolbar, from_=-180, to=180, tickinterval=180, orient=HORIZONTAL, length=180)
            self.rotation.set(0)
            self.rotation.pack()
            self.entry_label = Label(self.toolbar, text="Test with text input")
            self.entry_label.pack()
            self.sv = StringVar()
            self.sv.trace_add("write", self.get_text)
            self.text_entry = Entry(self.toolbar, textvariable=self.sv)
            self.text_entry.pack()
        '''if self.img.size[0] > self.size[0]:
            wpercent = ((self.size[0] - 200) / float(self.img.size[0]))
            hsize = int((float(self.img.size[1]) * float(wpercent)))
            self.img = self.img.resize((self.size[0] - 200, hsize), Image.ANTIALIAS)
        if self.img.size[1] > self.size[1]:
            hpercent = ((self.size[1]) / float(self.img.size[1]))
            wsize = int((float(self.img.size[0] - 200) * float(hpercent)))
            self.img = self.img.resize((wsize, self.size[1]), Image.ANTIALIAS)'''
        self.meme = ImageTk.PhotoImage(self.img)
        self.canvas.delete(ALL)
        self.canvas.create_image(self.img.width/2.0, self.img.height/2.0, anchor=CENTER, image=self.meme)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def close_image(self):
        self.canvas.delete(ALL)
        self.toolbar.pack_forget()

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

    def fix_pos(self, event):
        self.x1, self.y1 = event.x, event.y

    def get_text(self, *args):
        if self.x2 < self.x1:
            self.x1, self.x2 = self.x2, self.x1
        if self.y2 < self.y1:
            self.y1, self.y2 = self.y2, self.y1
        width, height = (self.x2 - self.x1), (self.y2 - self.y1)
        print ("x:", self.x1, "y:", self.y2, "width:", width, "height:", height)
        if width < 30 or height < 30:
            messagebox.showwarning("Small content area", "Content area is too small, please select larger area")
        else:
            font_size = 40
            font_type = ImageFont.truetype("../MemeCreatorBot/impact.ttf", font_size)
            im = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(im)
            text = self.sv.get()
            modifiedtext = ''
            currstr = ''
            if draw.textsize(text, font=font_type)[0] < width:
                modifiedtext = text
            else:
                words = text.split()
                for i in range(len(words)):
                    if draw.textsize(currstr, font=font_type)[0] + draw.textsize(words[i], font=font_type)[0] < width:
                        currstr += words[i] + ' '
                    else:
                        modifiedtext += currstr + '\n'
                        currstr = words[i] + ' '
                    if i == len(words) - 1:
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
                      font=font_type, spacing=3, align='center')
            self.text_img = ImageTk.PhotoImage(im)
            self.canvas.create_image(self.x1, self.y1, anchor=NW, image=self.text_img)
            del im




root = Tk()
root.title('MemeCreatorBot helper')
Application(root)
root.resizable(0, 0)
root.mainloop()
