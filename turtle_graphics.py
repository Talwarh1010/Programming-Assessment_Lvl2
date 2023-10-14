import turtle


def start():
    # Set up the turtle graphics window
    turtle.bgcolor('black')
    screen = turtle.Screen()
    screen.title("Price Comparison Calculator by Harveer Talwar")
    screen.setup(1000, 500)
    t = turtle.Turtle()
    t.color('white')
    t.shape('turtle')

    # Draw a 'S' shape and horizontal lines
    t.penup()
    t.goto(-100, 0)
    t.pendown()
    t.forward(45)
    t.circle(50, 180)
    t.circle(-50, 180)
    t.forward(45)

    for x in [-70, -50]:
        t.penup()
        t.goto(x, -10)
        t.setheading(90)
        t.pendown()
        t.forward(225)

    # Display a welcome message and instructions
    t.penup()
    t.goto(-50, -60)
    style = ('Courier', 25, 'italic')
    second_style = ("Courier", 15, "normal")
    t.write("Welcome to Price Comparison Calculator", font=style, align='center')
    t.goto(-50, -100)
    t.pendown()
    t.hideturtle()
    t.write("Close this window to begin using the calculator", font=second_style, align='center')
    turtle.done()


start()
