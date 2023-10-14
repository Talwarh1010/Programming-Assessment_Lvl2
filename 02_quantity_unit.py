import re


def validate_quantity_unit(user_input):
    while True:
        response = input(user_input)
        # Regular expression pattern to match the quantity and unit
        pattern = r'^(\d+)(kg|g|ml|L)$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern, re.IGNORECASE)

        # Use re.match() to check if the user input matches the pattern
        match = regex.match(response)

        if match:
            # If a match is found, extract the quantity and unit from the input
            quantity = int(match.group(1))  # Convert the quantity to an integer
            unit = match.group(2).lower()  # Get the unit and convert it to lowercase
            return quantity, unit

        print("Error")
        continue


amount = validate_quantity_unit("How much do you have? ")
