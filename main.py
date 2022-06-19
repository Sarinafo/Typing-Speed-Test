from tkinter import *
import math
import csv
import random

PINK = '#F4BFBF'
ORANGE = '#FFD9C0'
YELLOW = '#FAF0D7'
BLUE = '#8CC0DE'
FONT_NAME = "Courier"
words_data = []
displayed_words = []
user_words = []
display = ''
wpm_count = 0
cpm_count = 0
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed Test Application")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)


page1 = Frame(window)
page2 = Frame(window)


for frame in (page1, page2):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(page1)

def user_type(event):
    user_words.append(entry_box.get().title().strip().lower())
    entry_box.delete(0, "end")
    if len(user_words) % 10 == 0:
        random_words()
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_text.config(text=f"{count_min}:{count_sec}")
    if count != 0:
        window.after(1000, count_down, count - 1)
    if count == 0:
        compare()


def start_timer():
    count_down(60)


# ---------------------------- GET WORDS ------------------------------- #
with open('words.csv') as file:
    data = csv.reader(file)
    for row in data:
        words_data.append(''.join(row))

def random_words():
    global display
    display = ""
    for i in range(10):
        display_word = random.choice(words_data)
        displayed_words.append(display_word)
        display += (display_word + ' ')
    canvas.itemconfig(word_show, text=display)

# ---------------------------- TIMER RESET ------------------------------- #

def restart():
    global displayed_words, user_words, wpm_count, cpm_count
    displayed_words = []
    user_words = []
    wpm_count = 0
    cpm_count = 0
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    entry_box.config(state="normal")
    start_timer()
    random_words()

# ---------------------------- START APPLICATION ------------------------------- #

def start():
    global displayed_words, user_words, wpm_count, cpm_count
    displayed_words = []
    user_words = []
    wpm_count = 0
    cpm_count = 0
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    entry_box.config(state="normal")
    start_timer()
    random_words()


def compare():
    # count WPM
    global wpm_count, cpm_count
    entry_box.config(state="disabled")
    for i in user_words:
        if i in displayed_words:
            wpm_count += 1
            cpm_count += len(i)
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    print(f"user_type: {user_words}")
    print(f"display_words: {displayed_words}")


# ---------------------------- FIRST PAGE ------------------------------- #


page1.config(padx=50, pady=50, bg=ORANGE)
# Title
title_label = Label(page1, text='Typing Speed Test', bg=ORANGE, font=(FONT_NAME, 35, 'bold'))
title_label.grid(column=2, row=0)

# select level
select_label = Label(page1, text='Select the begin button to start the game', bg=ORANGE, font=(FONT_NAME, 15, 'italic'))
select_label.grid(column=2, row=1, padx=20, pady=20)

easy_button = Button(page1, text='BEGIN', highlightbackground=ORANGE, command=lambda: show_frame(page2))
easy_button.grid(column=2, row=2)

# ---------------------------- SECOND PAGE ------------------------------- #
page2.config(padx=50, pady=50, bg=YELLOW)

timer_text = Label(page2, text="00:00", bg=YELLOW, fg=PINK, font=(FONT_NAME, 35, "bold"))
timer_text.grid(column=2, row=0)

cpm_label = Label(page2, text="Corrected CPM: ", font=("Arial", 12), bg=YELLOW)
cpm_label.grid(column=2, row=1)
cpm_value = Label(page2, text="?", font=("Arial", 12), bg=YELLOW)
cpm_value.grid(column=3, row=1)

wpm_label = Label(page2, text="WPM: ", font=("Arial", 12), bg=YELLOW)
wpm_label.grid(column=4, row=1)
wpm_value = Label(page2, text="?", font=("Arial", 12), bg=YELLOW)
wpm_value.grid(column=5, row=1)


canvas = Canvas(page2, width=350, height=263, bg=YELLOW, highlightthickness=0)
pink_card = PhotoImage(file="new_card.png")
refresh = PhotoImage(file="refresh.png")
canvas.create_image(175, 131, image=pink_card)
word_show = canvas.create_text(160, 132, text="Press the start button\nto begin.\nPress the space button after each word.\nCapitalization doesn't matter", font=("Courier", 14, "bold"), fill=BLUE, justify="center", width=250)

canvas.grid(column=2, row=2, columnspan=6)

entry_box = Entry(page2, bd=0, font=("Arial", 12), justify="center", width=30)
entry_box.focus()
entry_box.grid(row=3, column=1, columnspan=6)
entry_box.bind("<space>", user_type)


start_button = Button(page2, text='START', highlightbackground=YELLOW, command=start)
start_button.grid(column=3, row=4)

refresh_button = Button(page2, image=refresh, highlightbackground=YELLOW, command=restart)
refresh_button.grid(column=3, row=5)




window.mainloop()