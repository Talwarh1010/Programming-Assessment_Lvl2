# Necessary import modules. Used for creating regex patterns, turtle graphics, and dataframes
import re, turtle, pandas as pd
# Creates screen for turtle graphics
from turtle import Screen
# Used for creating a table for the item details
from tabulate import tabulate
# Used for getting today's date
from datetime import date
# For the bar graph generation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Start screen with welcome message
def start():
    # Set up the turtle graphics window
    # Changes the colour to background to black
    turtle.bgcolor('black')
    welcome_screen = Screen()
    # Add a title for the top left of the window
    welcome_screen.title("Price Comparison Calculator by Harveer Talwar")
    # Adjust the window size
    welcome_screen.setup(1000, 500)
    turtle_pointer = turtle.Turtle()
    # Change the colour of pointer to white
    turtle_pointer.color('white')
    # Change the pointer shape to a turtle
    turtle_pointer.shape('turtle')

    # Move the turtle to the starting point
    turtle_pointer.penup()
    turtle_pointer.goto(-100, 0)
    turtle_pointer.pendown()

    # Draw S shape
    turtle_pointer.forward(45)
    turtle_pointer.circle(50, 180)
    turtle_pointer.circle(-50, 180)
    turtle_pointer.forward(45)

    # Draw horizontal lines across the "S" shape
    for x in [-70, -50]:
        turtle_pointer.penup()
        turtle_pointer.goto(x, -10)
        turtle_pointer.setheading(90)
        turtle_pointer.pendown()
        turtle_pointer.forward(225)

    # Display a welcome message and instructions
    turtle_pointer.penup()
    turtle_pointer.goto(-50, -60)
    # Set font for the main message
    style = ('Courier', 25, 'italic')
    # Set font for the small message
    second_style = ("Courier", 15, "normal")
    turtle_pointer.write("Welcome to Price Comparison Calculator", font=style, align='center')
    turtle_pointer.goto(-50, -100)
    turtle_pointer.pendown()
    turtle_pointer.hideturtle()
    turtle_pointer.write("Close this window to begin using the calculator", font=second_style, align='center')
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
def validate_quantity_unit(question):
    while True:
        response = input(question).lower()
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
            # Splits the input into two variables (quantity - number and unit - letters)
            quantity, unit = float(match.group(1)), match.group(3).lower()
            # Set dictionary for the conversion to common unit
            conversion_dict = {"l": 1, "ml": 0.001, "g": 0.001, "kg": 1}
            converted_quantity = quantity * conversion_dict.get(unit)
            # Find converted unit (The unit that the number is being converted to)
            converted_unit = "L" if unit in ["ml", "l"] else "KG"
            # Return these for further calculations
            return quantity, unit, f"{quantity}{unit}", converted_quantity, converted_unit
        # If quantity is invalid, print error
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
        # if it returns True, then it is valid
        if validation_function(response):
            return response
        print(f"{error_message}. Please try again.\n")


def plot_unit_costs(items, unit_costs, budget_user, cost_list):
    # Create a DataFrame to hold the items and unit costs
    df = pd.DataFrame({'Item': items, 'Unit Cost': unit_costs, 'Cost': cost_list})

    # Sort the DataFrame by 'Unit Cost' in ascending order
    df = df.sort_values(by='Unit Cost', ascending=True)

    # Extract the sorted items, unit costs, and costs
    sorted_items = df['Item']
    sorted_unit_costs = df['Unit Cost']
    sorted_costs = df['Cost']

    # Create a list of colors based on whether the cost is within the budget
    colors = ['red' if cost > budget_user else 'skyblue' for cost in sorted_costs]
    plt.figure(figsize=(10, 6))
    # Create horizontal bar graph with the item names and the corresponding unit prices
    plt.barh(sorted_items, sorted_unit_costs, color=colors)
    # Label x and y axis by unit cost and item name
    plt.xlabel('Unit Cost ($ per unit)')
    plt.ylabel('Item name')
    # Create heading for the bar graph
    plt.title(f'Unit Cost Comparison (Budget: ${budget_user:.2f})')
    plt.gca().invert_yaxis()  # Invert the y-axis to show the lowest unit costs at the top
    # Ensures everything is within the window
    plt.tight_layout()
    # Creates legends(What the colours mean) for the bar graph
    handles = [mpatches.Patch(color='skyblue', label='Under Budget'),
               mpatches.Patch(color='red', label='Exceeds Budget')]
    plt.legend(handles=handles, loc='upper right')
    # Display the bar graph
    plt.show()


