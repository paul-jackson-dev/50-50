import json

while True:
    print("----------------------")
    print("s : close all positions")
    # print("s75 : reduce positions by 75%")
    print("r : set risk")
    print("c : close a symbol")
    print("type a symbol to open")
    print("")
    command = input("enter a command: ")

    if command == "s":
        outside_command_path = "json/" + "outside_command.json"
        with open(outside_command_path, 'w') as file_object:  # open the file in write mode
            json.dump(command, file_object)

    if command == "s75":
        outside_command_path = "json/" + "outside_command.json"
        with open(outside_command_path, 'w') as file_object:  # open the file in write mode
            json.dump(command, file_object)

    if command == "r":
        outside_command_path = "json/" + "risk.json"
        with open(outside_command_path, 'r') as openfile:
            risk = json.load(openfile)
        command = input("risk is " + risk + ". enter the new risk: ")
        with open(outside_command_path, 'w') as file_object:  # open the file in write mode
            json.dump(command, file_object)

    if command == "c":
        path = "json/" + "close.json"
        command = input("symbol to close: ").upper()
        with open(path, 'w') as file_object:  # open the file in write mode
            json.dump(command, file_object)
    else:
        path = "json/" + "open.json"
        with open(path, 'w') as file_object:  # open the file in write mode
            json.dump(command.upper(), file_object)

    print("you entered: " + command)
