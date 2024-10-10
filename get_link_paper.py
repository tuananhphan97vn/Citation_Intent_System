from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Thiết lập Chrome options (nếu cần)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình

# Đường dẫn đến ChromeDriver
chrome_driver_path = './chromedriver'  # Thay bằng đường dẫn đến ChromeDriver của bạn

# Khởi tạo trình duyệt
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Mở Web of Science
driver.get("https://www.webofscience.com/wos/woscc/basic-search")

try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-option"))
    )

    # Nhập tiêu đề của bài báo
    title = "Read-All-in-Once (RAiO): Multi-Layer Contextual Architecture for Long-Text Machine Reading Comprehension"
    search_box.send_keys(title)

    # Nhấn Enter để tìm kiếm
    search_box.send_keys(Keys.ENTER)

    # Chờ một khoảng thời gian để trang kết quả tải
    time.sleep(5)

    # Lấy địa chỉ URL của trang kết quả sau khi chuyển hướng
    current_url = driver.current_url
    print(f"Địa chỉ trang web kết quả: {current_url}")

finally:
    # Đóng trình duyệt sau khi hoàn thành tác vụ
    driver.quit()