#! python3
# changeMeeting.py - allows changing .csv without going into it

import re
import pandas as pd

file = pd.read_csv('timings.csv')
def showAndChange(type):
    if type == 0:
        name = 'time'
    elif type == 1:
        name = 'meeting ID'
    elif type == 2:
        name = 'password'
    else:
        raise Exception("Must call function with 0, 1, or 2")
    # new = input("Current " + name + ": " + file.iloc[0,type] + ' ')
    mo = None
    if type == 0:
        isValid = re.compile(r'\d\d:\d\d')
    elif type == 1:
        isValid = re.compile(r'\d{3}\s?\d{4}\s?\d{4}')
    elif type == 2:
        isValid = re.compile(r'[0-9a-zA-z]+')
    while mo == None:
        new = input("Current " + name + ": " + str(file.iloc[0,type]) + ' ')
        if new != '':
            if new == 'delete' or new == 'remove':
                confirmInput = input("Do you really want to delete all entries?").lower()
                if confirmInput.startswith('y'):
                    for i in (0,1,2):
                        file.iloc[0,i] = None
            else:
                mo = isValid.search(new)
                new = mo.group()
                file.iloc[0,type] = new
                print(file.iloc[0,type])
        else:
            break

# shows current time. if entered, change to new time
showAndChange(0)
# change code
showAndChange(1)
# change password
showAndChange(2)
# saves over file
file.to_csv('timings.csv', index=False)
print('Saved.')
