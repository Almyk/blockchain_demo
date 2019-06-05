from tkinter import *
from PIL import ImageTk, Image


if __name__ == '__main__':
    window = Tk()
    window.title("Sogang Blockcoin")
    window.configure(background="black")
    window.resizable(0,0)


    # get background image
    bk_image = Image.open("sogang.jpg")
    width, height = bk_image.size
    width *= 2
    height *= 2

    # create canvas
    # C = Canvas(window, height=height, width=width)
    # C.pack()
    canvas = Canvas(window, width=width, height=height)
    canvas.pack()

    # add background image
    bk_image = bk_image.resize((width, height), Image.ANTIALIAS)
    bk_image = ImageTk.PhotoImage(bk_image)
    canvas.create_image(width/2,height/2, image=bk_image)


    # test = Label(window, text='test 2', fg='black', bg="#33B5E5", anchor=W,
    #              width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    # canvas.create_window(10,200, anchor=NW, window=test)

    # add quit button
    quit_button = Button(window, text="Quit", command=window.quit, anchor=W,
                         width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 10, anchor=NW, window=quit_button)

    # generate key button
    gen_key_btn = Button(window, text="Generate Key", command=window.quit, anchor=W,
                         width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 100, anchor=NW, window=gen_key_btn)

    # load key button
    load_key_btn = Button(window, text="Load Key", command=window.quit, anchor=W,
                          width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 140, anchor=NW, window=load_key_btn)

    # make transaction button
    transaction_btn = Button(window, text="Transaction", command=window.quit, anchor=W,
                             width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 180, anchor=NW, window=transaction_btn)

    # Start Mining button
    start_mining_btn = Button(window, text="Start Mining", command=window.quit, anchor=W,
                             width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 220, anchor=NW, window=start_mining_btn)

    # Stop Mining button
    stop_mining_btn = Button(window, text="Stop Mining", command=window.quit, anchor=W,
                             width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 260, anchor=NW, window=stop_mining_btn)

    # Block History button
    history_btn = Button(window, text="Block History", command=window.quit, anchor=W,
                             width=10, activebackground="#33B5E5", highlightbackground="#33B5E5")
    canvas.create_window(10, 300, anchor=NW, window=history_btn)

    curr_trans_label = Label(window, text="Current Transactions:", anchor=W,
                             fg='black', bg='#33B5E5')
    canvas.create_window(10, 340, anchor=NW, window=curr_trans_label)


    window.mainloop()
