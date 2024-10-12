from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import time

# Thiết lập Chrome options (nếu cần)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình

# Đường dẫn đến ChromeDriver
chrome_driver_path = './chromedriver'  # Thay bằng đường dẫn đến ChromeDriver của bạn

# Khởi tạo trình duyệt

def clean_new_line_inside_tag(soup):
    for a_tag in soup.find_all('a'):
        # Lấy thẻ cha của thẻ <a>
        parent_tag = a_tag.parent
        
        if parent_tag:
            # Lấy toàn bộ văn bản trong thẻ cha, loại bỏ '\n'
            parent_text = parent_tag.get_text(separator="", strip=True).replace('\n', '')
            
            # Cập nhật lại nội dung của thẻ cha
            parent_tag.clear()  # Xóa toàn bộ nội dung của thẻ cha
            parent_tag.append(parent_text)  # Thêm lại nội dung đã làm sạch

            # Đặt lại thẻ <a> vào thẻ cha
            parent_tag.append(a_tag)

        # Loại bỏ '\n' trong tất cả các thuộc tính của thẻ <a>
        for attr, value in a_tag.attrs.items():
            if isinstance(value, list):
                # Nếu giá trị là danh sách, loại bỏ '\n' trong từng phần tử
                cleaned_values = [v.replace('\n', '') for v in value]
                a_tag[attr] = cleaned_values  # Cập nhật thuộc tính
            else:
                a_tag[attr] = value.replace('\n', '')  # Loại bỏ '\n'
                
    return soup 

def get_paper_soure_html(paper_url):

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Optional, run in headless mode if you don't need a UI
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    # options.add_argument('--no-sandbox')  # Added for certain environments

    # Automatically download and set up ChromeDriver
    # service = Service(ChromeDriverManager().install())
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    driver.get(paper_url)

    # Wait for the page to load (you might need to adjust this depending on the page's load time)
    time.sleep(5)

    # Get the page source and convert it to a BeautifulSoup object
    html = driver.page_source
    soup1 = BeautifulSoup(html, 'html.parser')
    soup2 = BeautifulSoup(html, 'html.parser')

    # print(soup2)


    soup2 = clean_new_line_inside_tag(soup2)

    with open('output_test2.html', 'w', encoding='utf-8') as file:
        file.write(str(soup2))

    with open('output_test1.html', 'w', encoding='utf-8') as file:
        file.write(str(soup1))

    with open("paper1.html", "w", encoding="utf-8") as file1 , open("paper2.html", "w", encoding="utf-8") as file2:
        secs = soup1.find_all('section')
        secs2 = soup2.find_all('section')

        for sec in secs:
            file1.write(sec.prettify())

        for sec in secs2:
            print(sec)
            print('-----------')
            file2.write(sec.prettify())

    # links = soup.find_all('a', attrs={'data-ta': "stat-number-citation-related-count"})
    # # In ra các thẻ <a> tìm được
    # result = [] 
    # for link in links:
    #     href = link.get('href')
    #     if href.startswith("https://www.webofscience.com") == False  :
    #         href = "https://www.webofscience.com" + href 
    #         result.append(href)
    # # Close the brower 
    # return result[0]

if __name__ == '__main__':
    # title = """Dynamic Traffic Light Control System Based on Process Synchronization Among Connected Vehicles"""
    # cited_paper_url = search_paper_by_title_wos( title)
    # citing_paper_url = get_paper_soure_html(cited_paper_url)
    #access citting paper url and load the html content from this link 
    url = """https://link.springer.com/article/10.1007/s10844-024-00886-5"""
    get_paper_soure_html(url)