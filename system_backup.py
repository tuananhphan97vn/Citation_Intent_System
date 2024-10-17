
#full system, the system receive the title or DOI of the paper and return
# 
# output : all of the journal citing paper that cite considered paper (cited paper) along with all of the citation sentences in the citing paper.  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re 
import nltk 
import time 

chrome_driver_path = './chromedriver'
def read_all_tag_a(file_name):
	delimiter = "<<<<<<<<<<<>>>>>>>>>>>>"
	with open(file_name,'r',encoding='utf-8') as f:
		data   = f.read()
		all_tag_a = data.split('<<<<<<<<<<<>>>>>>>>>>>>')
		all_tag_a = [BeautifulSoup(line, 'html.parser') for line in all_tag_a]
		return all_tag_a

def find_citation_sentence(title_cited_paper , sent_matches):
#sent matches is the list. each element of list is the tuple = (sent , list of tag_a)
	result = [] 
	for sent_match in sent_matches:
		flag = False 
		citation_sent = sent_match[0]
		all_tag_a = sent_match[1]
		for tag_a in all_tag_a:
			if check_cited_paper_reference(title_cited_paper , tag_a) == True :
				result.append(citation_sent)
				break 
	return result

def check_cited_paper_reference(title_cited_paper  , tag_a):
	title_reference  = tag_a.get('title')
	if title_reference is not None:
		# print('title reference ' , title_reference)
		if title_cited_paper.lower() in title_reference.lower():
			return True 
		else:
			return False  
	else: 
		return False 

def map_sent_to_refer(sent, a_tags):
	#a_tags is the list of tag <a> inside the referecence 
	N = len(a_tags)
	result = [] 
	for i in range( N-1 , -1 , -1):
		if 'href' + str(i) in sent:
			result.append(a_tags[i])
			sent = sent.replace('href' + str(i), " " + a_tags[i].get_text() + " ")
	return sent, result

def handle_raw_text(text):
	lines = text.split('\n')
	lines = [   t for t in lines if t.strip() != '']
	list_sent = [] 
	for line in lines: 
		sents = sentence_split(line)
		for sent in sents :
			list_sent.append(sent.strip())
	return list_sent


def match_sent_ref(text , all_tag_a):

	#sent matches return each of sentence with corresponding reference, from the content of reference, we can retrieve and check the reference with original title or doi of cited paper 
	
	sents = handle_raw_text(text)

	sent_matches = []
	for sent in sents: 
		sent_match = map_sent_to_refer(sent,  all_tag_a)
		sent_matches.append(sent_match)
	
	return sent_matches


def sentence_split(text, keywords = ["Fig.", "Table.", "Eq.", "fig.", "Tab.", "eq.","tab.","al.","al. (", "al. ["]):

	def check_end_string (string, keywords):
		for kw in keywords:
			if string.endswith(kw) == True:
				return True 
		return False 

	sentences = nltk.sent_tokenize(text)
	result = [] 
	N = len(sentences)
	list_index = []
	for i in range(N - 1):
		if check_end_string(sentences[i] , keywords) == True :
			list_index.append(i)
	buffer = []
	for i in range(N):
		if i not in list_index:
			if len(buffer) == 0 :
				#buffer is empty 
				result.append(sentences[i])
			else:
				#buffer is not empty, there are at least one sent is added to buffer 
				buffer.append(sentences[i])
				result.append(" ".join(buffer))
				#reset buffer 
				buffer = [] 
		else:
			buffer.append(sentences[i])
	# print('\n list sent using buffer ' , result)
	# print(len(" ".join(sentences).split()) , len(" ".join(result).split())) 
	return result


def extract_citation_sent(title, full_text_citing_paper, list_tag_a):
	#given the title of the paper, and the full text of citing paper, the list of all tag a in the html file, return all the citaton sentence that mention current paper
	#the full text of citing paper is the result of html.get_text() with all the tag a are replaced with the 'href'+order of tag a, Note: the tag a is unique because there are some duplicate link

	sent_matches = match_sent_ref(full_text_citing_paper , list_tag_a)
	for s in sent_matches:
		print(s)
		print('\n')
	citation_sents = find_citation_sentence(title , sent_matches)
	return citation_sents

def get_citing_paper_soure_html(title_cited_paper , paper_url):

	# def clean_new_line_inside_tag(soup):
	# 	all_a_tags = soup.find_all('a')
	# 	# Loại bỏ ký tự \n trong tất cả các thuộc tính của thẻ <a>
	# 	for tag in all_a_tags:
	# 		for attr, value in tag.attrs.items():
	# 			if isinstance(value, str):
	# 				tag[attr] = value.replace('\n', '')	
	# 	return soup 

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

	options = webdriver.ChromeOptions()
	service = Service(chrome_driver_path)
	driver = webdriver.Chrome(service=service, options=options)
	# driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(paper_url)
	time.sleep(5)
	soup = BeautifulSoup(driver.page_source , 'html.parser')
	with open('soup.html' ,'w') as f:
		f.write(str(soup))
	# soup = clean_new_line_inside_tag(soup) 
	soup , all_tag_a= replace_tag_a(soup) 
	replaced_text = soup.get_text()
	with open('temp.txt','w') as f:
		f.write(replaced_text)
	with open('all_tag_a.txt','w') as f:
		f.write("\n".join([str(tag_a) for tag_a in all_tag_a]))
	list_citation_context = extract_citation_sent(title_cited_paper , replaced_text , all_tag_a)
	return list_citation_context

