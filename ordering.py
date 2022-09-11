import email
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import os
from twilio.rest import Client
import sys
import random

def callMyselfToNotify(phoneNum):
    
    twilioInfoFile = open("twilioCred.txt", "r")
    twilioLines=twilioInfoFile.readlines()
    accountSID, authToken, twiPhoneNum = twilioLines[0], twilioLines[1], twilioLines[2]
    
    client = Client(accountSID, authToken)
    
    call = client.calls.create(
        to = phoneNum,
        from_ = twiPhoneNum,
        twiml='<Response><Say> The stuff is ready and getting prepared!</Say></Response>'
        )

def fullPurchase(driver):
    
    userInfoFile = open("userInfo.txt", "r")
    userLines=userInfoFile.readlines()
    phoneNum, fName = str(userLines[0]), str(userLines[1]) 
    lName, address = str(userLines[2]), str(userLines[3])
    postal, prov = str(userLines[4]), str(userLines[5])
    city, email = str(userLines[6]), str(userLines[7])

    credInfoFile = open("credInfo.txt", "r")
    credLines = credInfoFile.readlines()
    ccNum, secNum, expiry = str(credLines[0]), str(credLines[1]), str(credLines[2])

    #clicks add to cart
    driver.find_element_by_xpath("//button[contains(text(), 'Add to cart')]").click()
    time.sleep(3)
    
    #Selects the province in a dropdown menu
    province = Select(driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[2]/div/div[1]/form/section/div[2]/div[1]/p[2]/span/select'))
    province.select_by_visible_text(prov)
    #Enters postal code into 
    postalCode = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[2]/div/div[1]/form/section/div[2]/div[2]/p[2]/input')
    postalCode.send_keys(postal)
    time.sleep(1)
    
    #Hits update totals to move into shipping choices
    driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[2]/div/div[1]/form/section/div[2]/button').click()
    callMyselfToNotify(phoneNum)
    time.sleep(5)
    
    #Changes to calgary flat curbside delivery for flat 50$ fee
    driver.find_element_by_id('shipping_method_0_flat_rate57').click()
    time.sleep(1.25)
    
    #Proceeds to checkout after changing shipping method
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div[1]/div[3]/div[1]/div[3]/div[2]/div[2]/div/a[2]').click()
    time.sleep(5)
    
    #Filling in all the forms
    for item in email: driver.find_element_by_xpath("//input[@type='email']").send_keys(item) #Email
    for item in phoneNum: driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[1]/div/p[2]/span/input').send_keys(item) #PhoneNum
    for item in fName: driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[1]/div/p[3]/span/input').send_keys(item) #First Name
    for item in lName: driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[1]/div/p[4]/span/input').send_keys(item) # Last Name
    for item in address: driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[1]/div/p[5]/span/input').send_keys(item) #Address
    for item in city: driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[1]/div/p[7]/span/input').send_keys(item) # City
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[2]/div/div[2]/span').click()
    time.sleep(4)
            
    #iframe for a single html item
    
    driver.switch_to_frame(driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[5]/div/ul/div[1]/div/div/div[5]/fieldset/div[1]/div/div/div/iframe"))
    
    for item in ccNum: driver.find_element_by_xpath('/html/body/div/form/span[2]/div/div[2]/span/input').send_keys(item)
        
    driver.switch_to.default_content()
    driver.switch_to_frame(driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[5]/div/ul/div[1]/div/div/div[5]/fieldset/div[2]/div/div/iframe'))
    
    for item in expiry: driver.find_element_by_xpath('/html/body/div/form/span[2]/span/input').send_keys(item)
        
    driver.switch_to.default_content()
    driver.switch_to_frame(driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[1]/div[5]/div/ul/div[1]/div/div/div[5]/fieldset/div[3]/div/div/iframe'))
    
    for item in secNum: driver.find_element_by_xpath('/html/body/div/form/span[2]/span/input').send_keys(item)
            
    driver.switch_to.default_content()
            
    #Place the order
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/section/div/div/div/div/div/div/div[1]/div/form[3]/div[2]/div/div[2]/div/div[2]/button').click()
    time.sleep(30)
    driver.stop_client()
    driver.quit()
    os.remove("var.txt")
    f = open("var.txt", "w")
    f.write("1")
    f.close()

def whilstLoop(URI):
    options = webdriver.Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--window-size=200,200")
    #Gets the page open
    driver = webdriver.Chrome(executable_path = "chromedriver", chrome_options = options)
    driver.get(URI)
    time.sleep(4)
    
    while True:
        f = open("var.txt", "r")
        if "1" not in f.read(): # If the system has updated to purchased, stops attempting to purchase
            f.close()
            try:
                fullPurchase(driver)
                break
            except:
                time.sleep(random.randint(0,2))
                driver.refresh()
        else:
            f.close()
            break

if __name__ == "__main__":

    whilstLoop(str(sys.argv[-1]))