# Gets the user budget, all the item info, creates a table and a text file
def get_items():
    # Ask user for budget
    user_budget = float(
        validate_input("What is your budget: $", lambda x: x.replace(".", "", 1).isnumeric() and float(x) > 0,
                       "Please enter a valid budget. (A number more than 0)"))

    # Initialize lists to store item details
    item_names_list, quantity_strings_list, converted_quantity_strings_list, item_costs_list, unit_price_strings_list,\
        unit_prices_num_list, unit_types, \
        graph_input = [], [], \
        [], [], [], [], [], []

    while True:
        # Ask the user for the name of the item
        item_name = validate_input("Item name (enter 'xxx' to quit entering items): ",
                                   lambda x: x.replace(" ", "").isalnum(),
                                   "The item name can only include letters, integers and spaces")

        # Check if the user entered 'xxx' as the item name without entering any other items
        if item_name == "xxx" and not item_names_list:
            print("Please enter at least one item.")
            continue
        # Check if the user entered 'xxx' to exit the item entry loop
        elif item_name == "xxx":
            break
        # Ask user for quantity and unit
        quantity, unit, quantity_str, converted_quantity, converted_unit = validate_quantity_unit(
            "What is the quantity and unit (e.g 120kg, 10l): ")
        unit_types.append(unit)

        # Prompt the user for the total cost of the item
        item_cost = float(
            validate_input("What is the total cost: $", lambda x: x.replace(".", "", 1).isnumeric() and float(x) > 0,
                           "Please enter an number more than 0"))

        # Calculate the converted quantity and unit cost
        unit_cost_num = item_cost / converted_quantity

        # For display in the dataframe
        per_unit_str = f"${unit_cost_num:.2f}/{converted_unit}"

        # Append item details to lists(to form a dataframe)
        item_names_list.append(item_name)
        quantity_strings_list.append(quantity_str)
        converted_quantity_strings_list.append(f"{converted_quantity:.3f}{converted_unit}")
        item_costs_list.append(round(item_cost, 3))
        unit_price_strings_list.append(per_unit_str)
        unit_prices_num_list.append(unit_cost_num)

    # Create a dictionary to store item details
    item_dict = {
        "Item": item_names_list,
        "Amount": quantity_strings_list,
        "Converted amount": converted_quantity_strings_list,
        "Cost": item_costs_list,
        "Unit Price": unit_price_strings_list,
        "num_unit_price": unit_prices_num_list
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

    # Display the data frame as a table
    table = tabulate(price_frame, headers='keys', tablefmt='fancy_grid')
    # Finds best option within the budget
    if not affordable_items.empty:
        # Get the best option (lowest unit price) within the user's budget
        best_option = affordable_items.iloc[0]
        best_option_name = best_option.name
        conclusion = f"The best option within your budget (${user_budget:.2f}) is: {best_option_name}"
    else:
        conclusion = "There are no affordable options"
    # Add disclaimer if user enter items with different unit types.
    if "kg" in unit_types and "l" in unit_types:
        important_note = "Disclaimer - Since you have compared items that have different unit types, the " \
                         "result may differ from what " \
                         "you were expecting."
    # No disclaimer if all the item units are the same
    else:
        important_note = ""

    return table, conclusion, important_note, user_budget, item_names_list, unit_prices_num_list, item_costs_list


# Main Routine
start()

# Main menu loop
while True:
    print("""Menu
1 - View Instructions 📝
2 - Start Price Comparison 💲
3 - Quit 👋""")

    menu_choice = input("Enter your choice, (1/2/3): ")
    # Display instructions if user enters '1'
    if menu_choice == '1':
        instructions()
        print()
    # Start price comparison if user enters '2'
    elif menu_choice == '2':
        # Get today's date
        today = date.today()
        formatted_date = today.strftime("%d/%m/%Y")
        # Get heading for output
        heading = f"----- Price Comparison Calculator ({formatted_date}) -----"
        table_txt, conclusion_txt, important_note_txt, user_budget_txt, item_list_txt, per_unit_list_txt, cost_list_text = get_items()
        # For displaying in the output.
        budget = f"Budget: ${user_budget_txt:.2f}"
        print(f"\n{heading}\n\n{budget}\n\n{table_txt}\n\n{conclusion_txt}\n\n{important_note_txt}")
        # Regex pattern for text file name (Allows letters, uppercase and lowercase). Allows numbers as well as
        # underscores, brackets, dashes, full stops, and commas
        valid_filename_pattern = re.compile(r"^[a-zA-Z0-9_()\-,.]+$")

        # Create a text file with the table and conclusion
        user_file_name = validate_input("What would you like the text file name to be? ",
                                        lambda x: bool(valid_filename_pattern.match(x)), "Please enter a "
                                                                                         "valid file name. Only "
                                                                                         "letters, and numbers are "
                                                                                         "allowed as well as "
                                                                                         "underscores, brackets, dashes"
                                                                                         "commas, and full stops")
        # Create a list to print to out on the text file
        to_write = [heading, budget, table_txt, conclusion_txt, important_note_txt]
        # Create text file with intended file name
        file_name = f"{user_file_name}.txt"
        # Open text file and write item information to the text file
        with open(file_name, "w+", encoding="utf-8") as text_file:
            for item in to_write:
                text_file.write(item)
                text_file.write("\n\n")
        # Plot bar graph and display it
        plot_unit_costs(item_list_txt, per_unit_list_txt, user_budget_txt, cost_list_text)

    # Program ends with a fare well message if user enters '3'
    elif menu_choice == '3':
        print("Thank you for using the Price Comparison Calculator. Goodbye!")
        break
    # If user does not enter 1, 2 or 3. Give error
    else:
        print("Invalid choice. Please choose a valid option (1/2/3).")
