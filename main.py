#! python3
# main.py - interactively controls virtual school
import pandas as pd
from datetime import datetime
import time
import subprocess
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import os

time_df = pd.read_csv('timings.csv')
dayOfWeek = datetime.now().strftime('%A')  # returns string Friday
pyautogui.FAILSAFE = True
classIndexes = {
    'physics': 0,
    'economics': 1
}
continueOnWeekend = False


def openSchoology():
    global browser
    browser = webdriver.Firefox()
    # make it wait up to 15 seconds before throwing error
    browser.implicitly_wait(15)
    # /~ nano .zprofile for environment variables (below)
    school_username = os.environ.get('SCHOOLOGY_ID')
    school_password = os.environ.get('SCHOOLOGY_PASS')

    browser.get('https://stjohnsschools.schoology.com')
    emailElem = browser.find_element_by_xpath('//*[@id="i0116"]')
    emailElem.send_keys(school_username)
    time.sleep(1)
    emailElem.send_keys(Keys.ENTER)

    passwordElem = browser.find_element_by_xpath('//*[@id="passwordInput"]')
    passwordElem.send_keys(school_password)
    signInElem = browser.find_element_by_xpath('//*[@id="submitButton"]')
    signInElem.click()
    stayInElem = browser.find_element_by_xpath('//*[@id="idSIButton9"]')
    stayInElem.click()

    print("Opened Schoology home page...\n")


def scrapePhysics():
    global physics_zoom_id
    global physics_zoom_passcode
    teacherIndex = 0
    teacherNamesElems = browser.find_elements_by_xpath(
        '//*[@title="View user profile."]')
    physicsText = ''
    for teacher in teacherNamesElems:
        if teacher.text == 'Martin Hillier':
            bodyTextElems = browser.find_elements_by_class_name('edge-item')
            bodyText = bodyTextElems[teacherIndex]
            physicsText += bodyText.text
            # print(bodyText.text)
        teacherIndex += 1
    idRegex = re.compile(r'(\d{3}\s?\d{4}\s?\d{4})')
    passRegex = re.compile(r'passcode: (\S*)')
    try:
        physics_zoom_id = idRegex.search(physicsText).group()
        physics_zoom_passcode = passRegex.search(physicsText).group(1)
    except:
        print("Could not get zoom info.")
        physics_zoom_id, physics_zoom_passcode = 'id', 'passcode'

    print(f'Physics zoom ID: {physics_zoom_id}')
    print(f'Physics zoom passcode: {physics_zoom_passcode}\n')

    changeMeeting(physics_zoom_id, physics_zoom_passcode, 'physics')  # change csv


def economics_login():
    # click groups
    groupsElem = browser.find_element_by_xpath(
        '/html/body/div[1]/div[1]/header/nav/ul[1]/li[3]/div/button/span')
    groupsElem.click()

    # click econ
    econGroupElem = browser.find_element_by_xpath(
        '/html/body/div[1]/div[1]/header/nav/ul[1]/li[3]/div/div/div/div/div[3]/div[1]/article')
    econGroupElem.click()

    conferencesElem = browser.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div/div[1]/a/span')
    conferencesElem.click()

    attempts = 0
    override = False
    while True:
        if attempts > 10 and not override:
            choice = input(
                "You've tried more than 10 times. Continue? (y/n) ").strip().lower()
            if choice.startswith('y'):
                override = True
                print("Continuing...\n")
            else:
                print("Ending...\n")
                break
        try:
            # joinElem = browser.find_element_by_class_name('ng-binding')
            # joinElem.click()
            browser.find_element_by_xpath(
                '/html/body/div/div[4]/table/tbody/tr[2]/td[1]').click()
            break
        except:
            attempts += 1
            time.sleep(15)
            browser.refresh()
    # click headphones and type 'good afternoon'
    browser.find_element_by_xpath('icon--2q1XXw icon-bbb-listen').click()
    textBox = browser.find_element_by_id('message-input')
    textBox.send_keys('good afternoon')
    textBox.send_keys(Keys.RETURN)


def changeMeeting(id='', passcode='', course='physics'):
    global time_df
    # time_df.iloc[classIndexes[course], 0] = time
    time_df.iloc[classIndexes[course], 1] = id
    time_df.iloc[classIndexes[course], 2] = passcode
    time_df.to_csv('timings.csv', index=False)
    print("Updated timings.csv\n")


def isRetina():
    if subprocess.call("system_profiler SPDisplaysDataType | grep 'Retina'", shell=True, stdout=subprocess.DEVNULL) == 0:
        retinaScreen = True
    else:
        retinaScreen = False
    return retinaScreen


def isWednesday():
    global dayOfWeek
    if dayOfWeek == 'Wednesday':
        return True
    else:
        return False


def isWeekday():
    global dayOfWeek
    if dayOfWeek not in ['Saturday', 'Sunday']:
        return True
    else:
        return False


def zoom_sign_in(meetingid, pswd):
    # opens Zoom
    subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"])
    print("Opened Zoom\n")
    time.sleep(3)

    # click join
    join_butn = pyautogui.locateCenterOnScreen('join_btn.png')
    if isRetina():
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
    time.sleep(.2)
    pyautogui.press('enter')


def get_zoom_info(classname):
    global browser
    if classname == 'physics':
        openSchoology()
        scrapePhysics()  # get physics info and adds to csv
        browser.close()


while True:
    # checks if weekend
    if not isWeekday() and not continueOnWeekend:
        choice = input(
            "It is a weekend. Continue anyway? (y/n) ").strip().lower()
        if not choice.startswith('y'):
            print("Ending program...\n")
            break
        else:
            continueOnWeekend = True
            print("Continuing...\n")
            # implied continue

    # check if current time in csv
    now = datetime.now().strftime("%H:%M")
    if (now in str(time_df['timings']) and not isWednesday()) or (now in str(time_df['wedtime']) and isWednesday()):
        # find the proper row index with the right time
        if not isWednesday():
            current_row_index = time_df.loc[time_df['timings'] == now].index.values.astype('int')[
                0]
        else:
            current_row_index = time_df.loc[time_df['wedtime'] == now].index.values.astype('int')[
                0]
        # current_row_index could be 0, 1, 2, etc
        current_type = time_df.loc[current_row_index, 'type']  # ie zoom
        current_class = time_df.loc[current_row_index, 'classname']  # ie physics

        if current_type == 'zoom':
            # gets zoom ID and password with webscraping
            get_zoom_info(current_class)
            zoomID = time_df.loc[current_row_index, 'meetingid']
            zoomPass = time_df.loc[current_row_index, 'meetingpswd']

            zoom_sign_in(zoomID, zoomPass)
            print("Signed in to " + current_class)
            time.sleep(45)
        elif current_type == 'schoology':
            # Open with schoology conferences
            openSchoology()
            if current_class == 'economics':
                economics_login()
            elif current_class == 'gov':
                pass
            elif current_class == 'computer':
                pass
            elif current_class == 'lit':
                pass
            else:
                print(current_class + " is not a valid class.")
        elif current_type == 'zoomEmbed':
            print("Should open with zoom from schoology")
            pass
        else:
            print(f"Did not recognize {current_type} as a type.")

    time.sleep(15)
