
def menu():
    print("WELCOME")
    print("OPTIONS")
    print("1. Register")
    print("2. Log in")
    op = input("Select and option: ")
    return op
    
def menu_in(): 
    print("Activities: ")
    print("1. Show all users")
    print("2. Add user")
    print("3. Show contact details from user")
    print("4. Private chat")
    print("5. Join a room")
    print("6. Send presence message")
    print("7. Chat with everyone")
    print("8. Send file")
    print("9. Exit session")
    print("10. Delete your account")
    op = input("Select one activity: ")
    return op

def show_menu(): 
    print("What do you wanna show? ")
    print("1. Chat")
    print("2. Away")
    print("3. Extended away")
    print("4. Do not disturb")
    op = input("==> ")
    return op