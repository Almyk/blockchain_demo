import Blockchain
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import random

def quit_app():
    node.stop()
    node.join()
    root.quit()


def generate_key():
    # TODO: use the blockchain class' key generation function
    key = node.gen_keys()
    messagebox.showinfo("New Key Generated", "A new key has been generated and loaded into the client\n\n'" + key + "'")
    pass


def load_key():
    # TODO: popup that asks for your key
    messagebox.showinfo("Load Key", "To be implemented ;) ")
    pass


def make_transaction():
    # TODO: popup where you set receiver, using public key, and determine amount to send
    pass


def start_mining():
    # TODO: tell the node to start mining process
    messagebox.showinfo("Mining", "Started Mining\n\nIf you succeed in generating a block you will earn coins")
    pass


def stop_mining():
    # TODO: tell the node to stop mining
    messagebox.showinfo("Mining", "Stopped Mining")
    pass


def view_history():
    # TODO: popup that shows the block history, scrollable window
    pass


def eventCallback(event, server, node, data=None):
    if event == "NODE_CONNECTED":
        # TODO update user count
        pass
    elif event == "update_transaction_pool":
        # TODO update transaction pool
        print("update transaction pool")
        update_transaction_pool()

        pass
    elif event == "update_miner_count":
        # TODO update miner count
        pass


def update_transaction_pool():
    curr_trans_box.delete(0.0, END)
    trans_str = ""
    for transaction in node.transaction_pool:
        trans_str += transaction + '\n'

    curr_trans_box.insert(END, trans_str)


def update_all():
    update_transaction_pool()
    update_miner()
    update_user()
    update_blocks()


def update_miner():
    miner_count.delete(0.0, END)
    node.ask_for_mine_count()
    count = str(node.miner_count)
    miner_count.insert(END, count)


def update_user():
    user_count.delete(0.0, END)
    count = str(node.get_unique_node_count())
    user_count.insert(END, count)

def update_blocks():
    block_box.delete(0.0, END)
    chain = node.blockchain.chain
    block_str = ""
    for block in chain:
        stamp = str(block.time_stamp)
        try:
            stamp = time.ctime(block.time_stamp)
        except Exception as e:
            print(e)
        block_str += stamp + ':\n ' + str(block.transaction_list) +'\n-----\n'
    block_box.insert(END, block_str)


root = Tk()
root.title("Sogang HalalChain")
root.configure(background="black")
root.resizable(0, 0)


# get background image
bk_image = Image.open("sogang.jpg")
width, height = bk_image.size
width *= 2
height *= 2

# create canvas
canvas = Canvas(root, width=width, height=height)
canvas.pack()

# add background image
bk_image = bk_image.resize((width, height), Image.ANTIALIAS)
bk_image = ImageTk.PhotoImage(bk_image)
canvas.create_image(width/2,height/2, image=bk_image)

# add quit button
quit_button = Button(root, text="Quit", command=quit_app, anchor=W, fg='white',
                     width=10, activebackground="#33B5E5", highlightbackground="#666")
canvas.create_window(10, 10, anchor=NW, window=quit_button)

temp_y = 160
rel_y = 40
# generate key button
gen_key_btn = Button(root, text="Generate Key", command=generate_key, anchor=W, fg='white',
                     width=10, activebackground="#33B5E5", highlightbackground="#666")
canvas.create_window(10, temp_y, anchor=NW, window=gen_key_btn)

# # load key button
# load_key_btn = Button(root, text="Load Key", command=load_key, anchor=W, fg='white',
#                       width=10, activebackground="#33B5E5", highlightbackground="#666")
# canvas.create_window(10, temp_y + rel_y, anchor=NW, window=load_key_btn)

# load key button
update_btn = Button(root, text="Update Info", command=update_all, anchor=W, fg='white',
                      width=10, activebackground="#33B5E5", highlightbackground="#666")
canvas.create_window(10, temp_y + rel_y, anchor=NW, window=update_btn)

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
                      background='gray', highlightbackground="#666")
canvas.create_window(40, temp_y+rel_y, anchor=NW, window=curr_trans_box)
curr_trans_box.bindtags((str(curr_trans_box), str(root), "all"))

curr_trans_label = Label(root, text="Current Transactions:", anchor=W,
                         fg='black', bg='#666', font='none 16 bold')
canvas.create_window(10, temp_y, anchor=NW, window=curr_trans_label)

# trans_str = ""
# for transaction in node.transaction_pool:
#     trans_str += transaction + '\n'

# curr_trans_box.insert(END, trans_str)

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
                       background='#666', highlightbackground="#666", text=text)
canvas.create_window(10, temp_y + rel_y, anchor=NW, window=curr_trans_num)
### End of display current transactions ###

# create blockchain node
port = random.randint(1111,9999)
host = 'localhost'
node = Blockchain.BlockchainNode(host, port, eventCallback)
node.start()
node.join_network(host, 888)
print(node.transaction_pool)

update_transaction_pool()

# Display blocks
temp_x = width
label_x = width/2 + width/4 + 58
temp_y = 230
rel_y = 26

block_box = Text(root, width=40, wrap=WORD, font='none 14 bold',
                      background='gray', highlightbackground="#666")
canvas.create_window(temp_x, temp_y+rel_y, anchor=NE, window=block_box)
block_box.bindtags((str(block_box), str(root), "all"))

block_label = Label(root, text="My Blocks:", anchor=W,
                         fg='black', bg='#666', font='none 16 bold')
canvas.create_window(label_x, temp_y, anchor=NE, window=block_label)
### END of display blocks ###

# display users in network
temp_x = label_x + width/16

user_count = Text(root, width=10, height=1, wrap=WORD, font='none 14 bold',
                  background='gray', highlightbackground="#666")
canvas.create_window(temp_x, 10, anchor=NW, window=user_count)
user_count.bindtags((str(user_count), str(root), "all"))

user_label = Label(root, text="Users:", anchor=W,
                         fg='black', bg='#666', font='none 16 bold')
canvas.create_window(temp_x, 10, anchor=NE, window=user_label)
count = str(node.get_unique_node_count())
user_count.insert(END, count)
### END of display users ###

# display miners in network
temp_x = label_x + width/16
rel_y = 40

miner_count = Text(root, width=10, height=1, wrap=WORD, font='none 14 bold',
                  background='gray', highlightbackground="#666")
canvas.create_window(temp_x, 10+rel_y, anchor=NW, window=miner_count)
miner_count.bindtags((str(user_count), str(root), "all"))

miner_label = Label(root, text="Miners:", anchor=W,
                         fg='black', bg='#666', font='none 16 bold')
canvas.create_window(temp_x, 10+rel_y, anchor=NE, window=miner_label)
count = str(node.miner_count)
miner_count.insert(END, count)
### END of display users ###

update_all()
root.mainloop()

