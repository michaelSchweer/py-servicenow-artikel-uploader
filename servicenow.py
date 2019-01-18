import sys
import os
import re
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

baseUrl = '<BASE URL>'

afdID = int(input('Afdeling?: '))
artikelID = int(input('Artikel?: '))

klokkenEr = str(datetime.now())
logFileName = '{}.log'.format(klokkenEr.replace(':', '_'))
userName = os.environ['USERNAME']
computerName = os.environ['COMPUTERNAME']
print('')
strStart = 'Startet af {} @ {}, {}'.format(userName, computerName, klokkenEr)
print(strStart)


options = Options()
# options.add_argument('--headless') # kommentér denne linje ud for at få vist browseren under eksekvering
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
options.add_argument('--silent')
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(3)
driver.get(baseUrl)
print('')

sleep(2)

# test-instance creds
login = ActionChains(driver)
login.send_keys('<USER>')
login.send_keys(Keys.TAB)
login.send_keys('<PASSWD>')
login.send_keys(Keys.ENTER)
login.perform()

sleep(3)

driver.get('<POST FORM>')

# input strings, TABs away
inputKB = 'Consumer Service' # 0
inputCategory = 'Cat' # 1
inputShortDesc = 'Kort beskrivelse...' # 14
inputUser = 'Bruger kommentar' # 16
# submit, 18

artikelDir = 'path\\{}\\{}'.format(afdID, artikelID)
artikelHTML = 'path\\{}\\{}\\{}-{}.html'.format(afdID, artikelID, afdID, artikelID)
with open(artikelHTML, 'r', encoding="utf8") as f:
    inputTech = f.read()

artikelFiler = os.listdir(artikelDir)
picFiler = []
for fil in artikelFiler:
    if not fil.endswith('.html'):
        picFuldSti = os.path.join(artikelDir, fil)
        picFiler.append(picFuldSti)

antalPics = len(picFiler)
regexImgTag = re.compile("(<img.*?>)")
htmlParts = re.split(regexImgTag, inputTech)

for part in htmlParts:
    if part.startswith('<img '):
        del htmlParts[htmlParts.index(part)]

sleep(2)
attachBtn = driver.find_element_by_id('header_add_attachment')
attachBtn.click()
sleep(1)

for picFil in picFiler:
    driver.find_element_by_id('attachFile').send_keys(picFil)
    sleep(1)

print('[{}] {} pic(s) attached'.format(artikelID, len(picFiler)))

ActionChains(driver).send_keys(Keys.ENTER).perform()
sleep(1)
driver.find_element_by_id('sys_display.kb_knowledge.kb_knowledge_base').send_keys(inputKB)
driver.find_element_by_id('kb_knowledge.short_description').send_keys(inputShortDesc)

sleep(1)
codeBtn = driver.find_element_by_id('mceu_48')
picBtn = driver.find_element_by_id('mceu_46')

ActionChains(driver).move_to_element(codeBtn)
sleep(1)

indsattePics = 0
for p in htmlParts:
    codeBtn.click()
    sleep(1)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()
    sleep(1)
    if htmlParts.index(p) == 0:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
    pasteHTML = ActionChains(driver)
    pasteHTML.send_keys(p)
    pasteHTML.perform()
    sleep(1)
    buttons = driver.find_elements_by_tag_name('button')
    for b in buttons:
        if 'Ok' in b.text:
            b.click()
            break
    sleep(1)

    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()

    if antalPics:
        picBtn.click()
        sleep(1)
        picToInsert = picFiler[indsattePics].split('\\')[-1]
        sleep(1)
        selectPic = Select(driver.find_element_by_id('attachment_list'))
        selectPic.select_by_visible_text(picToInsert)
        antalPics -= 1
        indsattePics += 1
        sleep(1)

        # selectAlign = Select(driver.find_element_by_id('f_align'))
        # selectAlign.select_by_visible_text('Middle')
        # sleep(1)

        saveBtn = driver.find_element_by_id('save_button')
        saveBtn.click()
        sleep(1)

        
print('[{}] Done...'.format(artikelID))