from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
url = "https://app.ahrefs.com/batch-analysis"
email = "hoibeokkk@rattlenhumbarnyc.com"
password = "teamasm10k"

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "D:\Domain Checking\Ahrefs-auto-check-domains-tool\src\DataAnalysis\data"}
options.add_experimental_option('prefs', prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH, options= options, service = Service(ChromeDriverManager().install()))
driver.get(url)

df = pd.read_csv("src/assets/input.csv", header = None)
df.columns = ["Domains"]

def check_domain():
    domains = []
    # Login
    try:  
        txtUser = driver.find_element(By.NAME, 'email')
        txtUser.clear()
        txtUser.send_keys(email)
    except:
        pass
    txtPass = driver.find_element(By.NAME, 'password')
    txtPass.clear()
    txtPass.send_keys(password)
    driver.find_element(By.XPATH,"//button[@type='submit']").click()

    # Get input domain and paste into the textbox
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter up to 200 URLs (one URL per line)']")))
    txtDomain = driver.find_element(By.XPATH, "//textarea[@placeholder='Enter up to 200 URLs (one URL per line)']")

    while len(df) != 0:
        for i in range(0, (len(df) // 200) + 1):
            for j in df["Domains"]:
            # Copy domain name
                pyperclip.copy(j)
                clipboard_text= pyperclip.paste()
                domains.append(clipboard_text)
                print(len(domains))
                if len(domains) < 201:
                # Paste domain name in batch analysis form
                    txtDomain.send_keys(clipboard_text)
                    txtDomain.send_keys(Keys.ENTER)
                    # Empty the clipboard text
                    clipboard_text = ""
                else:
                    break
            driver.find_element(By.XPATH,"//button[@id = 'startAnalysisButton']").click()
            time.sleep(20)
            # Export data
            driver.find_element(By.XPATH, "//a[@id = 'baExportButton']").click()
            time.sleep(10)
            driver.find_element(By.XPATH, "//button[@id = 'start_export_w_selected_charset']").click()
            time.sleep(10)
            txtDomain = driver.find_element(By.XPATH, "//textarea[@placeholder='Enter up to 200 URLs (one URL per line)']")
            txtDomain.clear()
            df.drop(index=df.index[:200], axis=0, inplace=True)
            domains = []
