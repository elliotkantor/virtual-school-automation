#! python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, re, os
import pandas as pd
from datetime import datetime
import zoomAutomation

browser = webdriver.Firefox()
# make it wait up to 15 seconds before throwing error
browser.implicitly_wait(15)

def openSchoology():
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
    teacherNamesElems = browser.find_elements_by_xpath('//*[@title="View user profile."]')
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

    print(f'{physics_zoom_id = }')
    print(f'{physics_zoom_passcode = }\n')

def changeMeeting(time, id, passcode):
    file = pd.read_csv('timings.csv')
    file.iloc[0,1] = id
    file.iloc[0,2] = passcode
    file.iloc[0,0] = time
    file.to_csv('timings.csv', index=False)
    print("Updated timings.csv\n")

def start():
    global physics_zoom_id
    global physics_zoom_passcode

    # set time of physics class
    if zoomAutomation.isWednesday():
        # early release
        physics_time = '11:42'
    else:
        physics_time = '12:32'

    openSchoology()
    scrapePhysics() # get physics info
    browser.close()
    changeMeeting(physics_time, physics_zoom_id, physics_zoom_passcode) # change csv
    zoomAutomation.start() # check for meetings
    print('Done')

if __name__ == '__main__':
    start()
