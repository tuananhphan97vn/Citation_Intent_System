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


# Mở Web of Science
def search_paper_by_title_wos( title):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.webofscience.com/wos/woscc/basic-search")

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-option"))
        )

        # Nhập tiêu đề của bài báo
        search_box.send_keys(title)

        # Nhấn Enter để tìm kiếm
        search_box.send_keys(Keys.ENTER)

        # Chờ một khoảng thời gian để trang kết quả tải
        time.sleep(5)

        # Lấy địa chỉ URL của trang kết quả sau khi chuyển hướng
        current_url = driver.current_url

    finally:
        # Đóng trình duyệt sau khi hoàn thành tác vụ
        driver.quit()


    return current_url 

def get_paper_infor( url):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(5)
    try:
        pass

    finally:
        # Đóng trình duyệt sau khi hoàn thành tác vụ
        driver.quit()

def get_paper_soure_html(paper_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional, run in headless mode if you don't need a UI
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    options.add_argument('--no-sandbox')  # Added for certain environments

    # Automatically download and set up ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    driver.get(paper_url)

    # Wait for the page to load (you might need to adjust this depending on the page's load time)
    time.sleep(5)

    # Get the page source and convert it to a BeautifulSoup object
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print(soup)

    links = soup.find_all('a', attrs={'data-ta': "stat-number-citation-related-count"})
    # In ra các thẻ <a> tìm được
    result = [] 
    for link in links:
        href = link.get('href')
        if href.startswith("https://www.webofscience.com") == False  :
            href = "https://www.webofscience.com" + href 
            result.append(href)
    # Close the brower 
    return result[0]

def get_links_citing_papers(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Optional, run in headless mode if you don't need a UI
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    # options.add_argument('--no-sandbox')  # Added for certain environments

    # Automatically download and set up ChromeDriver
    # service = Service(ChromeDriverManager().install())
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    driver.get(url)

    # Wait for the page to load (you might need to adjust this depending on the page's load time)
    time.sleep(10)

    # Get the page source and convert it to a BeautifulSoup object
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print('soup ', soup)

    html_content = soup.prettify()

    # Save the HTML content to a file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    gs_rt_links = soup.select('.gs_rt a')

    # Print all the found <a> tags
    result = [] 
    for link in gs_rt_links:
        result.append(link.get('href') + "\t" + link.get_text())

    driver.quit()
    return result

if __name__ == '__main__':
    # title = """Dynamic Traffic Light Control System Based on Process Synchronization Among Connected Vehicles"""
    # cited_paper_url = search_paper_by_title_wos( title)
    # citing_paper_url = get_paper_soure_html(cited_paper_url)
    #access citting paper url and load the html content from this link 
    url = """https://scholar.google.com/scholar?oi=bibs&hl=en&cites=7228556788885243036"""
    citing_paper_link = get_links_citing_papers(url)
    for link in citing_paper_link:
        print(link)
