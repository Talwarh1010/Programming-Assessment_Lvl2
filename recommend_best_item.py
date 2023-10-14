import pandas as pd
from tabulate import tabulate


def currency(x):
    return f"${x:.2f}"


item_dict = {
    "Item": ['Sea Salt Crackers', 'Griffins Snax', 'Pizza shapes', 'Arnotts Cheds ', 'Rosemary Wheat', 'Original Rice '
                                                                                                      'Crackers'],
    "Amount": ['185.0g', '250.0g', '190.0g', '250.0g', '170.0g', '100.0g'],
    "Converted amount": ['0.185KG', '0.250KG', '0.190KG', '0.250KG', '0.170KG', '0.100KG'],
    "Cost": [2.0, 2.5, 3.3, 3.99, 2.0, 1.5],
    "Unit Price": ['$10.81/KG', '$10.00/KG', '$17.37/KG', '$15.96/KG', '$11.76/KG', '$15.00/KG'],
    "num_unit_price": [10.81081081081081, 10.0, 17.36842105263158, 15.96, 11.76470588235294, 15.0]
}
unit_types = ["kg"]
user_budget = 2.50
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
    conclusion = f"The best option within your budget (${user_budget:.2f}) is: {best_option_name}"
else:
    conclusion = "There are no affordable options"
# Add disclaimer if user enter items with different unit types.
if "kg" in unit_types and "l" in unit_types:
    important_note = "Disclaimer - Since you have compared items that have different unit types, the " \
                     "result may differ from what " \
                     "you were expecting."
else:
    important_note = ""
print(f"{table}\n\n{conclusion}")