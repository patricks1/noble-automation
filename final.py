import yagmail
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

#You need to change the text part of the following to whatever your 
#chromedriver is named. (Side note, make sure the chromedriver is in your
#automation folder.)
cService = webdriver.ChromeService(executable_path='./chromedriver_arm')

options=Options()
# Comment the following line to see Selenium working in the foreground.
options.add_argument('--headless=new') # Run in the background
driver =  webdriver.Chrome(service=cService, options=options)
driver.implicitly_wait(1)

results = []
res_txt = ''

# For each line in items.csv, run Selenium to put all the links you
# might be interested in in `results`.
# i.e. appending `results`

# The end goal is to have all bunch of links that might interest you
# in the list `results`.

with open('./items.csv') as f:
    for line in f.readlines():
        lst = line.replace('\n','').split(',')
        description=lst[0]
        category=lst[1]
        min_ = lst[2]
        max_ = lst[3]
        
        #1. go to craigslist.com
        driver.get('https://newyork.craigslist.org')

        #2. Click on the category that you want
        driver.find_element('link text', category).click()

        #3. Now that you're on the cat page, search for the
        #   `description`, making sure your results have a 
        #   price that falls within `min_` and `max_`
        min_cl = driver.find_element('css selector','[placeholder="min"]')
        max_cl = driver.find_element('css selector','[placeholder="max"]')
        min_cl.send_keys(min_)
        max_cl.send_keys(max_)
        
        search = driver.find_element('css selector','[enterkeyhint="search"]')
        search.send_keys(description)

        driver.find_element('css selector','.cl-exec-search').click()
        
        #4. Use css selectors to find all title elements and
        #   put their hrefs (i.e. link addresses) in `results`
        titles = driver.find_elements('css selector','.posting-title')
        for title in titles:
            link=title.get_attribute('href')
            results.append(link)
            res_txt+=link+'\n'

now=datetime.now()
time=now.strftime('%Y%m%d%H%M') 
with open("results"+time+".txt", 'w') as f:
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
