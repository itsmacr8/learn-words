import os
import datetime as dt
from tkinter import *
import pandas

# <---------------------------- CONSTANTS and VARIABLES -------------------------------> #

FONT = ('Arial', 40, 'normal')
ALIGNMENT = 'center'
BLACK = 'black'
WHITE = 'white'
NUM_OF_WEEK = dt.datetime.now().weekday()
DIRPATH = os.path.dirname(__file__)

flip_time = 3000
current_word_index = 0
username = input('Enter your name: ').replace(' ', '').lower()


# <---------------------------- FUNCTIONS -------------------------------> #

def filepath(filename):
    """Returns the full path of a file."""
    filepath = os.path.join(DIRPATH, filename).replace('\\', '/')
    return filepath


def open_file(name):
    with open(name, encoding='UTF-8') as word_file:
        data = pandas.read_csv(word_file)
    return data


def next_words():
    """Shows the next word from the _english_words.csv or _words_to_learn.csv file. If user plays this application for the first time then he will see the words from _french_words.csv otherwise from the _words_to_learn.csv file."""
    global current_word, flip_word_timer
    # cancel the timer so that it does not call the flip_word function if user clicks on the wrong or right button continuously. When user stop clicking on the buttons then he will see the answer for that word.
    window.after_cancel(flip_word_timer)

    # To handle the error when user learns or visits all the words.
    try:
        current_word = total_words[current_word_index]
    except IndexError:
        """If user learns all the words then he will see the message that he has learned all the words."""
        fix_error()
        return
    english_word = current_word['English']
    canvas.itemconfig(canvas_image, image=white_img)
    canvas.itemconfig(title_text, fill=BLACK, text='English')
    canvas.itemconfig(word_text, fill=BLACK,  text=english_word)
    # set the flip_word_timer back to 3 seconds when user clicks on the wrong or right button.
    flip_word_timer = window.after(flip_time, flip_word)


def known_words():
    """If user knows the word and click on the right then this words will be removed from the _words_to_learn.csv file."""

    # To handle the error when user learns or visits all the words.
    try:
        total_words.remove(current_word)
    except ValueError:
        """If user learns all the words then he will see the message that he has learned all the words."""
        fix_error()
        return
    next_words()
    words_to_learn = pandas.DataFrame(total_words)
    words_to_learn.to_csv(user_learned_words, index=False)


def unknown_words():
    """If user does not know the word and click on the wrong button then Goto to the next word."""
    global current_word_index
    current_word_index += 1
    next_words()


def flip_word():
    """Change the background and text color when user sees the translated word."""
    bangali_word = current_word['Bangali']
    canvas.itemconfig(canvas_image, image=purple_img)
    canvas.itemconfig(title_text, fill=WHITE, text='Bangali')
    canvas.itemconfig(word_text,  fill=WHITE, text=bangali_word)


def fix_error():
    current_word['Bangali'] = 'শেষ হয়েছে। অভিনন্দন!'
    flip_word()


# <---------------------------- OPENING CSV FILE -------------------------------> #
user_learned_words = filepath(f'partials/_{username}.csv')
english_words = filepath('partials/_english_words.csv')

# If Today is Monday or Tuesday, User will revise the words.
if NUM_OF_WEEK == 0 or NUM_OF_WEEK == 3:
    words = open_file(english_words)
    flip_time = 1000
else:
    try:
        words = open_file(user_learned_words)
    except FileNotFoundError:
        """If user comes for the first time, he will not have any learned words. That's why his file is not exist yet.."""
        words = open_file(english_words)
    except pandas.errors.EmptyDataError:
        """If user file is empty then handle the error."""
        print('You have already learned all the words! You can start again from the beginning.')
        quit()

total_words = words.to_dict(orient='records')


# <---------------------------- UI SETUP -------------------------------> #

window = Tk()
window.title('Flashy card app')
window.config(padx=50, pady=50, bg='#B1DDC6')

# Call the flip_word function after 3 seconds
flip_word_timer = window.after(flip_time, flip_word)

canvas = Canvas(width=600, height=400, highlightthickness=0)
white_image = filepath('partials/images/white.png')
white_img = PhotoImage(file=white_image)
purple_image = filepath('partials/images/purple.png')
purple_img = PhotoImage(file=purple_image)
canvas_image = canvas.create_image(300, 200)
title_text = canvas.create_text(300, 130, font=FONT)
word_text = canvas.create_text(300, 230, font=FONT)
canvas.grid(row=0, column=0, columnspan=2, pady=20)

wrong_image = filepath('partials/images/wrong.png')
wrong_button_image = PhotoImage(file=wrong_image)
wrong_button = Button(image=wrong_button_image, command=unknown_words)
wrong_button.grid(row=1, column=0)

right_image = filepath('partials/images/right.png')
right_button_image = PhotoImage(file=right_image)
right_button = Button(image=right_button_image, command=known_words)
right_button.grid(row=1, column=1)


next_words()
window.mainloop()
