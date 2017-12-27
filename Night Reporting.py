from selenium import webdriver as driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

# Calls Driver and Opens Google Chrome
browser = driver.Chrome('C:\\Users\\na\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe')
browser.get(r"https://accounts.iqmetrix.net/Account/Login?returnUrl=https%3a%2f%2faccounts.iqmetrix.net%3a443%2fv1%2foauth2%2fauth%3fresponse_type%3dtoken%26client_id%3dAuthCode%26redirect_uri%3dhttps%253a%252f%252fmyrq1.iqmetrix.net%26approval_prompt%3dauto")

# Login to iQ Metrix website
browser.find_element_by_name("UserName").send_keys(
    "USERNAME@springcommunications")
browser.find_element_by_name("Password").send_keys("PASSWORD")
browser.find_element_by_name("Submit").click()


wait = WebDriverWait(browser, 100)
wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="nav-region"]/div/nav/div/div[2]/ul[1]/li[3]/a')))


# Navigate to correct page for report
browser.find_element_by_xpath(
    '//*[@id="nav-region"]/div/nav/div/div[2]/ul[1]/li[3]/a').click()

# Click on Perfomance Metrix
wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="main-region"]/div/div/div/div/div[3]/div[4]/a')))
browser.find_element_by_xpath(
    '//*[@id="main-region"]/div/div/div/div/div[3]/div[4]/a').click()

# Click for drop down menu
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-region"]/div/div[1]/div[2]/div/div[3]/div/div/div/div/select/option[text()="Quantity"]')))
browser.find_element_by_xpath('//*[@id="main-region"]/div/div[1]/div[2]/div/div[3]/div/div/div/div/select/option[text()="Quantity"]').click()

# Wait for store to load before clicking submit
wait.until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="s2id_autogen4"]/a/span[1]')))

# Click of the Submit buttong
browser.find_element_by_xpath(
    '//*[@id="main-region"]/div/div[1]/div[2]/div/div[4]/div/input').click()


# Wait for Tables to Load on Page
wait.until(EC.visibility_of_all_elements_located(
    (By.CLASS_NAME, 'results-count')))

# Turn off extra columns
browser.find_element_by_id("columns-button").click()  # Columns button
browser.find_element_by_id("data-2").click()  # OFF Quantity to Date Column
browser.find_element_by_id("data-3").click()  # OFF Quantity % of Target Column
browser.find_element_by_id("data-4").click()  # OFF Trending Column


# Top table
gpTable = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody')

# Bottom Table
reportTable = browser.find_element_by_xpath(
    '//*[@id="DataTables_Table_1"]/tbody')

# Creating a text file with complete report
report = open("report.text", "w")
report.write(gpTable.text)
report.write('\n')
report.write(reportTable.text)
report.close()

# Parse info to paste on groupME nightly Report
rExtract = open('report.text') # File that has all info

# File with only info that will be posted on groupMe
fWrite = open('final.text', 'w')

# List of what needs to be reported on
lines = ['Profit incl.', 'OPPS + WIRED', 'GROSS ADDS',
         'Postpaid Voice', 'CRU Postpaid Voice', 'Prepaid', 'ENTERTAINMENT',
         'DirecTV', 'DirecTV Now', 'UVerse TV', 'Broadband', 'SSW',
         'Tablet Data', 'TOTAL PROTECTED', 'ACCESSORIES', 'Acc Elig Opps']

# placer to go through list in loop
i = 0

# file that we writing final report too

fWrite.write('870 Hialeah Palm \n')  # First line of report
fWrite.write('***********************\n')  # Seperator
for rContents in rExtract.readlines():  # will parse all lines from file
    if i < len(lines):  # This will go through list in the report
        if lines[i] in rContents:
            fWrite.write(rContents)
            i += 1
rExtract.close()
fWrite.close()

# Login to groupMe
browser.get(r'https://web.groupme.com/signin') # Web address
browser.find_element_by_id('signinUserNameInput').send_keys("Username") # Username
browser.find_element_by_id("signinPasswordInput").send_keys("PASSWORD") # Password
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin"]/div/form/button')))
browser.find_element_by_xpath('//*[@id="signin"]/div/form/button').click()

# link to chat where to post
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tray"]/div[3]/div[1]/button[1]/div/div[2]/div/h4/div[1]/span')))
browser.find_element_by_xpath('//*[@id="tray"]/div[3]/div[1]/button[1]/div/div[2]/div/h4/div[1]/span').click()

cReport = open('final.text')
copy = cReport.read()
pyperclip.copy(copy)
cReport.close()

# Click on chat box and hits ENTER
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="chats"]/div/div[3]/div/div[2]/div/div[1]/div[1]/div')))
browser.find_element_by_xpath('//*[@id="chats"]/div/div[3]/div/div[2]/div/div[1]/div[1]/div').send_keys(pyperclip.paste())
#browser.find_element_by_xpath('//*[@id="chats"]/div/div[3]/div/div[2]/div/div[1]/div[1]/div').send_keys(Keys.RETURN)
