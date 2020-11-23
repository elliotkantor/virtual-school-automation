#! python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, re, os
import pandas as pd
from datetime import datetime
import zoomAutomation

# which row includes data for this class
classIndexes = {
    'physics': 0,
    'economics': 1
}

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

    print(f'Physics zoom ID: {physics_zoom_id}')
    print(f'Physics zoom passcode: {physics_zoom_passcode}\n')

class embedZoom:
    def __init__(self):
        openSchoology()
    def login():
        pass

class economicsLogin(embedZoom):
    def __init__(self):
        super().__init__(self)

    def login():
        # click groups
        groupsElem = browser.find_element_by_xpath('/html/body/div[1]/div[1]/header/nav/ul[1]/li[3]/div/button/span')
        groupsElem.click()

        # click econ
        econGroupElem = browser.find_element_by_xpath('/html/body/div[1]/div[1]/header/nav/ul[1]/li[3]/div/div/div/div/div[3]/div[1]/article')
        econGroupElem.click()

        conferencesElem = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div/div[1]/a/span')
        conferencesElem.click()
        attempts = 0
        override = False
        while True:
            if attempts > 10 and not override:
                choice = input("You've tried more than 10 times. Continue? (y/n) ").strip().lower()
                if choice.startswith('y'):
                    override = True
                    print("Continuing...\n")
                else:
                    print("Ending...\n")
                    break
            try:
                joinElem = browser.find_element_by_class_name('ng-binding')
                joinElem.click()
                break
            except:
                attempts += 1
                time.sleep(15)
                browser.refresh()
        # click headphones and type 'good afternoon'
        # browser.find_element_by_xpath('').click()
        # textBox = browser.find_element_by_xpath('')
        # textBox.send_keys('good afternoon')
        # textBox.send_keys(Keys.RETURN)

# ant-btn ant-table-span (class name for zoom join button schoology embed)

def changeMeeting(time, id='', passcode='', course='physics'):
    file = pd.read_csv('timings.csv')
    file.iloc[classIndexes[course], 0] = time
    file.iloc[classIndexes[course], 1] = id
    file.iloc[classIndexes[course], 2] = passcode
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
    changeMeeting(physics_time, physics_zoom_id, physics_zoom_passcode, 'physics') # change csv
    # zoomAutomation.start() # check for meetings
    # print('Done')

if __name__ == '__main__':
    start()