def run(title):
	#input: the title of considered paper
	#output: all the link to acess the citing paper, which cite the input paper 

	def get_cited_paper_link(title):
		chrome_options = Options()
		chrome_options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình

		# Đường dẫn đến ChromeDriver
		chrome_driver_path = './chromedriver'  # Thay bằng đường dẫn đến ChromeDriver
		#access the google scholar link, and get the page of cited paper 
		google_scholar_link = "https://scholar.google.com/schhp?hl=en&as_sdt=0,5"
		service = Service(chrome_driver_path)
		driver = webdriver.Chrome(service=service, options=chrome_options)
		driver.get(google_scholar_link)
		current_url = ""
		try:
			search_box = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.NAME, 'q'))
			)

			# Nhập tiêu đề của bài báo
			search_box.send_keys(title)

			# Nhấn Enter để tìm kiếm
			search_box.send_keys(Keys.ENTER)

			# Chờ một khoảng thời gian để trang kết quả tải
			time.sleep(5)

			# Lấy địa chỉ URL của trang kết quả sau khi chuyển hướng
			current_url = driver.current_url
			print(current_url)
			driver.quit()

		finally:
			# Đóng trình duyệt sau khi hoàn thành tác vụ
			driver.quit()

		return current_url 
	
	def access_citing_paper_link(url):
		chrome_options = Options()
		chrome_options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình

		# Đường dẫn đến ChromeDriver
		chrome_driver_path = './chromedriver'  # Thay bằng đường dẫn đến ChromeDriver
		#access the google scholar link, and get the page of cited paper 
		service = Service(chrome_driver_path)
		driver = webdriver.Chrome(service=service, options=chrome_options)
		driver.get(url)
		time.sleep(5)
		soup = BeautifulSoup(driver.page_source , 'html.parser')
		#find the first tag a that consist of 'Cited by'
		
		first_cited_by_link = soup.find('a', string=lambda text: text and 'Cited by' in text)

		href = ""
		driver.quit()
		# Output the found link and its text
		if first_cited_by_link:
			href = first_cited_by_link['href']
			if 'https://scholar.google.com' not in href:
				href = 'https://scholar.google.com'+href
			return href 
		else:
			pass 

		return href
	
	def get_all_citing_paper_link(url):
		chrome_options = Options()
		chrome_options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình

		# Đường dẫn đến ChromeDriver
		chrome_driver_path = './chromedriver'  # Thay bằng đường dẫn đến ChromeDriver
		#access the google scholar link, and get the page of cited paper 
		service = Service(chrome_driver_path)
		driver = webdriver.Chrome(service=service, options=chrome_options)
		driver.get(url)
		time.sleep(5)
		soup = BeautifulSoup(driver.page_source , 'html.parser')

		html_content = soup.prettify()
		# Save the HTML content to a file
		with open("output.html", "w", encoding="utf-8") as file:
			file.write(html_content)
		gs_rt_links = soup.select('.gs_rt a')
		# Print all the found <a> tags
		result = [] 
		for link in gs_rt_links:
			if 'http' in link.get('href'):
				result.append((link.get_text(), link.get('href')))
		driver.quit()
		return result
		#all tag a indicate the list of tag a 

	cited_paper_link = get_cited_paper_link(title)
	citing_link = access_citing_paper_link(cited_paper_link)
	list_citing_paper_info = get_all_citing_paper_link(citing_link)

	# #after getting the citing paper links, craw the full text of the paper and filter the citation
	list_citation_context = [] 
	for citing_paper_link in list_citing_paper_info:
		if citing_paper_link[1].startswith('https://link.springer.com/'):
			print('----------------------------')
			print('Citing paper is :' , citing_paper_link[0], 'link to citing paper :', citing_paper_link[1])
			citing_url = citing_paper_link[1]
			list_citation_context = get_citing_paper_soure_html(title , citing_url)
			print('list citation context: ')
			for citation_context in list_citation_context:
				print(citation_context)


	# list_citation_context = get_citing_paper_soure_html(title , 'https://link.springer.com/article/10.1007/s10844-024-00886-5')
	# for citation_context in list_citation_context:
	# 	print(citation_context)
if __name__ == '__main__':


	# with open('html_text2.txt' , 'r', encoding='utf-8') as f:
	# 	text = f.read()
	# title_cited_paper ="""Reducing catastrophic forgetting in neural networks via gaussian mixture approximation"""
	# citing_url = """https://www.sciencedirect.com/science/article/pii/S0925231222008785"""
	# list_citation_context = get_citing_paper_soure_html(title_cited_paper , citing_url)

	# all_tag_a = read_all_tag_a('all_tag_a.html')
	# result = extract_citation_sent(title_cited_paper , text , all_tag_a)
	# for sent in result : 
	# 	print(sent)
	# run(title_cited_paper)


	
