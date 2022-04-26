# import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def main ():
    clear()
    titlePage()
    sleep(2)
    titlePrompts()

def isVerbose():
    return True #Debug On
    #return False #Debug Off

def titlePage():
    welcomeLine = "Hi! Welcome to Lemonsville, California!"
    intro = "In this small town, you are in charge of running your own lemonade stand.\nYou can compete with as many other people as you wish, but how much profit \nyou make is up to you (the other stands' sales will not affect your business \nin any way). \n\nIf you make the most money, you're the winner!!"
    print(welcomeLine + "\n\n")
    print(intro + "\n\n")

def titlePrompts():
    newGameQuestion = "Are you starting a new game? (Y or N)\nType your answer and hit Enter/Return ==> "
    playerCountQ = "How many people will be playing ==> "
    isNewGame = yesNoPrompt(newGameQuestion)
    playerCount = howMany(playerCountQ)

def yesNoPrompt(qText):
    # Sets to simplify if/else in determining correct answers.
    yesChoice = ['yes', 'y']
    noChoice = ['no', 'n']

    while True:
        yesNoPrompt = input(qText)
        # Check if our answer is in one of two sets.
        if yesNoPrompt.lower() in yesChoice:
            # call method
            if isVerbose(): print("you typed: " + yesNoPrompt)
            return yesNoPrompt
            break
        elif yesNoPrompt.lower() in noChoice:
            # call method
            if isVerbose(): print("you typed: " + yesNoPrompt)
            return yesNoPrompt
            break
        else:
            if isVerbose(): print("you typed: " + yesNoPrompt)
            print("\a")
            print("Invalid response, try again.\n")
            continue

def howMany(cText):

    while True:
        count = int(input(cText))
        print(count)
        if count in range(1,30):
            if isVerbose(): print("you typed: " + str(count))
            return count
            break
        else:
            if isVerbose(): print("you typed: " + str(count))
            print("\a")
            print("Invalid response, try again.\n")
            continue

main()
