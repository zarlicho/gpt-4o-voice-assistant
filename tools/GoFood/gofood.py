from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium import webdriver
from colorama import Fore, init
import json, os, time, requests
import store
import re

class Gofud:
    def __init__(self):
        init()
        option = uc.ChromeOptions() 
        option.add_argument("--auto-open-devtools-for-tabs")
        option.add_argument(r"--user-data-dir=C:\chromeprofile")
        option.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.driver = uc.Chrome(options=option, desired_capabilities=caps, use_subprocess=True)
        self.driver.set_page_load_timeout(30)
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 30)
        self.req = requests.Session()
        self.Menu = store.Menu()
        self.StoreList = []
        self.AllFood = []
        

    def Setup(self):
        print(Fore.BLUE + 'Setup started')
        try:
            self.driver.get("https://gofood.co.id/login")
        except Exception as e:
            print(Fore.RED + str(e))

    def Login(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-card']/button[1]"))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-card']/form/div/div/div[2]/div[1]/input"))).send_keys("085771014979")
            self.actions.send_keys(Keys.ENTER)
            otpcode = input("masukan kode otp disini: ")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='otp']"))).send_keys(otpcode)
            self.actions.send_keys(Keys.ENTER)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='location-picker']"))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div/ul/li/div"))).click()
            time.sleep(2)
            myLocation = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[1]/div/a")))
            self.driver.get(myLocation.get_attribute('href'))
            time.sleep(2)
            self.driver.get("https://gofood.co.id/search?q=nasi goreng")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            logs = self.driver.get_log('performance')
            log_file_path = os.path.join(os.getcwd(), 'entity', 'network_log1.json')
            with open(log_file_path, "w", encoding="utf-8") as f: 
                f.write("[") 
                for log in logs: 
                    network_log = json.loads(log["message"])["message"] 
                    f.write(json.dumps(network_log)+",") 
                f.write("]") 
                print("Logs saved!")
            time.sleep(50)
        except Exception as e:
            print(Fore.RED + str(e))
            print(Fore.RED + "Browser automatically shutting down!")
            self.driver.quit()

    def GetStore(self, FoodName):
        allStore = self.Menu.GetStore(FoodName)
        self.StoreList = allStore
        print(self.StoreList)
        with open("./document/store.json", "w") as f:
            json.dump(allStore, f)
        return self.StoreList

    def GetAllMenu(self, StoreName):
        try:
            search = self.Menu.SearchStore(query=StoreName)
            print(self.StoreList)
            StoreLink = self.StoreList[search[0]]['link']
            print(search)
            self.driver.get(StoreLink)
            self.driver.refresh()
            FoodMenu = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[2]//div")))
            for index, food in enumerate(FoodMenu):
                try:
                    food_id = food.get_dom_attribute("id")
                    if food_id:  # Only process if `id` is not None or empty
                        section = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//*[@id='{food_id}']/div/div")))
                        for index, sections in enumerate(section):
                            FoodCard = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//*[@id='{food_id}']/div/div[{index+1}]")))
                            for Fcard in FoodCard:
                                if "Habis" not in Fcard.text:
                                    Fname = Fcard.find_element(By.TAG_NAME, "h3").text   
                                    Fprice = Fcard.find_element(By.TAG_NAME, "span").text
                                    menuDict = {
                                        "name": Fname,
                                        "price": Fprice,
                                        "foodId": food_id,
                                        "index": index+1
                                    }
                                    self.AllFood.append(menuDict)
                except Exception as e:
                    print(e)
            with open("./document/menu.json", "w") as f:
                json.dump(self.AllFood, f)
            print(self.AllFood)
            return self.AllFood
        except Exception as e:
            return f"something wrong while Getting all menu! the error is: {str(e)}"

    def Order(self, MenuName):
        orderFood = []
        pattern = re.compile(MenuName, re.IGNORECASE)
        for food in self.AllFood:
            orderFood.append(food['name'])
        print(orderFood)
        for index, food in enumerate(orderFood):
            if pattern.search(food):
                print(self.AllFood[index])
                foodid = self.AllFood[index]["foodId"]
                Findex = self.AllFood[index]["index"]
                FoodCard = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//*[@id='{foodid}']/div/div[{Findex}]")))
                for Fcard in FoodCard:
                    if "Habis" not in Fcard.text:
                        if "Catatan" not in Fcard.text:
                            Fcard.find_element(By.TAG_NAME, "button").click()
                        else:
                            # self.wait.until(EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[2]/div/div[4]/div/div")))[0].click()
                            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, f"/html/body/div[3]/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/a")))[0].click()
                            time.sleep(10)
                            
        time.sleep(6)
        return "Your food order was successful!"

# Contoh pemakaian
# if __name__ == "__main__":
# gofud = Gofud()
# # gofud.Setup()
# # gofud.Login()
# gofud.GetStore("nasi goreng")
# gofud.GetAllMenu("Nasi Goreng Fajar Harapan Maju")
# gofud.Order("Mie Goreng Ayam Baso")
