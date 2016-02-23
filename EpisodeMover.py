import json
import os
import re
import shutil

# Moves files/folders from source path to the show directory specified by
# user if all show keywords are in the file/folder name 
def move_files():
    srcdir = input("Please enter the full path where your videos are located.\n" +
                   "Example: C:\\user\\downloads\\ \n").strip()
    while not os.path.isdir(srcdir):
        srcdir = input("Invalid directory. Please enter the full path where your " +
                       "videos are located.\n Example: C:\\user\\downloads\\ \n").strip()
    for filename in os.listdir(srcdir):
        # Only look for folders/files in the format "S##E##". Example: "X-Files S01E02"
        if re.search('[sS]\\d{2}[eE]\\d{2}', filename):
            found = False
            filepath = os.path.join(srcdir, filename)
            name = filename.lower()
            for key in data.keys():
                keywords = key.split()
                if all(word in name for word in keywords):
                    found = True
                    shutil.move(filepath, data[key])
                    print("*** Moved:", (filename[:41] + "...") if len(filename) > 44 else filename)
                    break
            if not found:
                # Prints the shows that matched the episode formatting, but were not
                # configured to be processed
                print("* Not processed:", (filename[:35] + '...') if len(filename) > 38 else filename)

# Adds directories to the data dictionary. User adds show keywords that map to the
# show's directory path
# Keywords are used so "X.Files", "X-Files", and "X Files" will all be matched by the
# two keywords: "X" and "Files"
def add_directory():
    showKeywords = input("Input mandatory keywords for the show title seperated by a space.\n" +
                         "Example: X files\n").lower().strip()
    while re.search('[^A-Za-z0-9 ]+', showKeywords):
        showKeywords = input("Invalid, please input alphanumeric characters only\n" +
                             "Input mandatory keywords for the show title seperated by a space.\n" +
                             "Example: X files\n").lower().strip()
    showPath = input("Input path for the folder for {}:\n".format(showKeywords) +
                     "Example: C:\\videos\\x files\n").strip()
    if not os.path.exists(showPath):
        os.makedirs(showPath)
        print("Directory did not exist. Created directory: '{}'".format(showPath))
    print("Move '{}' shows to directory: '{}'".format(showKeywords, showPath))
    data[showKeywords] = showPath
    save_json()

# Allows the user to view list of directories and delete one if necessary
def remove_directory():
    count = 1
    # Creates a dict to map user selection numbers to keys of the data dict
    deleteDict = {}
    print('\n')
    for key in data.keys():
        print("{}. {} --> {}".format(count, key, data[key]))
        deleteDict[count] = key
        count += 1
    print("{}. Cancel".format(count))
    selection = input("Select the number of the directory you want to delete:\n").strip()
    while (not selection.isdigit()) or (int(selection) not in deleteDict.keys()) and \
            (int(selection) != count):
        selection = input("Invalid selection. Select the number of the directory you want " +
                          "to delete:\n").strip()
    selection = int(selection)
    if selection != count:
        print("{} is being deleted".format(deleteDict[selection]))
        del data[deleteDict[selection]]
    save_json()

# Main menu to prompt the user for their chosen operation, or to quit
def prompt():
    inpt = input("\nSelect the number of the operation you wish to complete:\n" +
                 "1. Run file mover\n2. Add directories" +
                 "\n3. Remove directory\n4. Quit\n").strip()
    while inpt not in ['1','2','3','4']:
        inpt = input("\nInvalid. Please select the number of the operation you wish " +
                     "to complete:\n" +
                     "1. Run file mover\n2. Add directories" +
                     "\n3. Remove directory\n4. Quit\n").strip()
    return inpt

# Saves the data dict to a JSON file for future use
def save_json():
    with open(cwd + '\\data.json', 'w') as f:
        json.dump(data, f)

# Loads dictionary of show keywords and directories from JSON data file if it exists
# Prints loaded data
data = {}
cwd = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(cwd + '\\data.json'):
    with open(cwd + '\\data.json', 'r') as f:
         data = json.load(f)
    print("Loaded data:")
    for key in data.keys():
        print("{} --> {}".format(key, data[key]))
        
# Main menu: loops until user quits
while True:
    inpt = prompt()
    if inpt == '1':
        move_files()
    if inpt == '2':
        add_directory()
    if inpt == '3':
        remove_directory()
    if inpt == '4':
        print("Directory data saved. Exiting the program")
        break
    
