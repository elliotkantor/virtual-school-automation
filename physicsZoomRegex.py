#! python3
# from zoomAutomation import sign_in
# scrapes schoology, finds today's info, logs in at proper time
import re
import pyperclip
import pandas as pd

# scrape schoology


# extract today's info
input("Press enter to read clipboard. ")
text = pyperclip.paste()

idRegex = re.compile(r'(\d{3}\s?\d{4}\s?\d{4})')
passRegex = re.compile(r'(\S*)$')
id = idRegex.search(text).group()
passcode = passRegex.search(text).group()

print(id)
print(passcode)
# change csv
file = pd.read_csv('timings.csv')
file.iloc[0,1] = id
file.iloc[0,2] = passcode
file.to_csv('timings.csv', index=False)

# log in
# sign_in(id, passcode)
