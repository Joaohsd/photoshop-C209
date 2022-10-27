import tkinter as tk
from tkinter import DoubleVar, ttk
from tkinter import Canvas
from tkinter import filedialog
from tkinter import RIDGE, GROOVE, HORIZONTAL
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os

class Photoshop(tk.Tk):
    def __init__(self):
        # Calling super method
        super().__init__()

        # Information for image
        self.img = None
        self.imgCanvas = None
        self.imgPath = None
        
        # Modeling the application
        self.title("Photo Editor App")
        self.geometry('640x640')

        # Setting Buttons
        # Select Image Button
        self.buttonSelect = tk.Button(self, text="Select Image", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE)
        self.buttonSelect['command'] = self.selectImage
        self.buttonSelect.place(x=60, y=595)
        # Save Image Button
        self.buttonSave = tk.Button(self, text="Save", width=12, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE)
        self.buttonSave['command'] = self.save
        self.buttonSave.place(x=280, y=595)
        # Exit Button
        self.buttonExit = tk.Button(self, text="Exit", width=12, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE)
        self.buttonExit['command'] = self.exit
        self.buttonExit.place(x=460, y=595)

        # Setting Tools for the editor
        self.blurrLabel = tk.Label(self, text="Blur:", font=("ariel 17 bold"), width=9, anchor='e')
        self.blurrLabel.place(x=15, y=8)
        self.blurrValue = tk.DoubleVar()
        self.blurrSlider = ttk.Scale(self, from_=0, to=10, variable=self.blurrValue, orient=HORIZONTAL)
        self.blurrSlider['command'] = self.blurr
        self.blurrSlider.place(x=150, y=10)

        # Setting Canvas to display image
        self.canvas = Canvas(self, width="600", height="420", relief=RIDGE, bd=2)
        self.canvas.place(x=15, y=150)

    def blurr(self):
        for m in range(0, self.blurrValue.get()+1):
            img = self.img.filter(ImageFilter.BoxBlur(m))
            self.img = ImageTk.PhotoImage(img)
            self.canvas.create_image(300, 210, image=self.img)
            self.canvas.image = self.img

    
    def selectImage(self):
        self.img_path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.img = Image.open(self.img_path)
        self.img.thumbnail((350, 350))
        self.imgCanvas = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(300, 210, image=self.imgCanvas)
        self.canvas.image = self.imgCanvas

    def save(self):
        extension = self.img_path.split(".")[-1]
        file = asksaveasfilename(defaultextension=f".{extension}", filetypes=[("All Files", "*.*"), ("PNG file", "*.png"), ("jpg file", "*.jpg")])
        if file:
            self.img.save(file)
        else:
            showinfo(title='Information', message='Not saved!')

    def exit(self):
        showinfo(title='Information', message='Bye!')
        self.destroy()
    
    