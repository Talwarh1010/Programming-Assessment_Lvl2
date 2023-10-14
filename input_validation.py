# Validate item name input
import re


def validate_input(question, validation_function, error_message):
    while True:
        response = input(question)
        if validation_function(response):
            return response
        print(f"{error_message}. Please try again.\n")


float(validate_input("What is your budget: $", lambda x: x.replace(".", "", 1).isnumeric() and float(x) > 0,
                     "Please enter a valid budget. (A number more than 0)"))
print()

validate_input("Item name (enter 'xxx' to quit entering items): ",
               lambda x: x.replace(" ", "").isalnum(),
               "The item name can only include letters, integers and spaces")

valid_filename_pattern = re.compile(r'^[a-zA-Z0-9_()\-,.]+$')

validate_input("What would you like the text file name to be? ",
                   lambda x: bool(valid_filename_pattern.match(x)), "Please enter a "
                                                                    "valid file name")
print()
