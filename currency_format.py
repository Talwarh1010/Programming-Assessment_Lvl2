def currency(x):
    return f"${x:.2f}"


number = 10
print(f"Number is {number}")
converted = currency(10)
print(converted)
number = 12.5
print(f"Number is {number}")
converted = currency(12.5)
print(converted)
number = 0.01925
print(f"Number is {number}")
converted = currency(number)
print(converted)

