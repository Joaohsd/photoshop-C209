import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import filedialog
from tkinter import RIDGE, GROOVE, HORIZONTAL
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing_extensions import IntVar
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import os

class Photoshop(tk.Tk):
    def __init__(self):
        # Calling super method
        super().__init__()

        # Information for image
        self.imgOrig = None
        self.imgUp = None
        self.imgNumpy = None
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
        # Blurr tool
        self.blurrLabel = tk.Label(self, text="Blur:", font=("ariel 17 bold"), width=9, anchor='e')
        self.blurrLabel.place(x=8, y=10)
        self.blurrValue = tk.IntVar()
        self.blurrSlider = ttk.Scale(self, from_=0, to=5, variable=self.blurrValue, orient=HORIZONTAL)
        self.blurrSlider['command'] = self.blurr
        self.blurrSlider.place(x=150, y=15)
        # Brightness tool
        self.brightnessLabel = tk.Label(self, text="Brightness:", font=("ariel 17 bold"))
        self.brightnessLabel.place(x=8, y=50)
        self.brightnessValue = tk.IntVar()
        self.brightnessSlider = ttk.Scale(self, from_=1, to=10, variable=self.brightnessValue, orient=HORIZONTAL)
        self.brightnessSlider['command'] = self.brightness
        self.brightnessSlider.place(x=150, y=55)
        # Greyscale tool
        self.greyscaleLabel = tk.Label(self, text="Greyscale:", font=("ariel 17 bold"))
        self.greyscaleLabel.place(x=8, y=90)
        self.greyscaleValue = tk.IntVar()
        self.greyscaleSlider = ttk.Scale(self, from_=1, to=10, variable=self.greyscaleValue, orient=HORIZONTAL)
        self.greyscaleSlider['command'] = self.greyscale
        self.greyscaleSlider.place(x=150, y=95)

        # Rotate Tool
        self.rotateLabel = tk.Label(self, text="Rotate:", font=("ariel 17 bold"))
        self.rotateLabel.place(x=370, y=8)
        values = [0, 45, 90, 135, 180, 225, 270, 315, 360]
        self.rotateOptions = ttk.Combobox(self, values=values, font=('ariel 10 bold'))
        self.rotateOptions.place(x=460, y=15)
        self.rotateOptions.bind("<<ComboboxSelected>>", self.rotate)
        # Flip Tool
        self.flipLabel = tk.Label(self, text="Flip:", font=("ariel 17 bold"))
        self.flipLabel.place(x=400, y=50)
        self.reflectionValues = ["Y REFLECTION", "X REFLECTION "]
        self.flipOptions = ttk.Combobox(self, values=self.reflectionValues, font=('ariel 10 bold'))
        self.flipOptions.place(x=460, y=57)
        self.flipOptions.bind("<<ComboboxSelected>>", self.flip)
        # Setting Canvas to display image
        self.canvas = Canvas(self, width="600", height="420", relief=RIDGE, bd=2)
        self.canvas.place(x=15, y=150)

    def blurr(self, event):
        for m in range(0, self.blurrValue.get()+1):
            imgBlurr = self.imgOrig.filter(ImageFilter.BoxBlur(m))
            self.imgUp = imgBlurr
            self.imgNumpy = np.array(imgBlurr)
            self.imgCanvas = ImageTk.PhotoImage(imgBlurr)
            self.canvas.create_image(300, 210, image=self.imgCanvas)
            self.canvas.image = self.imgCanvas
    
    def brightness(self, event):
        for m in range(0, self.brightnessValue.get()+1):
            imgg = ImageEnhance.Brightness(self.imgOrig)
            img2 = imgg.enhance(m)
            self.imgUp = img2
            self.imgNumpy = np.array(img2)
            img3 = ImageTk.PhotoImage(img2)
            self.canvas.create_image(300, 210, image=img3)
            self.canvas.image = img3

    def greyscale(self, event):
        if self.GreyOption.get():
            imgGrey = self.imgUp.convert('L')
            self.imgUp = imgGrey
            self.imgNumpy = np.array(imgGrey)
            self.imgCanvas = ImageTk.PhotoImage(imgGrey)
            self.canvas.create_image(300, 210, image=self.imgCanvas)
            self.canvas.image = self.imgCanvas
        
    def rotate(self, event):
        imgRotate = self.imgUp.rotate(float(self.rotateOptions.get()))
        self.imgUp = imgRotate
        self.imgNumpy = np.array(imgRotate)
        self.imgCanvas = ImageTk.PhotoImage(imgRotate)
        self.canvas.create_image(300, 210, image=self.imgCanvas)
        self.canvas.image = self.imgCanvas

    def flip(self, event):
        if self.flipOptions.get() == "Y REFLECTION":
            imgFlip = self.imgUp.transpose(Image.FLIP_LEFT_RIGHT)
            self.imgNumpy = np.array(imgFlip)
            self.imgCanvas = ImageTk.PhotoImage(imgFlip)
            self.canvas.create_image(300, 210, image=self.imgCanvas)
            self.canvas.image = self.imgCanvas
        else:
            imgFlip = self.imgUp.transpose(Image.FLIP_TOP_BOTTOM)
            self.imgNumpy = np.array(imgFlip)
            self.imgCanvas = ImageTk.PhotoImage(imgFlip)
            self.canvas.create_image(300, 210, image=self.imgCanvas)
            self.canvas.image = self.imgCanvas

    def selectImage(self):
        self.img_path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.imgOrig = Image.open(self.img_path)
        self.imgUp = self.imgOrig
        self.imgNumpy = np.array(self.imgOrig)
        self.imgOrig.thumbnail((420, 420))
        self.imgCanvas = ImageTk.PhotoImage(self.imgOrig)
        self.canvas.create_image(300, 210, image=self.imgCanvas)
        self.canvas.image = self.imgCanvas
    
    # Função para realizar o espelhamento em relação ao eixo X 
    def reflexao(img):
        (l, c, p) = img.shape
        img_refl = np.zeros(shape=img.shape, dtype=np.uint8)
        for i in range(l):
            for j in range(c):
                new_x = j
                new_y = -i
                img_refl[new_y, new_x] = img[i, j]
                
        return img_refl

    def save(self):
        extension = self.img_path.split(".")[-1]
        file = asksaveasfilename(defaultextension=f".{extension}", filetypes=[("All Files", "*.*"), ("PNG file", "*.png"), ("jpg file", "*.jpg")])
        if file:
            self.imgUp.save(file)
        else:
            showinfo(title='Information', message='Not saved!')

    def exit(self):
        showinfo(title='Information', message='Bye!')
        self.destroy()
    
    