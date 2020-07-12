
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
from datetime import date
from datetime import datetime


def get_all_values(index):
    delta = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(index) + "]/div/div[2]")
    strike = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(index) + "]/div/div[4]")
    iv = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(index) + "]/div/div[5]")
    theta = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(index) + "]/div/div[9]")
    premium = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(index) + "]/div/div[6]")
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(index, "Nifty--->  ", "delta:", delta.text, "strike:", strike.text, "iv:", iv.text, "theta:", theta.text, "premium:", premium.text, "today:", today, "current_time:", current_time)
    driver.close()
    sys.exit(0)


threshold = float(input("Enter cutt-off delta: "))
delta_list = []
threshold_found = False

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://web.sensibull.com/option-chain?expiry=2020-07-16&tradingsymbol=NIFTY")

popup_close = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[13]/div[3]/div/div/button")),
                        message="Close Popup"
                    )

popup_close.click()
print("Popup closed")

greek = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[2]/div[2]/label[2]/span[1]/span[1]/span[1]/input')

if not greek.is_selected():
    greek.click()
print("Geek mode selected")

for i in range(1, 61):
    delta = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(i) + "]/div/div[2]")
    try:
        delta_value = float(delta.text)
        delta_list.append(delta_value)
        if (delta_value == threshold):
            threshold_found = True
            index = i
            get_all_values(index)
    except ValueError:
        print("Not a float -> No Delta Value:", delta.text) 

if not threshold_found:
    min_diff = float('-inf')
    index = -1
    for i in range(len(delta_list)):
        diff = delta_list[i] - threshold
        if min_diff < diff and diff < 0:
            min_diff = diff;
            index = i
    delta = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[3]/div/div/div[3]/div[1]/div/div[1]/div[3]/div[" + str(index + 1) + "]/div/div[2]")
    get_all_values(index + 1)
