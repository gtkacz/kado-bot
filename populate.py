import re, logging
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import Tk, ttk, messagebox
from tkinter.filedialog import askopenfilename

def tag_cleanup(html, c_name = False):
    html = str(html)
    cleanr = re.compile('<.*?>')
    string = (re.sub(cleanr, '', html))
    string = string.replace('\n', '')
    string = string.replace('\t', '')
    
    if c_name:
        string = re.sub(r'[^\x00-\x7f]',r'', string)
        #string = string.split(" ")[:-1]
    
    return string

def attr_from_tag(string, tag):
    soup = BeautifulSoup(string, 'html.parser')
    result = [tag.attrs for tag in soup.findAll(tag)]
    
    return result

def main():
    CUR_DIR = Path(__file__).parent
    PROGRAM = 'chromedriver.exe'
    PATH = CUR_DIR / PROGRAM
    
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument('--headless')
    
    try:
        browser = webdriver.Chrome(PATH, options=OPTIONS)
        
    except WebDriverException:
        BINARY = 'D:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        # BINARY = askopenfilename()
        OPTIONS.binary_location = BINARY
        OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(PATH, options=OPTIONS)
        
    invalid_numbers = []
    c = 1
    
    while True:
        char_url = f'https://myanimelist.net/character/{c}/'
        
        try:
            browser.get(char_url)
            WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'normal_header')))
            source = browser.page_source
            
            soup = BeautifulSoup(source, 'html.parser')
            
            #name = tag_cleanup(soup.find_all('h2', class_ = 'normal_header')[0], True)
            img_src = soup.find_all('img', class_ = 'lazyloaded', src=True, alt=True)
            #print(c, name)
            for i in img_src:
                print(c, i['alt'], i['src'])
            
            c+=1
            
        except TimeoutException:
            try:
                source = browser.page_source
            
                soup = BeautifulSoup(source, 'html.parser')
                
                if soup.find_all('div', class_ = 'badresult'):
                    print(f'{c} is a invalid ID.')
                    invalid_numbers.append(c)
                    c+=1
                    continue
                
                browser.quit()
            finally:
                root = Tk()
                root.withdraw()
                messagebox.showerror('Timeout', 'MAL took too long to respond, try again.')
                root.destroy()

if __name__ == '__main__':
    main()