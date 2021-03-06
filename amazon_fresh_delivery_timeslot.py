import bs4
import getpass
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from twilio.rest import Client

# Amazon credentials
username = input('Amazon username: ')
password = getpass.getpass()
##username = 'username'
##password = 'password'

# Twilio configuration
##toNumber = 'to phone number'
##fromNumber = 'from phone number'
##accountSid = 'twilio sid'
##authToken = 'twilio token'
##client = Client(accountSid, authToken)

def timeSleep(x, driver):
    for i in range(x, -1, -1):
        sys.stdout.write('\r')
        sys.stdout.write('{:2d} seconds'.format(i))
        sys.stdout.flush()
        time.sleep(1)
    driver.refresh()
    sys.stdout.write('\r')
    sys.stdout.write('Page refreshed\n')
    sys.stdout.flush()

def createDriver():
    chromeOpts = webdriver.ChromeOptions()
    chromeOpts.add_argument('--incognito')
    chromeOpts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('chromedriver', options = chromeOpts)
    return driver

def driverWait(driver, findType, selector):
    while True:
        if findType == 'css':
            try: driver.find_element_by_css_selector(selector).click(); break
            except NoSuchElementException: driver.implicitly_wait(0.2)
        elif findType == 'name':
            try: driver.find_element_by_name(selector).click(); break
            except NoSuchElementException: driver.implicitly_wait(0.2)

def navigateToShipOptions(driver):
    driver.get('https://www.amazon.com/gp/sign-in.html')
    usernameField = driver.find_element_by_css_selector('#ap_email')
    usernameField.send_keys(username)
    driverWait(driver, 'css', '#continue')
    passwordField = driver.find_element_by_css_selector('#ap_password')
    passwordField.send_keys(password)
    driverWait(driver, 'css', '#signInSubmit')
    driver.get('https://www.amazon.com/alm/storefront?almBrandId=QW1hem9uIEZyZXNo')
    driverWait(driver, 'name', 'proceedToFreshCheckout')
    driverWait(driver, 'name', 'proceedToCheckout')

def findSlots(driver):
    while True:
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        try:
            findAllSlots = soup.find_all('div', class_ ='ufss-slot-price-container')
            for slot in findAllSlots:
                if 'Not Avaiable' in slot.get_text():
                    pass
                else:
                    try: client.messages.create(to = toNumber,from_ = fromNumber,body = 'SLOTS OPEN!')
                    except NameError: pass
                    print('SLOTS OPEN!')
                    for i in range(5):
                        print('\a')
                        time.sleep(1)
                    time.sleep(1800)
                    driver.quit()
                    return
        except AttributeError: pass
        timeSleep(60, driver)

if __name__ == '__main__':
    driver = createDriver()
    navigateToShipOptions(driver)
    findSlots(driver)
