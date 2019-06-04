from tkinter import *
from PIL import ImageTk, Image





if __name__ == '__main__':
    window = Tk()
    window.title("Sogang Blockchat")
    window.configure(background="black")
    window.resizable(0,0)

    C = Canvas(window, bg='blue', height=500, width=800)
    # add an image
    bk_image = Image.open("tests/engineeringDep.jpg")
    width, height = bk_image.size
    width *= 3
    height *= 3
    bk_image = bk_image.resize((width, height), Image.ANTIALIAS)
    bk_image = ImageTk.PhotoImage(bk_image)
    bk_label = Label(window, image=bk_image)
    bk_label.place(x=0,y=0, relwidth=1, relheight=1)
    C.pack()

    window.mainloop()
