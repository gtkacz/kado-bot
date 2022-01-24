import re, logging, json
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
        string = re.sub(r'[^\x00-\x7f]', r'', string)
        #string = string.split(" ")[:-1]
    
    return string

def write_to_json(name, img_src, edition=None):
    data_raw = {name: img_src}
    
    with open('characters.json', 'r+') as file:
        data = json.load(file)
        data.update(data_raw)
        file.seek(0)
        json.dump(data, file)

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
            WebDriverWait(browser, 5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'lazyloaded')))
            source = browser.page_source
            
            soup = BeautifulSoup(source, 'html.parser')
            
            img_tag = soup.find_all('img', class_ = 'lazyloaded', src = True, alt = True)
            name = img_tag[0]['alt']
            img_src = img_tag[0]['src']
            
            print(f'{c}. {name} - {img_src}')
            write_to_json(name, img_src)
            
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
                # root = Tk()
                # root.withdraw()
                # messagebox.showerror('Timeout', 'MAL took too long to respond, try again.')
                # root.destroy()
                pass

if __name__ == '__main__':
    main()