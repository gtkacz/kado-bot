import re, sys, html, requests, os
from tqdm import tqdm
from lxml import etree
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import Tk, ttk, messagebox
from tkinter.filedialog import askopenfilename

def tag_cleanup(html):
    html = str(html)
    cleanr = re.compile('<.*?>')
    string = (re.sub(cleanr, '', html))
    string = string.replace('\n', '')
    string = string.replace('\t', '')
    return string

def main():
    char_url = f'https://myanimelist.net/character/1/'
    
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

if __name__ == '__main__':
    main()