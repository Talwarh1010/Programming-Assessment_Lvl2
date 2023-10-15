from datetime import date

today = date.today()
formatted_date = today.strftime("%d/%m/%Y")
heading = f"The heading would be ----- Price Comparison Calculator ({formatted_date}) -----"
print(f"The current date is {today}")
print(heading)