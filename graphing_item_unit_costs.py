import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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
    plt.barh(sorted_items, sorted_unit_costs, color=colors)

    plt.xlabel('Unit Cost ($ per unit)')
    plt.ylabel('Item name')
    plt.title(f'Unit Cost Comparison (Budget: ${budget_user:.2f})')
    plt.gca().invert_yaxis()  # Invert the y-axis to show the lowest unit costs at the top
    plt.tight_layout()

    handles = [mpatches.Patch(color='skyblue', label='Under Budget'),
               mpatches.Patch(color='red', label='Exceeds Budget')]
    plt.legend(handles=handles, loc='upper right')

    plt.show()


plot_unit_costs(items=['Sea Salt Crackers', 'Griffin Snax', 'Pizza Shapes', 'Arnotts Cheds', 'Rosemary Wheat',
                       'Original Rice Crackers'], unit_costs=[10.81, 10.00, 17.37, 15.96, 11.76, 16.5],
                cost_list=[2.00, 2.50, 3.30, 3.99, 2.00, 1.65], budget_user=2.5)


