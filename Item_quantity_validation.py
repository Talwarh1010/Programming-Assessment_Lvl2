import re


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
            print("Please enter a valid quantity. A number followed by a unit. Units allowed - (kg, g, l, ml)")
            continue


validate_quantity_unit(
    "What is the quantity and unit (e.g 120kg, 10l): ")
