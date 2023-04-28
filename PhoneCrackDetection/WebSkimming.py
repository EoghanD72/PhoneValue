# import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# create a chrome webdriver
driver = webdriver.Chrome()

# imports keys which is used to send input
from selenium.webdriver.common.keys import Keys

# opens ebay through the driver
driver.get("https://www.ebay.ie/")
# inspect the search box to find its name attribute "_nkw"
search_box = driver.find_element(By.NAME, "_nkw")
# fills the seachbox with the string term given
search_box.send_keys("galaxy s21 fair")
# keys.RETURN sends the enter key
search_box.send_keys(Keys.RETURN)

# create a set of keywords to exclude
exclude_keywords = {'case', 'empty', 'replacement', 'microphone', 'camera', 'accessory', 'cover', 'dummy', 'fake', 'otter', 'battery', 'dummies', 'screen'}

# Importing BeautifulSoup to navigate HTML
from bs4 import BeautifulSoup

# passes the html source code of the webpage
soup = BeautifulSoup(driver.page_source, "html.parser")
# finds all the elements given the "s-item" class
listings = soup.find_all("li", {"class": "s-item"})

price_list = []

# looks through all the listings found and extracts name and price then prints
for listing in listings:
    # name = listing.find("div", {"class": "s-item__title"}).text.strip() # text.strip() removes leading/tailing whitespace
    # if not any(keyword in name.lower() for keyword in exclude_keywords):
    #     price = listing.find("span", {"class": "s-item__price"}).text.strip()
    #     print(name, "\n", price)
    try:
        name = listing.find("div", {"class": "s-item__title"}).text.strip()
        if not any(keyword in name.lower() for keyword in exclude_keywords):
            price = listing.find("span", {"class": "s-item__price"}).text.strip()
            price = float(price.replace("EUR", ""))
            if price > 25.0:
                price_list.append(price)
            condition = listing.find("span", {"class": "SECONDARY_INFO"}).text.strip()
            print(name, "\n", price, "\n", condition, "\n")
    except:
        continue
price_list = [float(x) for x in price_list]
print(price_list)

average = sum(price_list) / len(price_list)
print("average ", average)
# closes driver
driver.quit()
