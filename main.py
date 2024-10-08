import random
from tkinter import *
import pandas as pd
import os

BACKGROUND_COLOR = "#b1ddc6"
current_word = {}

# ---------------------------- FILE SETUP ------------------------------- #
# Check if 'words_to_learn.csv' exists
if os.path.exists('words_to_learn.csv'):
    df = pd.read_csv('words_to_learn.csv')
else:
    df = pd.read_csv('de_to_en_words.csv')

# Convert the DataFrame to a list of dictionaries for easier manipulation
words_list = df.to_dict(orient="records")


# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global current_word, flip_timer
    # Cancel the previous flip timer if there's one running
    window.after_cancel(flip_timer)

    if words_list:  # Ensure there are words left in the list
        current_word = random.choice(words_list)
        german_word = current_word['GERMAN']

        # Show the German word on the front of the card
        canvas.itemconfig(card_image, image=card_front)
        canvas.itemconfig(language_label, text="German", fill="black")
        canvas.itemconfig(word_label, text=german_word, fill="black")

        # Set the card to flip after 3 seconds
        flip_timer = window.after(3000, flip_card)
    else:
        # If there are no more words left, display a message
        canvas.itemconfig(language_label, text="No more words!", fill="black")
        canvas.itemconfig(word_label, text="", fill="black")


def flip_card():
    english_word = current_word['ENGLISH']

    # Show the English word on the back of the card
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=english_word, fill="white")


def known_word():
    # Remove the current word from the words_list
    words_list.remove(current_word)

    # Update the words_to_learn.csv file with the remaining words
    pd.DataFrame(words_list).to_csv('words_to_learn.csv', index=False)

    # Show the next card
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("German to English")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# FRONT CARD
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
language_label = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_label = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# X BUTTON (Unknown button)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)

# ✔ BUTTON (Known button)
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=known_word)
right_button.grid(column=1, row=1)

# Set an initial flip timer variable
flip_timer = window.after(3000, flip_card)

# Start with the first card
next_card()

window.mainloop()
