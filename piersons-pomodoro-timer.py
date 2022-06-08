from tkinter import *
import tkinter.messagebox
import time
import math
import os


# For EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
WORK_REPS_TO_LONG_BREAK = 4
DETAILS_FLAG = False

start_time = time.time()

timer = None

reps = 0

# ---------------------------- TIMER RESET ------------------------------- # 
def resetTimer():
    global timer
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text = "00:00")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 

def startTimer():
    # Timer call
    global timer
    timer = update_time(start_time = time.time(), mode = "Work")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 



def update_time(start_time, mode):
    global reps
    global timer
    global DETAILS_FLAG

    # Update Periods
    periods = ''.join(["✔"] * (reps % WORK_REPS_TO_LONG_BREAK))
    period_count.config(text = periods)

    # Update Time
    minutes = 0
    seconds = 0
    if mode == "Work":
        mode_minutes =  WORK_MIN 
    elif mode == "Short Break":
        mode_minutes =  SHORT_BREAK_MIN 
    elif mode == "Long Break":
        mode_minutes =  LONG_BREAK_MIN
    minutes = mode_minutes - (math.trunc((time.time() - start_time) / 60) + 1)
    str_minutes = str(minutes).rjust(2, "0")
    seconds = round(start_time - time.time()) % 60
    str_seconds = str(seconds).rjust(2, "0")

    canvas.itemconfig(timer_text, text = f"{str_minutes}:{str_seconds}")

    # Show Details
    if DETAILS_FLAG:
        debug_text = (f"Pomodoro work minutes: {WORK_MIN} \n" 
        + f"Short Break Minutes: {SHORT_BREAK_MIN} \n"
        + f"Long Break Minutes: {LONG_BREAK_MIN} \n"
        + f"Pomodoros per Long Break: {WORK_REPS_TO_LONG_BREAK}\n"
        + f"Total Pomodoros completed: {reps}")
        details_text.config(text = debug_text)
    else:
        details_text.config(text = "")

    # Switch Modes

    if minutes >= 0 and seconds >= 0:
        timer = window.after(500, update_time, start_time, mode)
    else:
        if mode == "Work":
            reps += 1
        if mode == "Short Break" or mode == "Long Break":
            tkinter.messagebox.showinfo('Pomodoro','Start your work task now')
            timer = window.after(500, update_time, time.time(), "Work")
            current_mode.config(text = "Work", fg = GREEN)
        elif mode == "Work" and reps != 0 and reps % WORK_REPS_TO_LONG_BREAK == 0:
            tkinter.messagebox.showinfo('Pomodoro','Start your long break now')
            timer = window.after(500, update_time, time.time(), "Long Break")
            current_mode.config(text = "Long Break", fg = RED)
        else:
            tkinter.messagebox.showinfo('Pomodoro','Start your short break now')
            timer = window.after(500, update_time, time.time(), "Short Break")
            current_mode.config(text = "Short Break", fg = PINK)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.minsize(width = 400, height = 400)
window.title("Pomodoro")
window.config(padx=20, pady = 20, bg = YELLOW)

# Options Modal
def editSettings():

    def saveSettings(**kwargs):
        global WORK_MIN
        global SHORT_BREAK_MIN
        global LONG_BREAK_MIN
        global WORK_REPS_TO_LONG_BREAK
        global DETAILS_FLAG

        WORK_MIN = int(work_min_input.get())
        SHORT_BREAK_MIN = int(short_break_min_input.get())
        LONG_BREAK_MIN = int(long_break_min_input.get())
        WORK_REPS_TO_LONG_BREAK = int(work_reps_input.get())
        DETAILS_FLAG = bool(display_details_input.get())
        button["text"] = "Saved"
        configwin.destroy()

    configwin = Toplevel(window)

    work_min = Label(configwin, text="Pomodoro work minutes: ")
    work_min.grid(sticky = "w", row = 0, column = 0)
    work_min_input = Spinbox(configwin, from_=0, to = 120, width=5)
    work_min_input.delete(0, "end")
    work_min_input.insert(0, WORK_MIN)
    work_min_input.grid(row = 0, column = 1)

    short_break_min = Label(configwin, text="Short break minutes: ")
    short_break_min.grid(sticky = "w", row = 1, column = 0)
    short_break_min_input = Spinbox(configwin, from_=0, to = 120, width=5)
    short_break_min_input.delete(0, "end")
    short_break_min_input.insert(0, SHORT_BREAK_MIN)
    short_break_min_input.grid(row = 1, column = 1)

    long_break_min = Label(configwin, text="Long break minutes: ")
    long_break_min.grid(sticky = "w", row = 2, column = 0)
    long_break_min_input = Spinbox(configwin, from_=0, to = 120, width=5)
    long_break_min_input.delete(0, "end")
    long_break_min_input.insert(0, LONG_BREAK_MIN)
    long_break_min_input.grid(row = 2, column = 1)

    work_reps = Label(configwin, text="Pomodoros per long break: ")
    work_reps.grid(sticky = "w", row = 3, column = 0)
    work_reps_input = Spinbox(configwin, from_=0, to = 120, width=5)
    work_reps_input.delete(0, "end")
    work_reps_input.insert(0, WORK_REPS_TO_LONG_BREAK)
    work_reps_input.grid(row = 3, column = 1)

    display_details_input = BooleanVar(value=DETAILS_FLAG)
    display_details = Checkbutton(configwin, variable = display_details_input, onvalue = True, offvalue = False, text = "Display Additional Details")
    display_details.grid(sticky = "w", row = 4, column = 0)

    button = Button(configwin, text="Save Settings", command=saveSettings)
    button.grid(row = 5, column = 0)

# About Modal
def openAbout():
    aboutwin = Toplevel(window, width = 20, height = 100)
    title = Label(aboutwin, text = "Pierson's Pomodoro Timer")
    title.grid(row=0, column = 0)
    author = Label(aboutwin, text="Author: Pierson Wodarz")
    author.grid(sticky = "w", row = 1, column = 0)
    Label(aboutwin, text="A pomodoro timer with configurable intervals.").grid(sticky = "w", row = 2, column = 0)
    Label(aboutwin, text="Inspired by various examples and Dr. Angela Yu's 100 days of code.").grid(sticky = "w", row = 3, column = 0)


menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Options", command=editSettings)
filemenu.add_command(label="About", command=openAbout)
menubar.add_cascade(label="Settings", menu=filemenu)
window.config(menu=menubar)

# Header
title = Label(text = "Timer", font = (FONT_NAME, 40, "bold"), bg = YELLOW)
title.pack()

# Tomato Timer
canvas = Canvas(width = 200, height = 224, bg = YELLOW, highlightthickness = 0)
tomato = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image = tomato)
timer_text = canvas.create_text(100, 130, text = "00:00", fill = "white", font=(FONT_NAME, 35, "bold"))
canvas.pack()

# Start Button
start_button = Button(text="Start", command = startTimer, highlightthickness = 0)
start_button.pack(side = "left")

# Reset Button
reset_button = Button(text="Reset", command = resetTimer, highlightthickness = 0)
reset_button.pack(side = "right")

# Period Count
period_count = Label(text = "", font=(FONT_NAME, 20, "bold"), bg = YELLOW, fg = GREEN)
period_count.pack()

# Current Mode
current_mode = Label(text = "Work", font=(FONT_NAME, 20, "bold"), bg = YELLOW, fg = GREEN)
current_mode.pack()

# Details
details_text = Label(text = "", font=(FONT_NAME, 12, "italic"))
details_text.pack(side = "bottom")


window.mainloop()