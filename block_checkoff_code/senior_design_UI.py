from tkinter import *

def func_1():
	button_1.config(bg='red')
#

def func_2():
	button_1.config(bg='green')
#

def func_3():
	button_1.config(bg='blue')
#

def fullscreen_on():
	root.attributes("-fullscreen", True)
#

def fullscreen_off():
	root.attributes("-fullscreen", False)
#

		
root = Tk()
root.title("Electronic Chess")
root.attributes("-fullscreen", False)

frame_1 = Frame(root, highlightbackground="green", highlightthickness=1)
frame_1.pack(fill=X)

button_1 = Button(frame_1, text="Start new game", command=func_1)
button_1.pack()
button_2 = Button(frame_1, text="Save a game", command=func_2)
button_2.pack()
#setting_icon = PhotoImage(file="setting_icon.png")
#setting_icon = setting_icon.subsample(20)
#button_3 = Button(frame_1, image=setting_icon, command=func_3)
#button_3.pack()
button_4 = Button(frame_1, text="fullscreen", command=fullscreen_on)
button_4.pack()
button_5 = Button(frame_1, text="not fullscreen", command=fullscreen_off)
button_5.pack()

v = StringVar()
entry_1 = Entry(root, textvariable=v)
entry_1.pack()

label_1 = Label(root, text="Text")
label_1.pack()

widthpixels=300
heightpixels=100
root.minsize(widthpixels, heightpixels)
root.resizable(width=True, height=True)
root.mainloop()
