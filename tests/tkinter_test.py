from tkinter import *
from PIL import ImageTk, Image

# key down function
def click():
    entered_text = textentry.get()
    output.delete(0.0, END)
    try:
        definition = my_compdictionary[entered_text]
    except:
        definition = "sorry that word is not in the dictionary"
    output.insert(END, definition)

# exit function
def close_window():
    window.destroy()
    exit()

# main
window = Tk()
window.title("Testing tkinter!!")
window.configure(background="black")
window.resizable(0,0)

# add an image
photo1 = ImageTk.PhotoImage(Image.open("engineeringDep.jpg"))
Label(window, image=photo1, bg="black").grid(row=0, column=0, sticky=E)

# create a label
Label(window, text="Enter the word you would like a definition for:", bg='black', fg='white', font='none 12 bold').grid(row=1, column=0, sticky=W)

# text entry box
textentry = Entry(window, width=20, bg='white')
textentry.grid(row=2, column=0, sticky=W)

# submit button
Button(window, text='SUBMIT', width=6, command=click, highlightbackground='black').grid(row=3, column=0, sticky=W)

# label to display def
Label(window, text='\nDefinitition:', bg='black', fg='white', font='none 12 bold').grid(row=4, column=0, sticky=W)

# create text box
output = Text(window, width=75, height=6, wrap=WORD, background='white')
output.grid(row=5, column=0, sticky=W, columnspan=2)

# dictionary
my_compdictionary = {
    'algorithm': 'bla bla bla algorithm bla bla bla', 'bug': 'something you should stomp on'
    }

# exit button
Button(window, text='EXIT', highlightbackground='black', font='none 12 bold', command=close_window).grid(row=6, column=0, sticky=W)

# run main loop
window.mainloop()
