# Greg is an automated robot. He is an interface to program in various different functions.
# He is currently a work in progress, and will be till he does everything important

import stockBot
import time


def main():
    input("Would you like to access Greg? (Press enter to continue)")
    print("/n/n/n")

    print("You have three options: step mode(s), auto mode(a), and exit(e)")
    print("Step mode will allow you to step through the program one step at a time")
    print("Auto mode will allow you to run the program automatically")
    print("Exit will exit the program")
    print("To access these modes, enter the letter in the parentheses")
    print()
    ans = input(">")

    if ans == "s":
        while True:
            stockBot.mainProgram()
            ans = input("Would you like to continue? (y/n)")
            if ans == "n":
                break
            else:
                continue

    elif ans == "a":
        while True:
            stockBot.mainProgram()
            time.sleep(60)

    elif ans == "e":
        return 0

    else:
        print("Invalid input. Please try again")
        main()
