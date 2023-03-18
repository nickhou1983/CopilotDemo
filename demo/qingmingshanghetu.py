"""
用Python画一个青蛙上藤蔓的图
"""
import turtle
import time

class TurtleFrog(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('turtle')
        self.color('green')
        self.penup()
        self.goto(-200, -100)
        self.pendown()

    def jump(self, x, y):
        self.penup()
        self.goto(x, y)
        self.pendown()

    def leaf(self):
        self.color('green')
        self.begin_fill()
        self.left(45)
        self.forward(90)
        self.circle(-45, 180)
        self.left(90)
        self.circle(-45, 180)
        self.forward(90)
        self.end_fill()

    def stem(self):
        self.color('brown')
        self.left(135)
        self.forward(100)

    def flower(self):
        self.color('red')
        self.begin_fill()
        for i in range(36):
            self.forward(10)
            self.left(10)
        self.end_fill()

    def petal(self):
        for i in range(2):
            self.left(45)
            self.forward(50)
            self.circle(40, 90)
            self.forward(50)
        
    def move(self):
        self.pensize(5)
        self.color('black')
        self.forward(30)
        self.pensize(1)

    def run(self):
        self.pensize(5)
        self.color('black')
        self.forward(300)

def main():
    turtle.setup(800, 600, 0, 0)
    turtle.penup()
    turtle.goto(-400, 200)
    turtle.pendown()
    turtle.pensize(20)
    turtle.pencolor('brown')
    turtle.seth(-40)
    for i in range(3):
        turtle.circle(40, 80)
        turtle.circle(-40, 80)
    turtle.circle(40, 80/2)
    turtle.fd(40)
    turtle.circle(16, 180)


    


