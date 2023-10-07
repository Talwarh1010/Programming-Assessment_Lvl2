# Used for validating quantity
import re
# Used for the start screen and welcome message
from turtle import Screen
import turtle
# Used for creating a table from a dataframe
from tabulate import tabulate
# Used to create a dataframe
import pandas as pd


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
    style = ("Comic Sans MS", 25, "normal")
    second_style = ("Comic Sans MS", 15, "normal")
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
            print("Please enter a valid quantity.")
            continue


# Format a number as currency with 2 decimal places
def currency(x):
    return f"${x:.2f}"


# Validate item name input
def validate_input(question, validation_function, error_message):
    while True:
        response = input(question)
        if validation_function(response):
            return response
        print(f"{error_message}. Please try again.\n")


# Gets the user budget, all the item info, creates a table and a text file
def get_items():
    # Ask user for budget
    user_budget = float(
        validate_input("What is your budget: $", lambda x: x.replace(".", "", 1).isnumeric() and float(x) > 0,
                       "Please enter a valid budget"))

    # Initialize lists to store item details
    item_list, quantity_list, converted_quantity_list, cost_list, per_unit_list, per_unit_num_list, unit_types = [], [], [], [], [], [], []

    while True:
        # Ask the user for the name of the item
        item_name = validate_input("Item name: ", lambda x: x.replace(" ", "").isalnum(),
                                   "The item name can only include letters and numbers")

        # Check if the user entered 'xxx' as the item name without entering any other items
        if item_name == "xxx" and not item_list:
            print("Please enter at least one item.")
            continue
        # Check if the user entered 'xxx' to exit the item entry loop
        elif item_name == "xxx":
            break

        quantity, unit, quantity_str, converted_quantity, converted_unit = validate_quantity_unit(
            "What is the quantity (e.g 120kg, 10l): ")
        unit_types.append(unit)

        # Prompt the user for the total cost of the item
        item_cost = float(
            validate_input("What is the total cost: $", lambda x: x.replace(".", "", 1).isnumeric() and float(x) > 0,
                           "Please enter an number more than 0"))

        # Calculate the converted quantity and unit cost
        unit_cost_num = item_cost / converted_quantity

        # For display in the dataframe
        per_unit_str = f"${unit_cost_num:.3f}/{converted_unit}"

        # Append item details to lists(to form a dataframe)
        item_list.append(item_name)
        quantity_list.append(quantity_str)
        converted_quantity_list.append(f"{converted_quantity:.3f}{converted_unit}")
        cost_list.append(round(item_cost, 3))
        per_unit_list.append(per_unit_str)
        per_unit_num_list.append(unit_cost_num)

    # Create a dictionary to store item details
    item_dict = {
        "Item": item_list,
        "Amount": quantity_list,
        "Converted amount": converted_quantity_list,
        "Cost": cost_list,
        "Unit Price": per_unit_list,
        "num_unit_price": per_unit_num_list
    }

    # Create a DataFrame to display and manipulate the data
    price_frame = pd.DataFrame(item_dict)
    price_frame = price_frame.set_index('Item')

    # Sort the DataFrame by 'Unit Price' in ascending order
    price_frame = price_frame.sort_values(by='num_unit_price', ascending=True)

    # Remove the Unit Price Numeric column
    price_frame = price_frame.drop(columns=['num_unit_price'])

    # Create a new dataframe and filter items that are within the user's budget
    affordable_items = price_frame[price_frame['Cost'] <= user_budget]

    # Format the 'Cost' column in as currency
    price_frame[['Cost']] = price_frame[['Cost']].applymap(currency)

    # Display the price information as a table
    table = tabulate(price_frame, headers='keys', tablefmt='fancy_grid')

    if not affordable_items.empty:
        # Get the best option (lowest unit price) within the user's budget
        best_option = affordable_items.iloc[0]
        best_option_name = best_option.name
        conclusion = f"The best option within your budget (${user_budget}) is: {best_option_name}"
    else:
        conclusion = "There are no affordable options"
        best_option_name = "no affordable options"

    if "kg" in unit_types and "l" in unit_types:
        important_note = "Disclaimer - Since you have compared items that have different unit types, the " \
                         "result may differ from what " \
                         "you were expecting."
    else:
        important_note = ""

    return table, conclusion, best_option_name, important_note


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
        table_txt, conclusion_txt, best_option_txt, important_note_txt = get_items()
        print(f"{table_txt}\n\n{conclusion_txt}\n{important_note_txt}")
        # Create a text file with the table and conclusion
        file_name = f"{best_option_txt}.txt"
        with open(file_name, "w+", encoding="utf-8") as text_file:
            text_file.write(table_txt)
            text_file.write("\n\n")
            text_file.write(conclusion_txt)
            text_file.write("\n")
            text_file.write(important_note_txt)

    elif choice == '3':
        print("Thank you for using the Price Comparison Calculator. Goodbye!")
        break
    else:
        print("Invalid choice. Please choose a valid option (1/2/3).")
