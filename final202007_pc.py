from selenium import webdriver
from datetime import datetime
import yagmail

#You need to change the following to the location of your your automation
#folder.
direc = "C:/Users/n/Dropbox/nyccc_machine_learning_202007/automation/"
#You need to change the text part of the following to whatever your 
#chromedriver is named. (Side note, make sure the chromedriver is in your
#automation folder.
driver =  webdriver.Chrome(direc+"chromedriver.exe")

results = []
res_txt = ''

# For each line in items.csv, run Selenium to put all the links you
# might be interested in in `results`.
# i.e. appending `results`

# The end goal is to have all bunch of links that might interest you
# in the list `results`.

with open(direc+'items.csv') as f:
    for line in f.readlines():
        lst = line.replace('\n','').split(',')
        description=lst[0]
        category=lst[1]
        min_ = lst[2]
        max_ = lst[3]
        
        #1. go to craigslist.com
        driver.get('https://newyork.craigslist.org')

        #2. Click on the category that you want
        driver.find_element_by_link_text(category).click()

        #3. Now that you're on the cat page, search for the
        #   `description`, making sure your results have a 
        #   price that falls within `min_` and `max_`
        min_cl = driver.find_element_by_css_selector('.flatinput.min')
        max_cl = driver.find_element_by_css_selector('.flatinput.max')
        min_cl.send_keys(min_)
        max_cl.send_keys(max_)
        
        search = driver.find_element_by_css_selector('#query')
        search.send_keys(description)

        driver.find_element_by_css_selector('.icon-search').click()
        
        #4. Use css selectors to find all title elements and
        #   put their hrefs (i.e. link addresses) in `results`
        titles = driver.find_elements_by_css_selector('.result-title')
        for title in titles:
            link=title.get_attribute('href')
            results.append(link)
            res_txt+=link+'\n'

now=datetime.now()
time=now.strftime('%Y%m%d%H%M') 
with open(direc+"results"+time+".txt", 'w') as f:
    f.write(res_txt)

#Uncomment the following if you want yagmail to email you the results. Make
#sure you fill in your username and password.
'''
user=None
passw=None
yag=yagmail.SMTP(user, passw)
tgt_email=None
yag.send(tgt_email, 'Craigs List Results', results)
'''

driver.quit()
