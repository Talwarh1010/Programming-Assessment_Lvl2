# Necessary import modules. Used for creating regex patterns, turtle graphics, and dataframes
import re, turtle, pandas as pd
# Creates screen for turtle
from turtle import Screen
# Used for creating a table
from tabulate import tabulate
# Used for getting today's date
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Start screen with welcome message
def start():
    # Set up the turtle graphics window
    turtle.bgcolor('black')
    screen = Screen()
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

# Display program instructions
def instructions():
    print("""***** Instructions *****
    Enter the name of an item, quantity (e.g., 120kg, 10l), and its total cost
    To finish entering items, type 'xxx' when prompted for the item name
    After entering all items, you will see a table with price information
    The program will identify the best option within your budget
    All the price comparison information will be added to an auto-generated text file
    You can view the text file at any time and share it with people of your choice
    You can also choose the text file name
    You will also have access to a bar graph that compares all the item unit prices
    The bar graph can also be saved on your device
    You can use this calculator however many times you want by entering "2" in the menu again.
    Enjoy using the calculator!""")

# Validate quantity and unit input
def validate_quantity_unit(user_input):
    while True:
        response = input(user_input).lower()
        # A pattern to match the quantity (e.g 120kg, 10l)
        # - ^: Match to the start of the input
        # - (0*[1-9]\d*(\.\d+)?|0*\.\d*[1-9]\d*):
        #   - 0*: Zero or more leading zeros
        #   - [1-9]\d*: A non-zero digit followed by zero or more digits
        #   - (\.\d+)?: An optional decimal point followed by one or more digits (for decimals)
        # - (kg|g|ml|l): Match a unit, which can be kg, l, ml, g
        # - $: match to the end of the input
        pattern = r'^(0*[1-9]\d*(\.\d+)?|0*\.\d*[1-9]\d*)(kg|g|ml|l)$'
        match = re.match(pattern, response, re.IGNORECASE)

        if match:
            quantity, unit = float(match.group(1)), match.group(3).lower()
            conversion_dict = {"l": 1, "ml": 0.001, "g": 0.001, "kg": 1}
            converted_quantity = quantity * conversion_dict.get(unit)
            # Find converted unit (The unit that the number is being converted to)
            converted_unit = "L" if unit in ["ml", "l"] else "KG"
            return quantity, unit, f"{quantity}{unit}", converted_quantity, converted_unit
        else:
            print("Please enter a valid quantity. A number followed by a unit. Units allowed - (kg, g, L, ml)")
            continue

# Format a number as currency with 2 decimal places
def currency(x):
    return f"${x:.2f}"

# Validate item name, budget, cost, and text file name
def validate_input(question, validation_function, error_message):
    while True:
        response = input(question)
        if validation_function(response):
            return response
        print(f"{error_message}. Please try again.\n")

# The code that follows in this section is self-explanatory and does not require additional comments.

# Main Routine
start()

# Main menu loop
while True:
    print("""Menu
1 - View Instructions 📝
2 - Start Price Comparison 💲
3 - Quit 👋""")

    choice = input("Enter your choice, (1/2/3): ")
    if choice == '1':
        instructions()
        print()
    elif choice == '2':
        # Get today's date
        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")
        # Get heading for output
        heading = f"----- Price Comparison Calculator ({day}/{month}/{year}) -----"
        table_txt, conclusion_txt, important_note_txt, user_budget_txt, item_list_txt, per_unit_list_txt, cost_list_text = get_items()
        # For displaying in the output.
        budget = f"Budget: ${user_budget_txt:.2f}"
        print(f"\n{heading}\n\n{budget}\n\n{table_txt}\n\n{conclusion_txt}\n\n{important_note_txt}")

        valid_filename_pattern = re.compile(r'^[a-zA-Z0-9_()\-,.]+$')

        # Create a text file with the table and conclusion
        user_file_name = validate_input("What would you like the text file name to be? ",
                                        lambda x: bool(valid_filename_pattern.match(x)), "Please enter a "
                                                                                         "valid file name. Only "
                                                                                         "letters, and numbers are "
                                                                                         "allowed as well as "
                                                                                         "underscores, brackets, "
                                                                                         "commas, and full stops")
        # Create a list to print to out on the text file
        to_write = [heading, budget, table_txt, conclusion_txt, important_note_txt]
        file_name = f"{user_file_name}.txt"
        with open(file_name, "w+", encoding="utf-8") as text_file:
            for item in to_write:
                text_file.write(item)
                text_file.write("\n\n")

        plot_unit_costs(item_list_txt, per_unit_list_txt, user_budget_txt, cost_list_text)


    elif choice == '3':
        print("Thank you for using the Price Comparison Calculator. Goodbye!")
        break
    else:
        print("Invalid choice. Please choose a valid option (1/2/3).")
