import re, logging, json, time
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def tag_cleanup(html, c_name = False):
    html = str(html)
    cleanr = re.compile('<.*?>')
    string = (re.sub(cleanr, '', html))
    string = string.replace('\n', '')
    string = string.replace('\t', '')
    string = string.replace('  ', ' ')
    
    if c_name:
        string = re.sub(r'[^\x00-\x7f]', r'', string)
    
    return string

def write_to_json(name, anime, img_src):
    aliases = []
    
    if name.find('"') != -1:
        aliases_index = [m.start() for m in re.finditer('"', name)]
        
        aliases = name[aliases_index[0]+1:aliases_index[1]].split(',')
        aliases = [a.strip() for a in aliases]
        
        name = name[:aliases_index[0]-1] + name[aliases_index[1]+1:]
    
    data_raw = {name: {'Anime': anime, 'Image': img_src, 'Aliases': aliases}}
    
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
    OPTIONS.add_argument('--disable-blink-features=AutomationControlled')
    
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
            
            name = tag_cleanup(soup.find_all('h1', class_ = 'title-name')[0].find_all('strong')[0])
            
            img_tag = soup.find_all('img', class_ = 'lazyloaded', src = True, alt = True)
            img_src = img_tag[0]['src']
            
            anime_div = soup.find_all('td', class_ = 'borderClass')[0]
            anime_table = anime_div.find_all('table', width = True, cellspacing = True, cellpadding = True, border = 0)[0]
            try:
                anime = tag_cleanup(anime_table.find_all('td', class_ = 'borderClass')[1])
            except IndexError:
                continue
            anime = anime.partition('add')[0]
            
            name = name.strip()
            anime = anime.strip()
            img_src = img_src.strip()
            
            print(f'{c}. {name} - {anime} - {img_src}')
            write_to_json(name, anime, img_src)
            
            c+=1
            
        except TimeoutException:
            source = browser.page_source
        
            soup = BeautifulSoup(source, 'html.parser')
            
            if soup.find_all('div', class_ = 'badresult'):
                print(f'{c} is an invalid ID.')
                invalid_numbers.append(c)
                c+=1
                continue
            
            browser.quit()
            
            with open('invalid_characters.json', 'r+') as file:
                data = json.load(file)
                data += invalid_numbers
                data = list(set(data))
                data.sort()
                file.seek(0)
                json.dump(data, file)
                
        except ConnectionRefusedError:
            time.sleep(30)
            continue
                
if __name__ == '__main__':
    main()