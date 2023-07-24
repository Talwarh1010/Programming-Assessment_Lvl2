import re
import pandas


def validate_quantity_unit(user_input, error):
    while True:
        response = input(user_input).lower()
        # Regular expression pattern to match the quantity and unit
        pattern = r'^(\d+)(kg|g|ml|l|L)$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern, re.IGNORECASE)

        # Use re.match() to check if the user input matches the pattern
        match = regex.match(response)

        if match:
            # If a match is found, extract the quantity and unit from the input
            quantity = int(match.group(1))  # Convert the quantity to an integer
            unit = match.group(2).lower()  # Get the unit and convert it to lowercase

            return [quantity, unit, response]
        else:
            # If no match is found, return None
            print(error)
            continue


def currency(x):
    return f"${x:.2f}"


def string_check(question, error):
    while True:
        response = input(question)
        if response.isnumeric():
            print(f"{error}. \nPlease try again. \n")
            continue

        return response


def num_check(question, error, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print(error)

                continue
            return response
        except ValueError:
            print(error)


def get_items():
    item_list = []
    quantity_list = []
    cost_list = []
    per_unit = []
    product_dict = {
        "Item": item_list,
        "Amount": quantity_list,
        "Cost": cost_list,
        "Unit Price": per_unit

    }

    while True:
        item_name = string_check("Item name: ", "The item name cannot be blank or a number")
        if item_name == "xxx":
            per_item = string_check("Do you have any items that are calculated per item (e.g. eggs): ")
            if per_item == "yes":
                continue
            break

        item_quantity = validate_quantity_unit("Quantity(e.g 120g): ", error="Please enter a valid quantity")
        item_cost = num_check("Cost(e.g 10): ", error="Please enter a valid cost", num_type=float)
        conversion_dict = {
            "l": 1 * item_quantity[0],
            "ml": 0.001 * item_quantity[0],
            "g": 0.001 * item_quantity[0],
            "kg": 1 * item_quantity[0]
        }
        converted = conversion_dict[item_quantity[1]]
        print(converted)
        converted_unit = round((item_cost / converted), 2)
        print(converted_unit)
        if item_quantity[1] == "ml" or item_quantity[1] == "l":
            unit = "L"
        else:
            unit = "KG"
        unit_cost = f"${converted_unit}/{unit}"
        print(unit_cost)
        item_list.append(item_name)
        quantity_list.append(item_quantity[2])
        cost_list.append(item_cost)
        per_unit.append(unit_cost)

    price_frame = pandas.DataFrame(product_dict)
    price_frame = price_frame.set_index('Item')
    price_frame[['Cost']] = price_frame[['Cost']].applymap(currency)
    print(price_frame)


get_items()
