from tkinter import *
import random

#Enter game UI

def exit_program():
    window.destroy()

window = Tk()
window.title("Catch Candy")

canvas = Canvas(window, width = 800, height = 800, bg = 'black')
canvas.pack()

title = canvas.create_text(400, 400, text = 'Catch It If You Can', fill = 'white', font = ('Helvetica', 40))
directions = canvas.create_text(400, 500, text = 'Catch candys, except the red ones.', fill = 'white', font = ('Helvetica', 30))
start = canvas.create_text(400, 600, text = 'Press "Enter" to start', fill = 'white', font = ('Helvetica', 15))

score = 0
score_display = canvas.create_text(100, 50, text = 'Score : ' + str(score), fill = 'white', font = ('Helvetica', 20))

level = 1
level_display = canvas.create_text(700, 50, text = 'Level : ' + str(level), fill = 'white', font = ('Helvetica', 20))


player_image = PhotoImage(file = 'greenChar.gif')
mychar = canvas.create_image(400 ,700, image = player_image)

qbutton = Button(window, text = 'Quit', command = exit_program)
qbutton.pack()




# Create candy

candy_list = []
bad_candy_list = []
candy_speed = 2
candy_color_list = ['red', 'yellow', 'green', 'blue', 'pink', 'purple', 'white']
endgame = False

def make_candy():
    if endgame == False:
        xposition = random.randint(0, 800)
        candy_color = random.choice(candy_color_list)
        candy = canvas.create_oval(xposition, 0, xposition + 30, 30, fill = candy_color)
        candy_list.append(candy)
        if candy_color == 'red':
            bad_candy_list.append(candy)
        window.after(1000, make_candy)

def move_candy():
    for candy in candy_list:
        canvas.move(candy, 0, candy_speed)
        if canvas.coords(candy)[1] > 800:
            xposition = random.randint(0, 800)
            canvas.coords(candy, xposition, 0, xposition + 30, 30)
    window.after(50, move_candy)

#Update score and level

def update_score_level():
    global score, level, candy_speed
    score += 1
    canvas.itemconfig(score_display, text = 'Score : ' + str(score))

    if score % 10 == 0:
        level += 1
        candy_speed += 1
        canvas.itemconfig(level_display, text = 'Level : ' + str(level))
        
def end_game():
    window.destroy()

def end_title():
    canvas.delete(title)
    canvas.delete(directions)
    canvas.delete(start)

#Check if candy is caught

def collision(item1, item2, distance):
    xdistance = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    ydistance = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap =  xdistance < distance and ydistance < distance
    return overlap

def check_hits():
    global endgame
    for candy in bad_candy_list:
        if collision(mychar, candy, 30):
            for candy in candy_list:
                canvas.delete(candy)
            game_over = canvas.create_text(400, 400, text = 'Game Over', fill = 'red', font = ('Helvetica', 40))
            score_count = canvas.create_text(400, 500, text = 'Your score : ' + str(score), fill = 'white', font = ('Helvetica', 30))
            endgame = True
            window.after(2000, end_game)
            return
    for candy in candy_list:
        if collision(mychar, candy, 30):
            candy_list.remove(candy)
            canvas.delete(candy)
            update_score_level()
    window.after(100, check_hits)



#move character

move_direction = 0
def check_input(event):
    global move_direction
    if event.keysym == 'Left':
        move_direction = "Left"
    elif event.keysym == 'Right':
        move_direction = "Right"
    elif event.keysym == 'Up':
        move_direction = "Up"
    elif event.keysym == 'Down':
        move_direction = "Down"
    elif event.keysym == 'Escape':
        exit_program()
    elif event.keysym == 'Return':
        start_game()
    

def end_input(event):
    global move_direction
    move_direction = "None"

def move_character():
    if move_direction == "Left" and canvas.coords(mychar)[0] > 0:
        canvas.move(mychar, -10, 0)
    elif move_direction == "Right" and canvas.coords(mychar)[0] < 800:
        canvas.move(mychar, 10, 0)
    elif move_direction == "Up" and canvas.coords(mychar)[1] > 0:
        canvas.move(mychar, 0, -10)
    elif move_direction == "Down" and canvas.coords(mychar)[1] < 800:
        canvas.move(mychar, 0, 10)
    window.after(10, move_character)

canvas.bind_all('<KeyPress>', check_input)
canvas.bind_all('<KeyRelease>', end_input)

#Start game

def start_game():
    window.after(1000, end_title)
    window.after(1000, make_candy)
    window.after(1000, move_candy) 
    window.after(1000, check_hits)
    window.after(1000, move_character)


window.mainloop()