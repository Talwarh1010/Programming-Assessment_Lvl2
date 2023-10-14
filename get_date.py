from datetime import date

today = date.today()
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")
heading = f"The heading would be ----- Price Comparison Calculator ({day}/{month}/{year}) -----"
print(f"The current date is {today}")
print(heading)