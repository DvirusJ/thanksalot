import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from fake_useragent import UserAgent
ua = UserAgent()

length = 4
def generate_collisionavoider(length):
    characters = string.ascii_uppercase + string.digits
    collisionavoider = ''.join(random.choice(characters) for _ in range(length))
    return collisionavoider

if __name__ == '__main__':
    file = open("info.txt", "r")
    fdata = file.readlines()
    countfile = open("counter.txt", "r")
    counter = int(countfile.read().strip())
    countfile.close()
    fname = fdata[0].split("::")[1].strip()
    lname = fdata[1].split("::")[1].strip()
    password = fdata[4].split("::")[1].strip()
    phone = fdata[5].split("::")[1].strip()
    ticker = fdata[6].split("::")[1].strip()
    print("Loaded Credentials ")
    while True:
        try:
            ## print("Attempting to generate Email")
            collisionavoider = generate_collisionavoider(length)
            email = fdata[2].split("::")[1].strip() + str(counter) + collisionavoider +"@" + fdata[3].split("::")[1].strip()
            user_agent = ua.random
            options=webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument("--log-level=3")
            options.add_argument('--disable-gpu')
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            driver.get("https://secure.takealot.com/account/register")
            #time.sleep(1)
            print("------------------------ Account Registration Started ------------------------")
            print("Website Loaded Successfully")

            ## Accept Cookies
            cookies_xpath = "//*[@id='shopfront-app']/div[1]/div/div/button"

            ## Wait for 10 seconds for the cookies element to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cookies_xpath)))
            cookies_element = driver.find_element(by=By.XPATH, value=cookies_xpath)
            cookies_element.click()
            #time.sleep(0.1)
            ## First Name           
            first_name_xpath = "//*[@id='register_customer_first_name']"
            first_name_element = driver.find_element(by=By.XPATH, value=first_name_xpath)
            first_name_element.send_keys(fname)
            #time.sleep(0.1)
            ## Last Name
            last_name_xpath = "//*[@id='register_customer_last_name']"
            last_name_element = driver.find_element(by=By.XPATH, value=last_name_xpath)
            last_name_element.send_keys(lname)
            #time.sleep(0.1)
            ## Email
            email_xpath = "//*[@id='register_customer_email']"
            email_element = driver.find_element(by=By.XPATH, value=email_xpath)
            email_element.send_keys(email)
            #time.sleep(0.1)  
            ## Password
            password_xpath = "//*[@id='register_customer_new_password']"
            password_element = driver.find_element(by=By.XPATH, value=password_xpath)
            password_element.send_keys(password)
            #time.sleep(0.1)  
            ## Phone Number
            phone_xpath = "//*[@id='register_customer_mobile_national_number']"
            phone_element = driver.find_element(by=By.XPATH, value=phone_xpath)
            phone_element.send_keys(phone)
            #time.sleep(0.1)

            ## Locate the "Register" button using the data-testid attribute
            register_button_xpath = "//button[@class='button submit-action']"

            ## Find the "Register" button again and click it
            register_button = driver.find_element(By.XPATH, register_button_xpath)
            register_button.click()

            ## Confirmation
            confirm_xpath = "//a[.='Verify Mobile Number']"
            ## Wait for 10 seconds for the confirmation element to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, confirm_xpath)))
            if driver.find_element(by=By.XPATH, value=confirm_xpath):
                ## Increment counter
                counter += 1
                filee = open("counter.txt", "w")
                filee.write(str(counter))
                filee.close()

                print(f"""New Account Registered Successfully | {email}""")
                print("------------------------------------------------------------------------------\n")
                driver.quit()

            else:

                print("Failed to confirm account")
                print("------------------------------------------------------------------------------\n")
                driver.quit()

        except TimeoutException as te:
            print("Timeout Error: The cookies element was not found within 10 seconds. Reloading Client")
            driver.quit()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

