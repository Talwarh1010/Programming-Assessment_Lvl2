def instructions():
    print("""***** Instructions *****
    Enter the name of an item, quantity (e.g., 120kg, 10l), and its total cost
    To finish entering items, type 'xxx' when prompted for the item name
    After entering all items, you will see a table with price information
    The program will identify the best option within your budget
    All the price comparison information will be added to an auto-generated text file
    You can view the text file at any time and share it with people of your choice
    Enjoy using the calculator!""")


while True:
    print("""Menu
1 - View Instructions 📝
2 - Start Price Comparison 💲
3 - Quit 👋""")

    choice = input("Enter your choice, (1/2/3): ")
    if choice == '1':
        instructions()
        print()
    elif choice == '2':
        print()
        print("Start price comparison")
        print()


    elif choice == '3':
        print("Thank you for using the Price Comparison Calculator. Goodbye!")
        print()
        break
    else:
        print("Invalid choice. Please choose a valid option (1/2/3).")
