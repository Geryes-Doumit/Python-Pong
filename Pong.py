import tkinter as tk
import random
import math
import time

Play = False
Restart = False
A, B = 0, 0  # Score
ScoreReset = False
width = 1200
height = 650
Latency = 30
Speed = 10
SpeedLimit = 50
directions = [-math.pi / 4, math.pi / 4, 3 * math.pi / 4, -3 * math.pi / 4]
direction = random.choice(directions)
Y_Speed = -Speed * math.sin(direction)
X_Speed = Speed * math.cos(direction)
TimeL = 0
TimeR = 0
HitTime = 0
UpDownMovel = 0
UpDownMoveR = 0


def PlayPause():
    global Play
    if Play:
        Play = False
    else:
        Play = True
        window.after(0, moving)


def playpause(event):
    global Play
    if Play:
        Play = False
    else:
        Play = True
        window.after(0, moving)


def restart():
    global Restart, ScoreReset
    if not Restart:
        Restart = True
        ScoreReset = True


def reset_canvas():
    global Restart, ScoreReset, A, B
    global direction, Y_Speed, X_Speed
    global canvas, line, ball, leftRect, rightRect, Score
    global Play
    if Restart:
        if ScoreReset:
            A, B = 0, 0
        canvas.delete('all')
        line = canvas.create_line(width // 2, 40, width // 2, height, dash=(50, 50), fill="white")
        ball = canvas.create_oval(0.5 * width - 15, 0.5 * height - 15, 0.5 * width + 15, 0.5 * height + 15,
                                  fill='#f75a4f')
        leftRect = canvas.create_rectangle(5, 0.5 * height - 100, 20, 0.5 * height + 100, fill="white")
        rightRect = canvas.create_rectangle(width - 5, 0.5 * height - 100, width - 20, 0.5 * height + 100,
                                            fill="white")
        Score = canvas.create_text(width // 2, 20, fill="white", font=("Arial", "20"), text="0 - 0")
        canvas.pack()
        direction = random.choice(directions)
        Y_Speed = -Speed * math.sin(direction)
        X_Speed = Speed * math.cos(direction)
        Restart = False
        ScoreReset = False
        Play = False
        window.after(0, moving)


def rUp(event):
    global TimeR, UpDownMoveR
    TimeR = time.time()
    # print("Right Move at:" + str(TimeR))
    UpDownMoveR = 1
    x1r, y1r, x2r, y2r = canvas.coords(rightRect)
    if y1r - 10 > 0:
        canvas.move(rightRect, 0, -30)


def rDown(event):
    global TimeR, UpDownMoveR
    TimeR = time.time()
    # print("Right Move at:" + str(TimeR))
    UpDownMoveR = -1
    global height
    x1r, y1r, x2r, y2r = canvas.coords(rightRect)
    if y2r + 10 < height:
        canvas.move(rightRect, 0, 30)


def lUp(event):
    global TimeL, UpDownMovel
    UpDownMovel = 1
    TimeL = time.time()
    # print("Left Move at:" + str(TimeL))
    x1l, y1l, x2l, y2l = canvas.coords(leftRect)
    if y1l - 10 > 0:
        canvas.move(leftRect, 0, -30)


def lDown(event):
    global TimeL, UpDownMovel
    TimeL = time.time()
    # print("Left Move at:" + str(TimeL))
    UpDownMovel = -1
    global height
    x1l, y1l, x2l, y2l = canvas.coords(leftRect)
    if y2l + 10 < height:
        canvas.move(leftRect, 0, 30)


def UpDown_collision():
    global height
    global Y_Speed
    global width
    global ball

    x1, y1, x2, y2 = canvas.coords(ball)

    if y1 + Y_Speed < 0 or y2 + Y_Speed > height:
        Y_Speed *= -1


def LeftRight_collisions():
    global width
    global X_Speed, Y_Speed
    global width, HitTime
    global ball, leftRect, rightRect

    x1, y1, x2, y2 = canvas.coords(ball)
    x1l, y1l, x2l, y2l = canvas.coords(leftRect)
    x1r, y1r, x2r, y2r = canvas.coords(rightRect)

    test = X_Speed, Y_Speed

    if x1 + X_Speed < x2l and y1l < y2 + Y_Speed < y2l:
        HitTime = time.time()
        SpecialMovesL()
        if abs(X_Speed) < SpeedLimit:
            X_Speed *= -1.1
        else:
            X_Speed *= -1
        '''if random.randint(1, 10) == 5:
            SpeedSquared = X_Speed ** 2 + Y_Speed ** 2
            i = random.uniform(-math.pi/6, math.pi/6)
            X_Speed *= math.cos(i)
            Y_Speed *= math.sqrt(SpeedSquared - X_Speed ** 2)'''
        # print(X_Speed / test[0], Y_Speed / test[1])

    elif x1 + X_Speed > x2r - 45 and y1r < y2 + Y_Speed < y2r:
        HitTime = time.time()
        SpecialMovesR()
        if abs(X_Speed) < SpeedLimit:
            X_Speed *= -1.1
        else:
            X_Speed *= -1
        '''if random.randint(1, 10) == 5:
            SpeedSquared = X_Speed**2 + Y_Speed**2
            i = -random.uniform(-math.pi/6, math.pi/6)
            X_Speed *= math.cos(i)
            Y_Speed *= math.sqrt(SpeedSquared - X_Speed**2)'''

        # print(X_Speed / test[0], Y_Speed / test[1])


def autoReset():
    global ball, Score, width, Restart, A, B

    x1, y1, x2, y2 = canvas.coords(ball)

    if x1 < -20:
        time.sleep(1)
        Restart = True
        reset_canvas()
        A += 1
        Score = canvas.itemconfig(Score, text=str(A) + " - " + str(B))
        canvas.delete(Score)
        canvas.pack()

    elif x2 > width + 20:
        time.sleep(1)
        Restart = True
        reset_canvas()
        B += 1
        Score = canvas.itemconfig(Score, text=str(A) + " - " + str(B))
        canvas.delete(Score)
        canvas.pack()


def SpecialMovesL():
    global Y_Speed, X_Speed
    # print("HitTime " + str(HitTime))
    # print("hit - TimeL "+str(HitTime - TimeL))
    if HitTime - TimeL < 0.1:
        if Y_Speed * UpDownMovel < 0:
            X_Speed *= 1.1
        elif Y_Speed * UpDownMovel > 0:
            if random.randint(1, 5) == 3:
                X_Speed *= 1.1
                Y_Speed *= -1
            else:
                X_Speed *= 0.9


def SpecialMovesR():
    global Y_Speed, X_Speed
    # print("HitTime " + str(HitTime))
    # print("hit - TimeR "+str(HitTime - TimeR))
    if HitTime - TimeR < 0.1:
        if Y_Speed * UpDownMovel > 0:
            X_Speed *= 1.1
        elif Y_Speed * UpDownMovel < 0:
            if random.randint(1, 5) == 3:
                X_Speed *= 1.1
                Y_Speed *= -1
            else:
                X_Speed *= 0.9


def moving():
    global ball
    global X_Speed
    global Y_Speed, Play

    if Restart:
        reset_canvas()
    if Play:
        UpDown_collision()
        LeftRight_collisions()
        canvas.move(ball, X_Speed, Y_Speed)
        autoReset()
        window.after(Latency, moving)


window = tk.Tk()
canvas = tk.Canvas(window, bg="light blue", width=width, height=height)
line = canvas.create_line(width // 2, 40, width // 2, height, dash=(50, 50), fill="white")
ball = canvas.create_oval(0.5 * width - 15, 0.5 * height - 15, 0.5 * width + 15, 0.5 * height + 15, fill='#f75a4f')
leftRect = canvas.create_rectangle(5, 0.5 * height - 100, 20, 0.5 * height + 100, fill="white")
rightRect = canvas.create_rectangle(width - 5, 0.5 * height - 100, width - 20, 0.5 * height + 100, fill="white")
Score = canvas.create_text(width // 2, 20, fill="white", font=("Arial", "20"), text=str(A) + " - " + str(B))
canvas.pack()
button1 = tk.Button(window, text='Quit', command=window.destroy)
button2 = tk.Button(window, text='Play/Pause', command=PlayPause)
button2.pack()
button3 = tk.Button(window, text='Reset', command=restart)
button3.pack()
button1.pack()

window.bind("<Up>", rUp)
window.bind("<Down>", rDown)
window.bind("<z>", lUp)
window.bind("<s>", lDown)
window.bind("<space>", playpause)

moving()
window.mainloop()
