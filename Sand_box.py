import re
import turtle
from tabulate import tabulate
from turtle import Screen
import pandas as pd


def start():
    turtle.bgcolor('black')
    screen = Screen()
    screen.title("Price Comparison Calculator by Harveer Talwar")
    screen.setup(1000, 500)
    t = turtle.Turtle()
    t.color('white')
    t.shape('turtle')

    t.penup()
    t.goto(-100, 0)
    t.pendown()
    t.forward(45)
    t.circle(50, 180)
    t.circle(-50, 180)
    t.forward(45)

    # Draw horizontal lines
    for x in [-70, -50]:
        t.penup()
        t.goto(x, -10)
        t.setheading(90)
        t.pendown()
        t.forward(225)

    t.penup()
    t.goto(-50, -60)
    style = ("Comic Sans MS", 25, "normal")
    second_style = ("Comic Sans MS", 15, "normal")
    t.write("Welcome to Price Comparison Calculator", font=style, align='center')
    t.goto(-50, -100)
    t.pendown()
    t.hideturtle()
    t.write("Close this window to begin using the calculator", font=second_style, align='center')
    turtle.done()


def instructions():
    print("""***** Instructions *****
    Enter the name of an item, quantity (e.g., 120kg, 10l), and its total cost
    To finish entering items, type 'xxx' when prompted for the item name
    After entering all items, you will see a table with price information
    The program will identify the best option within your budget
    All the price comparison information will be added to an auto-generated Excel file
    You can view the Excel file at any time and share it with people of your choice
    Enjoy using the calculator!""")


def validate_quantity_unit(user_input):
    while True:
        response = input(user_input).lower()
        pattern = r'^(0*[1-9]\d*(\.\d+)?|0*\.\d*[1-9]\d*)(kg|g|ml|l)$'
        match = re.match(pattern, response, re.IGNORECASE)

        if match:
            quantity, unit, _, _ = float(match.group(1)), match.group(3).lower(), match.group(0), None
            conversion_dict = {"l": 1, "ml": 0.001, "g": 0.001, "kg": 1}
            converted_quantity = quantity * conversion_dict.get(unit, 1)
            converted_unit = "L" if unit in ["ml", "l"] else "KG"
            return quantity, unit, f"{quantity}{unit}", converted_quantity, converted_unit
        else:
            print("Please enter a valid quantity.")
            continue


def currency(x):
    return f"${x:.2f}"


def yes_no(question):
    to_check = ["yes", "no"]
    while True:
        response = input(question).lower()
        if response in to_check:
            return response
        elif response[0] in to_check[0]:
            return to_check[0]
        print("Please enter either 'yes' or 'no'.")


def string_check(question):
    while True:
        response = input(question)
        if response.isnumeric():
            print("The item name cannot be blank or a number.")
            continue
        return response


def num_check(question, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print("Please enter a number more than 0.")
                continue
            return response
        except ValueError:
            print("Please enter a valid number.")


def get_items():
    item_number = 0
    user_budget = num_check("What is your budget: $", float)
    item_list, quantity_list, converted_quantity_list, cost_list, per_unit_list = [], [], [], [], []

    while True:
        item_name = string_check("Item name: ")
        item_number += 1

        if item_name == "xxx" and item_number == 1:
            print("Please enter at least one item.")
            continue
        elif item_name == "xxx":
            break

        quantity = validate_quantity_unit("What is the quantity (e.g 120kg, 10l): ")
        item_cost = num_check("What is the total cost: $", float)
        converted_quantity, converted_unit = quantity[3], quantity[4]
        unit_cost = round((item_cost / converted_quantity), 2)
        per_unit = f"${unit_cost}/{converted_unit}"

        item_list.append(item_name)
        quantity_list.append(quantity[2])
        converted_quantity_list.append(f"{converted_quantity}{converted_unit}")
        cost_list.append(item_cost)
        per_unit_list.append(per_unit)

    item_dict = {
        "Item": item_list,
        "Amount": quantity_list,
        "Converted amount": converted_quantity_list,
        "Cost": cost_list,
        "Unit Price": per_unit_list
    }

    price_frame = pd.DataFrame(item_dict)
    price_frame = price_frame.set_index('Item')
    price_frame[['Cost']] = price_frame[['Cost']].applymap(currency)
    price_frame['Unit Price Numeric'] = price_frame['Unit Price'].str.replace(r'\$|/.*', '', regex=True).astype(float)
    price_frame = price_frame.sort_values(by='Unit Price Numeric', ascending=True)
    price_frame = price_frame.drop(columns=['Unit Price Numeric'])
    table = tabulate(price_frame, headers='keys', tablefmt='fancy_grid')
    print(table)

    price_frame['Cost'] = price_frame['Cost'].str.replace('$', '').astype(float)
    affordable_items = price_frame[price_frame['Cost'] <= user_budget]

    if not affordable_items.empty:
        best_option = affordable_items.iloc[0]
        best_option_name = best_option.name
        conclusion = f"The best option within your budget (${user_budget}) is: {best_option_name}"
    else:
        conclusion = "There are no affordable options"
        best_option_name = "no affordable options"

    print(conclusion)
    file_name = f"{best_option_name}.txt"
    with open(file_name, "w+", encoding="utf-8") as text_file:
        text_file.write(table)
        text_file.write("\n\n")
        text_file.write(conclusion)


start()
print("""\n Menu
1. View Instructions 📝
2. Start Price Comparison 💲
3. Quit 👋""")
while True:
    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        instructions()
        print()
    elif choice == '2':
        get_items()
        print()
    elif choice == '3':
        print("Thank you for using the Price Comparison Calculator. Goodbye!")
        break
    else:
        print("Invalid choice. Please choose a valid option (1/2/3).")
