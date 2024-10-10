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

    links = soup.find_all('a', attrs={'data-ta': "stat-number-citation-related-count"})

    # In ra các thẻ <a> tìm được
    for link in links:
        print(link.get('href'))
    # Close the browser
    driver.quit()

if __name__ == '__main__':
    title = """Dynamic Traffic Light Control System Based on Process Synchronization Among Connected Vehicles"""
    cited_paper_url = search_paper_by_title_wos( title)
    get_paper_soure_html(cited_paper_url)