from bs4 import BeautifulSoup
import re 
import nltk 

with open('output_test1.html' ,'r', encoding='utf-8') as f_r:
    data = f_r.read()
    soup  = BeautifulSoup(data , 'html.parser')
    full_text = soup.get_text()
    # print(soup)
    full_text = re.sub(r'\n+', '\n', full_text)
    # print(full_text)
    # full_text = re.sub(r'\s+', ' ', full_text)
    _ = full_text.split('\n')
    full_text = "\n".join([t.strip() for t in _])
    print(full_text)