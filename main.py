import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import sys
from datetime import timedelta, date
import re

def userInfo():
    myEmail = "pant.naman2001@gmail.com"
    myPassword = ".xvGvQ#D5vhW!kZ"


    username = driver.find_element(By.ID,"handleOrEmail")
    username.send_keys(myEmail)

    password = driver.find_element(By.ID, "password")
    password.send_keys(myPassword)

    # driver.find_element(By.XPATH,'//*[@id="remember"]').click()
    time.sleep(2)

    login()

def login():
    try:
        loginButton = driver.find_element(By.XPATH,'//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input')
        driver.execute_script("arguments[0].click();", loginButton)
    except Exception as err:
        with open('logs.txt', 'a') as logFile:
            logFile.write('Unable to log in, invalid credentials\n')

    print("Logged in")

    time.sleep(5)
    userDivs = userDiv()
    chooseContests(userDivs) 

def userDiv():
    try:
        userRating = driver.find_element(By.XPATH,'//span[@class="user-green"]')
        userRating = int(userRating.text)
        userDiv = 0
        if(userRating < 1400):
            userDiv = 4
        elif(userRating < 1600):
            userDiv = 3
        elif(userRating < 1900):
            userDiv = 2
        else:
            userDiv = 1
        # print(f"User divison calculated {userDiv}")
        return userDiv
    except Exception as err:
        with open('logs.txt', 'a') as log_file:
            log_file.writelines("Unable to fetch rating\n")
        raise err

def chooseContests(userDiv):
    
    # Go to contest page
    try:
        contestButton = driver.find_element(By.XPATH, '//a[@href="/contests"]')
        contestButton.click()
        time.sleep(5)
    except Exception as err:
        with open('logs.txt', 'a') as logFile:
            logFile.write('Unable to access contest page\n')
            print(str(err))

     # Access the Contest Table element
    try:
        contestTable = driver.find_element(By.XPATH, '//*[@id="pageContent"]/div[1]/div[1]')
        contestList = contestTable.find_elements(By.TAG_NAME, "tr")[1:]

        global validContestCount
        global registeredContestCount
        validContestCount = 0
        registeredContestCount = 0

        # Iterating every row of the table
        for row in contestList:
            try:
                contestName = row.find_elements(By.TAG_NAME, "td")
                contestName = contestName[0].text

                # regex to find Contest division
                contestDiv = [int (x) for x in re.findall(r"\. (.{1})", contestName)]
                # print(contestName, " ", contestDiv, " ", userDiv)
                # for x in re.findall(r"\. (.{1})", contestName):
                #     print(x)
                if(len(contestDiv) == 0):
                    contestDiv = 5
                else:
                    contestDiv = min(contestDiv)

                if (contestDiv <= userDiv):
                    registerLink = row.find_element(By.XPATH, '//a[@class="red-link"]')
                    validContestCount += 1
                    registeredContestCount += registerLink.click()
                    time.sleep(5)
                    register()
            except Exception as err:
                with open('logs.txt', 'a') as log_file:
                    log_file.writelines('Not eligible to register or Registration not opened yet\n')
                continue

        # All valid registration completed
        if (validContestCount == registeredContestCount):
            print("Done")
        else:
            print("Incomplete")

    except Exception as err:
        with open('logs.txt', 'a') as log_file:
            log_file.writelines('Table not accesible\n')
    time.sleep(5)

def register():
    try:
        registerButton = driver.find_element(By.CLASS_NAME, 'submit')
        registerButton.click()
        return 1
    except :
        with open('logs.txt', 'a') as log_file:
            log_file.writelines('Not able to register')
    time.sleep(5)
    return 0

if __name__ == '__main__':
    try:
        # Load chrome
        driver = webdriver.Chrome()
        driver.get("https://codeforces.com/")
    
        enterButton = driver.find_element(By.XPATH, '//*[@id="header"]/div[2]/div[2]/a[1]')

        # Enter login page if user is not logged in
        if enterButton.text == 'Enter':
            driver.execute_script("arguments[0].click();", enterButton)
            time.sleep(5)
            userInfo()
        else:
            with open('logs.txt', 'a') as log_file:
                log_file.write(f"User {enterButton.text} is already logged in.\n")
            chooseContests()
    except Exception as err:
        with open('logs.txt', 'a') as log_file:
            log_file.write('Site not working. Try later\n')
        raise err
        
    # driver.quit()
    driver.close()
    driver.quit()

