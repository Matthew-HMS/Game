#Todo: combo bonus, various map, highest combo, grade review(ABCD)

from os import remove
from tkinter import *
import random

#Enter game UI test

window = Tk()
window.title("Osu!")
window.config(cursor= 'none')

canvas = Canvas(window, width = 1600, height = 800, bg = 'black')
canvas.pack()

#title
title = canvas.create_text(750, 400, text = 'Osu!', fill = 'white', font = ('Helvetica', 50))
direction = canvas.create_text(750, 500, text = 'Press Enter to start, Esc to exit', fill = 'white', font = ('Helvetica', 20))

# personal record
def sort_rank():
    global score_list
    file = open("OsuRank.txt", "a")
    file = open("OsuRank.txt", "r")
    if file.mode == 'r':
        contents = file.read()
        score_list = contents.split("\n")
        for i in score_list:
            if i == '':
                score_list.remove(i)
        score_list = list(map(int, score_list))
        score_list.sort(reverse = True)

rank_display = ''
def rank_list():
    global rank_display, score_list
    count = 1
    for i in score_list[:10]:
        if i == '':
            continue
        else:
            rank_display += (str(count) + ".  " + str(i) + "\n")
            count += 1

sort_rank()
rank_list()
record = canvas.create_text(150, 400, text = 'Personal Record : \n\n' + rank_display , fill = 'white', font = ('Helvetica', 20))

#delete start UI
def end_title():
    canvas.delete(title)
    canvas.delete(direction)
    canvas.delete(record)

correct_circle = 0
total_circle = 0
score = 0
score_display = canvas.create_text(100, 50, text = 'Score : ' + str(score), fill = 'white', font = ('Helvetica', 20))
combo = 0
hp = 10
hp_title = canvas.create_text(350, 50, text = 'HP : ', fill = 'white', font = ('Helvetica', 20))

hp_display = canvas.create_rectangle(400, 50, 700, 70, fill = 'white')

def update_hp():
    global hp_display,hp
    canvas.delete(hp_display)
    hp_result = hp*30 + 400
    hp_display = canvas.create_rectangle( 400, 50, hp_result, 70, fill = 'white')


# move ball

image = PhotoImage(file = 'ball.gif')
ball = canvas.create_image(400, 400, anchor=NW, image=image)

def move(e):
   global image,ball
   image = PhotoImage(file = 'ball.gif')
   ball = canvas.create_image(e.x, e.y, image=image)

canvas.bind("<Motion>", move)

#Create circle
endgame = False

circle_list = []
def make_circle():
    global circle_list, total_circle
    if endgame == False:
        xposition = random.randint(100, 1400)
        yposition = random.randint(100, 700)
        circle = canvas.create_oval(xposition, yposition, xposition + 100, yposition + 100, outline = 'white', width = 5)
        circle_list.append(circle)
        total_circle += 1
        window.after(750, del_circle)
        window.after(750, make_circle)

# delete circle    
def del_circle():
    global combo,hp
    if endgame == False:
        for circle in circle_list:
            if correct == False:
                wrong_notice(canvas.coords(circle)[0]+100, canvas.coords(circle)[1]+100)
                combo = 0
                canvas.itemconfig(combo_display, text = '')
                if hp >= 1:
                    hp -= 1
                else: 
                    hp = 0
                if hp <= 0:
                    game_over()
                update_hp()
            canvas.delete(circle)
            circle_list.remove(circle)
            break


# read input
press = False
def check_input(event):
    global press
    if event.keysym == 'z' or event.keysym == 'x':
        press = True
    elif event.keysym == 'Escape':
        window.destroy()
    elif event.keysym == 'Return':
        start_game()


#check if the mouse is in the circle
def end_input(event):
    global press
    press = False
    
def contact(item1, item2, distance):
    global press
    xdistance = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    ydistance = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap =  xdistance < distance and ydistance < distance and press == True
    return overlap

#score
def update_score():
    global score
    score += 1
    canvas.itemconfig(score_display, text = 'Score : ' + str(score))

#notice 
def correct_notice(x,y):
    global notice_display
    notice_display = canvas.create_text(x, y, text = 'O', fill = 'green', font = ('Helvetica', 30))
    window.after(500, end_notice)

