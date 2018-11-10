from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math


class Application:
    def __init__(self, root):
        self.root = root
        self.size = (300, 300)
        self.setup_gui()
        self.x1, self.x2, self.y2, self.y1 = 0, 0, 0, 0
        self.text_color = StringVar()
        self.rotation_deg = 0
        self.line1 = 0
        self.areas_info = dict()
        self.class_data = ""
        self.dict_data = ""
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
        try:
            img = Image.open(filedialog.askopenfilename())
        except:
            return
        if img.width > self.root.winfo_screenwidth() or img.height > self.root.winfo_screenheight():
            if img.width > self.root.winfo_screenwidth():
                self.canvas.config(width=self.root.winfo_screenwidth(), height=img.height)
            elif img.height > self.root.winfo_screenheight():
                self.canvas.config(width=img.width, height=self.root.winfo_screenheight() - 110)
        else:
            self.canvas.config(width=img.width, height=img.height)
        if not self.canvas.find_all():
            self.toolbar = Frame(self.root)
            self.toolbar.pack(side=RIGHT)
            self.meme_name = StringVar()
            self.meme_var_name = StringVar()
            meme_name_label = Label(self.toolbar, text="Input the name of the meme")
            meme_name_label.grid(row=0, column=0)
            meme_name_input = Entry(self.toolbar, textvariable=self.meme_name)
            meme_name_input.grid(row=1, column=0)
            meme_var_name_label = Label(self.toolbar,
                                        text="Input the name of the variable, where the data will be stored in",
                                        wraplength=200)
            meme_var_name_label.grid(row=0, column=1)
            meme_var_name_input = Entry(self.toolbar, textvariable=self.meme_var_name)
            meme_var_name_input.grid(row=1, column=1)
            add_area_button = Button(self.toolbar, text="Add content area", command=self.add_area)
            add_area_button.grid(row=2, column=0, sticky=S)
            delete_area_button = Button(self.toolbar, text="Delete content area", command=self.delete_area)
            delete_area_button.grid(row=3, column=0)
            save_meme_button = Button(self.toolbar, text="Save current meme", command=self.save_meme)
            save_meme_button.grid(row=4, column=0, sticky=N)
            self.datalist = Listbox(self.toolbar, selectmode=EXTENDED)
            self.datalist.grid(row=2, column=1, rowspan=3, pady=(20, 0))
            rotate_label = Label(self.toolbar, text="Set the rotation of the area:")
            rotate_label.grid(row=5, columnspan=2, pady=10)
            rotation = Scale(self.toolbar, from_=-180, to=180, tickinterval=180, orient=HORIZONTAL, length=180, command=self.rotate_area)
            rotation.set(0)
            rotation.grid(row=6, columnspan=2)
            entry_label = Label(self.toolbar, text="Test with text input:")
            entry_label.grid(row=7, columnspan=2, pady=10)
            self.sv = StringVar()
            self.sv.trace_add("write", self.get_text)
            text_entry = Entry(self.toolbar, textvariable=self.sv)
            text_entry.grid(row=8, columnspan=2)
            rb_label = Label(self.toolbar, text="Select text color:")
            rb_label.grid(row=9, columnspan=2, pady=(10, 0))
            black_button = Radiobutton(self.toolbar, text="Black", variable=self.text_color, value="(0, 0, 0)")
            black_button.grid(row=10, column=0, pady=(0, 5))
            white_button = Radiobutton(self.toolbar, text="White", variable=self.text_color, value="(255, 255, 255)")
            white_button.grid(row=10, column=1, pady=(0, 5))
            black_button.select()
        try:
            text_entry.delete(0, END)
        except:
            pass
        self.meme = ImageTk.PhotoImage(img)
        self.canvas.delete(ALL)
        self.canvas.create_image(img.width / 2.0, img.height / 2.0, anchor=CENTER, image=self.meme)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # Adding selected area to the areas' dictionary
    def add_area(self):
        if self.x1 > 0 and self.x2 > 0 and self.y1 > 0 and self.y2 > 0:
            self.areas_info[(self.width, self.height)] = (self.x1, self.y1)
            self.datalist.insert(END, "(" + str(self.width) + ", " + str(
                self.height) + ")" + ": " + "(" + str(self.x1) + ", " + str(self.y1) + ")")
        else:
            messagebox.showwarning("No area was selected", "Please select an area on the picture")

    # Deleting area, selected in the listbox, from the dictionary of areas
    def delete_area(self):
        if self.datalist.curselection():
            selection = self.datalist.curselection()
            for i in selection[::-1]:
                width = int(self.datalist.get(i).split(":")[0].split(", ")[0][1:])
                height = int(self.datalist.get(i).split(":")[0].split(", ")[1][:-1])
                del self.areas_info[(width, height)]
                print(self.areas_info)
                self.datalist.delete(i)
        else:
            messagebox.showwarning("Select area to delete", "Please, select area or areas in the list to delete")

    # Save collected data to the MemeCreatorBot source file
    def save_meme(self):
        if self.datalist.index(END) != 0 and self.meme_var_name.get() != "" and self.meme_name:
            self.class_data += (self.meme_var_name.get().strip() + " = Meme({")
            counter = 1
            for w, h in self.areas_info:
                self.class_data += ("(" + str(w) + ", " + str(h) + "): (" + str(self.areas_info[w, h][0]) + ", " + str(self.areas_info[w, h][1]) + ")")
                counter += 1
                if counter <= len(self.areas_info):
                    self.class_data += ", "
            self.class_data += "}, 'impact.ttf', "
            self.class_data += self.text_color.get()
            self.class_data += ")"
            self.dict_data += ("'" + self.meme_name.get().strip().lower() + "': " + self.meme_var_name.get().strip())
            file_name = filedialog.askopenfilename()
            with open(file_name, "r", encoding="utf8") as in_file:
                buffer = in_file.readlines()
            with open(file_name, "w") as out_file:
                for line in buffer:
                    if line.startswith("Memes = {"):
                        line = self.class_data + '\n' + line
                    elif "#end" in line:
                        line = "         " + self.dict_data + ", " + line.lstrip()
                    out_file.write(line)
        else:
            messagebox.showwarning("No data to save", "Please input all the necessary data")

    # Rotate selected area for the given number of degrees
    def rotate_area(self, value):
        self.rotation_deg = int(value)
        center = (self.x1 + (self.x2-self.x1)/2, self.y1 + (self.y2-self.y1)/2)
        points = [(self.x1, self.y1), (self.x1, self.y2), (self.x2, self.y1), (self.x2, self.y2)]
        rotated_points = []
        for point in points:
            tempX = point[0] - center[0]
            tempY = point[1] - center[1]
            rotatedX = tempX * math.cos(self.rotation_deg * (math.pi/180)) - tempY * math.sin(self.rotation_deg * (math.pi/180))
            rotatedY = tempX * math.sin(self.rotation_deg * (math.pi/180)) + tempY * math.cos(self.rotation_deg * (math.pi/180))
            rotated_points.append((rotatedX + center[0], rotatedY + center[1]))
        if self.canvas.find_all() and self.x1 != 0 and self.y1 != 0:
            if self.line1:
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                self.canvas.delete(self.line3)
                self.canvas.delete(self.line4)
            self.line1 = self.canvas.create_line(rotated_points[0], rotated_points[2], dash=(12, 7), width=2)
            self.line2 = self.canvas.create_line(rotated_points[0], rotated_points[1], dash=(12, 7), width=2)
            self.line3 = self.canvas.create_line(rotated_points[2], rotated_points[3], dash=(12, 7), width=2)
            self.line4 = self.canvas.create_line(rotated_points[1], rotated_points[3], dash=(12, 7), width=2)


    # Clear the canvas from the contents and hide the toolbar
    def close_image(self):
        if self.canvas.find_all():
            self.canvas.delete(ALL)
            self.toolbar.pack_forget()
        else:
            pass

    def clear_canvas(self, event):
        self.canvas.delete(self.line1)
        self.canvas.delete(self.line2)
        self.canvas.delete(self.line3)
        self.canvas.delete(self.line4)

    def draw_rect(self, event):
        canvas = event.widget
        if self.canvas.find_all() and self.x1 != 0 and self.y1 != 0:
            if self.line1:
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                self.canvas.delete(self.line3)
                self.canvas.delete(self.line4)
            self.line1 = self.canvas.create_line(self.x1, self.y1, canvas.canvasx(event.x), self.y1, dash=(12, 7),
                                                 width=2)
            self.line2 = self.canvas.create_line(self.x1, self.y1, self.x1, canvas.canvasy(event.y), dash=(12, 7),
                                                 width=2)
            self.line3 = self.canvas.create_line(canvas.canvasx(event.x), self.y1, canvas.canvasx(event.x),
                                                 canvas.canvasy(event.y), dash=(12, 7), width=2)
            self.line4 = self.canvas.create_line(self.x1, canvas.canvasy(event.y), canvas.canvasx(event.x),
                                                 canvas.canvasy(event.y), dash=(12, 7), width=2)

    def draw_final_rect(self, event):
        canvas = event.widget
        self.x2, self.y2 = int(canvas.canvasx(event.x)), int(canvas.canvasy(event.y))
        if self.x2 < self.x1:
            self.x1, self.x2 = self.x2, self.x1
        if self.y2 < self.y1:
            self.y1, self.y2 = self.y2, self.y1
        self.width, self.height = int((self.x2 - self.x1)), int((self.y2 - self.y1))

    def fix_pos(self, event):
        canvas = event.widget
        self.x1, self.y1 = int(canvas.canvasx(event.x)), int(canvas.canvasy(event.y))

    def get_text(self, *args):
        if self.width < 30 or self.height < 30:
            messagebox.showwarning("Small content area", "Content area is too small, please select larger area")
        else:
            font_size = 40
            if self.text_color.get() == "(0, 0, 0)":
                txt_color = (0, 0, 0)
            else:
                txt_color = (255, 255, 255)
            font_type = ImageFont.truetype("../MemeCreatorBot/impact.ttf", font_size)
            im = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(im)
            text = self.sv.get()
            modifiedtext = ''
            currstr = ''
            if draw.textsize(text, font=font_type)[0] < self.width:
                modifiedtext = text
            else:
                words = text.split()
                for i in range(len(words)):
                    if draw.textsize(currstr, font=font_type)[0] + draw.textsize(words[i], font=font_type)[0] < self.width:
                        currstr += words[i] + ' '
                    else:
                        modifiedtext += currstr + '\n'
                        currstr = words[i] + ' '
                    if i == len(words) - 1:
                        modifiedtext += currstr
                while draw.textsize(modifiedtext, font=font_type)[1] > self.height or \
                        draw.textsize(modifiedtext, font=font_type)[0] > self.width:
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
            draw.text(((self.width - W) / 2.0, (self.height - H) / 2.0), modifiedtext, fill=txt_color,
                      font=font_type, spacing=3, align='center')
            self.text_img = ImageTk.PhotoImage(im)
            self.canvas.create_image(self.x1, self.y1, anchor=NW, image=self.text_img)
            del im


root = Tk()
root.title('MemeCreatorBot helper')
Application(root)
root.resizable(0, 0)
root.mainloop()
