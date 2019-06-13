from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yagmail

options = Options()
options.headless = True
driver = webdriver.Chrome("./chromedriver", chrome_options=options)

message = []

with open("items.csv") as f:
    for line in f.readlines():

        # Extract description, category and price range
        data = line.split(',')
        desc = data[0]
        category = data[1]
        low = float(data[2])
        high = float(data[3])

        # Use description to separate out each set of results
        message.append(desc)
        
        # Start at Craigslist homepage
        driver.get("https://newyork.craigslist.org/")
        
        # Go to specified category
        driver.find_element_by_link_text(category).click()
        query_field = driver.find_element_by_css_selector("#query")
        query_field.send_keys(desc)
        driver.find_element_by_css_selector(".icon-search").click()
   
        results = driver.find_elements_by_css_selector(".result-row")
        for result in results:
            raw_price = result.find_element_by_css_selector(".result-price").text
            price = float(raw_price.strip("$"))
            # Check price range
            if low < price and price < high:
                link = result.find_element_by_css_selector(".result-title").get_attribute("href")
                #Send link
                message.append(link)

# E-mail results                
yag = yagmail.SMTP('automatedalertbot', 'standingroomonly')
yag.send('robcarrington@gmail.com', 'subject', message)