def wrong_notice(x,y):
    global wrong_notice_display
    wrong_notice_display = canvas.create_text(x, y, text = 'X', fill = 'red', font = ('Helvetica', 30))
    window.after(500, end_wrong_notice)

def end_notice():
    canvas.delete(notice_display)

def end_wrong_notice():
    canvas.delete(wrong_notice_display)

combo_display = canvas.create_text(150, 700, text = '', fill = 'white', font = ('Helvetica', 30))
def combo_notice():
    global combo, combo_display
    canvas.itemconfig(combo_display, text = str(combo) + ' Combo !')


#check contact
correct = False
def check_hits():
    global correct, combo, hp, correct_circle
    for circle in circle_list:
        if contact(ball, circle, 100):
            correct == True
            correct_circle += 1
            correct_notice(canvas.coords(circle)[0]+100, canvas.coords(circle)[1]+100)
            canvas.delete(circle)
            circle_list.remove(circle)
            update_score()
            if hp < 10:
                hp += 0.5
                update_hp()
            combo += 1
            combo_notice()
            break
    correct == False
    window.after(100, check_hits)
    
canvas.bind_all('<KeyPress>', check_input)
canvas.bind_all('<KeyRelease>', end_input)


def start_game():
    end_title()
    window.after(1000, make_circle)
    window.after(1000, check_hits)

# record score
max_score = 0
def write_record():
    global max_score,score
    file = open("OsuRank.txt", "a")
    file.write(str(score) + "\n")
    file = open("OsuRank.txt", "r")
    if file.mode == 'r':
        contents = file.read()
        score_list = contents.split("\n")
        for i in score_list:
            if i == '':
                continue
            elif int(i) > max_score:
                max_score = int(i)
    file.close()



def game_over():
    global endgame, game_over_note, percent_note, key_note, highest_record
    endgame = True
    correct_pecentage = (correct_circle / total_circle * 100)
    write_record()
    game_over_note = canvas.create_text(750, 300, text = 'Game Over', fill = 'red', font = ('Helvetica', 50))
    percent_note = canvas.create_text(750, 400, text = 'Correct pecentage : ' + str(round(correct_pecentage,2)) + ' %', fill = 'white', font = ('Helvetica', 20))
    highest_record = canvas.create_text(750, 500, text = 'Highest score : ' + str(max_score), fill = 'white', font = ('Helvetica', 20))
    key_note = canvas.create_text(750, 600, text = 'Press "Esc" to exit, "Enter" to restart', fill = 'white', font = ('Helvetica', 20))
    canvas.bind_all('<KeyPress>', restart)


def restart(event):
    global title, direction, correct_circle, total_circle, score, score_display, combo, hp, hp_title, hp_display, endgame, combo_display, circle_list, record, rank_display
    if event.keysym == 'Return':
        canvas.delete(game_over_note)
        canvas.delete(percent_note)
        canvas.delete(key_note)
        canvas.delete(score_display)
        canvas.delete(highest_record)

        title = canvas.create_text(800, 400, text = 'Osu!', fill = 'white', font = ('Helvetica', 50))
        direction = canvas.create_text(800, 500, text = 'Press Enter to start', fill = 'white', font = ('Helvetica', 20))
        rank_display = ''
        sort_rank()
        rank_list()
        record = canvas.create_text(150, 400, text = 'Personal Record : \n\n' + rank_display , fill = 'white', font = ('Helvetica', 20))
        correct_circle = 0
        total_circle = 0
        score = 0
        score_display = canvas.create_text(100, 50, text = 'Score : ' + str(score), fill = 'white', font = ('Helvetica', 20))
        combo = 0
        hp = 10
        hp_title = canvas.create_text(350, 50, text = 'HP : ', fill = 'white', font = ('Helvetica', 20))

        hp_display = canvas.create_rectangle(400, 50, 700, 70, fill = 'white')
        endgame = False
        combo_display = canvas.create_text(150, 700, text = '', fill = 'white', font = ('Helvetica', 30))
        circle_list = []

        canvas.bind_all('<KeyPress>', check_input)
        canvas.bind_all('<KeyRelease>', end_input)

    elif event.keysym == 'Escape':
        window.destroy()




window.mainloop()