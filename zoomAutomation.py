#! python3
# zoomAutomation.py - Opens zoom and logs in with ID and password based on CSV sheet
import subprocess, pyautogui, time, sys
import pandas as pd
from datetime import datetime

pyautogui.FAILSAFE = True

def isRetina():
    if subprocess.call("system_profiler SPDisplaysDataType | grep 'Retina'", shell=True, stdout=subprocess.DEVNULL) == 0:
        retinaScreen = True
    else:
        retinaScreen = False
    return retinaScreen

dayOfWeek = datetime.now().strftime('%A') # returns string Friday
def isWednesday():
    global dayOfWeek
    if dayOfWeek == 'Wednesday':
        return True
    else:
        return False
def isWeekday():
    global dayOfWeek
    if dayOfWeek not in ['Saturday','Sunday']:
        return True
    else:
        return False

def sign_in(meetingid, pswd):
    # opens Zoom
    subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"])
    print("Opened Zoom\n")
    time.sleep(3)

    # click join
    join_butn = pyautogui.locateCenterOnScreen('join_btn.png')
    if retinaScreen:
        join_butn = (join_butn.x / 2, join_butn.y / 2)
    pyautogui.moveTo(join_butn, duration=1)
    pyautogui.click()
    # print('join')

    # enter meeting id
    pyautogui.write(meetingid)
    pyautogui.press('enter')
    time.sleep(2)

    # enter password
    pyautogui.write(pswd)
    pyautogui.press('enter')

# reading the file
def start():
    global isWeekday
    continueOnWeekend = False
    df = pd.read_csv('timings.csv')
    print("Checking time and meetings...\n")

    while True:
        if not isWeekday() and not continueOnWeekend:
            choice = input("It is a weekend. Continue anyway? (y/n) ").strip().lower()
            if not choice.startswith('y'):
                print("Ending program...\n")
                break
            else:
                continueOnWeekend = True
                print("Continuing...\n")
                # implied continue

        # check if current time in csv
        now = datetime.now().strftime("%H:%M")
        if now in str(df['timings']):
            # find the proper row with the right time
            row = df.loc[df['timings'] == now]
            m_id = str(row.iloc[0,1])
            m_pswd = str(row.iloc[0,2])

            sign_in(m_id, m_pswd)
            print("Signed in!")
            break
        time.sleep(15)

if __name__ == '__main__':
    start()
