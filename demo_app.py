from tkinter import *
from PIL import ImageTk, Image

def generate_key():
    pass

def load_key():
    pass

def make_transaction():
    pass

def start_mining():
    pass

def stop_mining():
    pass

def view_history():
    pass

if __name__ == '__main__':
    root = Tk()
    root.title("Sogang Blockcoin")
    root.configure(background="black")
    root.resizable(0, 0)


    # get background image
    bk_image = Image.open("sogang.jpg")
    width, height = bk_image.size
    width *= 2
    height *= 2

    # create canvas
    # C = Canvas(window, height=height, width=width)
    # C.pack()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()

    # add background image
    bk_image = bk_image.resize((width, height), Image.ANTIALIAS)
    bk_image = ImageTk.PhotoImage(bk_image)
    canvas.create_image(width/2,height/2, image=bk_image)

    # add quit button
    quit_button = Button(root, text="Quit", command=root.quit, anchor=W, fg='white',
                         width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, 10, anchor=NW, window=quit_button)

    temp_y = 160
    rel_y = 40
    # generate key button
    gen_key_btn = Button(root, text="Generate Key", command=generate_key, anchor=W, fg='white',
                         width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, temp_y, anchor=NW, window=gen_key_btn)

    # load key button
    load_key_btn = Button(root, text="Load Key", command=load_key, anchor=W, fg='white',
                          width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, temp_y + rel_y, anchor=NW, window=load_key_btn)

    # make transaction button
    transaction_btn = Button(root, text="Transaction", command=make_transaction, anchor=W, fg='white',
                             width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, temp_y + 2*rel_y, anchor=NW, window=transaction_btn)

    # Start Mining button
    start_mining_btn = Button(root, text="Start Mining", command=start_mining, anchor=W, fg='white',
                              width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, temp_y + 3*rel_y, anchor=NW, window=start_mining_btn)

    # Stop Mining button
    stop_mining_btn = Button(root, text="Stop Mining", command=stop_mining, anchor=W, fg='white',
                             width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, temp_y + 4*rel_y, anchor=NW, window=stop_mining_btn)

    # Block History button
    history_btn = Button(root, text="Block History", command=view_history, anchor=W, fg='white',
                         width=10, activebackground="#33B5E5", highlightbackground="#666")
    canvas.create_window(10, temp_y + 5*rel_y, anchor=NW, window=history_btn)


    # Display current transactions
    temp_y = 480
    rel_y = 26
    curr_trans_box = Text(root, width=75, height=10, wrap=WORD, font='none 14 bold',
                          background='gray', highlightbackground="#777")
    canvas.create_window(40, temp_y+rel_y, anchor=NW, window=curr_trans_box)
    curr_trans_box.bindtags((str(curr_trans_box), str(root), "all"))

    curr_trans_label = Label(root, text="Current Transactions:", anchor=W,
                             fg='black', bg='#666', font='none 16 bold')
    canvas.create_window(10, temp_y, anchor=NW, window=curr_trans_label)

    text = """1.
2.
3.
4.
5.
6.
7.
8.
9.
10."""
    curr_trans_num = Label(root, width=3, height=10, font='none 14 bold',
                           background='#777', highlightbackground="#777", text=text)
    canvas.create_window(10, temp_y + rel_y, anchor=NW, window=curr_trans_num)
    ###

    root.mainloop()
