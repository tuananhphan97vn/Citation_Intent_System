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

	all_a_tags = soup.find_all('a')
	# Loại bỏ ký tự \n trong tất cả các thuộc tính của thẻ <a>
	for tag in all_a_tags:
		for attr, value in tag.attrs.items():
			if isinstance(value, str):
				tag[attr] = value.replace('\n', '')
					
	return soup 


def find_all_parent_tag_a(soup):
	links = soup.find_all('a')

	# Lấy các thẻ cha của mỗi thẻ <a>
	parent_tags = [link.parent for link in links]

	return parent_tags

def replace_tag_a(soup):
	#replace all tag a with the href{i}, with i is the order of the tag <a> in the html soup file
	links = soup.find_all('a')
	# print(len(links))
	links = list(set(links)) #get all unique tag a from the html soup object 
	all_tag_a = links
	# Loop through each <a> tag and replace it with {hrefi}
	for i, link in enumerate(links):
		# Create the replacement string
		replacement = f"href{i}"
		# Replace the <a> tag with the replacement string
		link.replace_with(replacement)
	return soup , all_tag_a

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

	soup2 = clean_new_line_inside_tag(soup2) 
	soup2 , all_tag_a= replace_tag_a(soup2) 

	#all tag a indicate the list of tag a 
	for tag_a in all_tag_a:
		print(tag_a)

	with open('output_test1.html', 'w', encoding='utf-8') as file:
		file.write(str(soup1))

	with open('output_test2.html', 'w', encoding='utf-8') as file:
		file.write(str(soup2))

	with open('html_text1.txt' , 'w') as f:
		f.write(soup1.get_text())

	with open('html_text2.txt' , 'w') as f:
		f.write(soup2.get_text())

	with open('all_tag_a.html' ,'w') as f:
		for tag_a in all_tag_a:
			f.write(str(tag_a) + "<<<<<<<<<<<>>>>>>>>>>>>")

if __name__ == '__main__':
	# title = """Dynamic Traffic Light Control System Based on Process Synchronization Among Connected Vehicles"""
	# cited_paper_url = search_paper_by_title_wos( title)
	# citing_paper_url = get_paper_soure_html(cited_paper_url)
	#access citting paper url and load the html content from this link 
	url = """https://link.springer.com/article/10.1007/s10844-024-00886-5"""
	get_paper_soure_html(url)