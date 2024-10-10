import re
from bs4 import BeautifulSoup
import html


def remove_redun_space(text):
	# Loại bỏ khoảng trắng thừa
	text = re.sub(r'\s+', ' ', text).strip()
	return text

def sentence_split(text, keywords = ["Fig.", "Table.", "Eq.", "fig.", "Tab.", "eq.","tab."]):
	# Join the keywords into a regex pattern for matching
	keywords_pattern = r'|'.join(re.escape(keyword) for keyword in keywords)
	
	# Regular expression to match sentence-ending punctuation but avoid splitting after specific keywords like Fig., Table., Eq.
	sentence_endings = re.compile(r'([.!?])(\s|$)')
	
	# Split the text using sentence-ending punctuation
	split_sentences = sentence_endings.split(text)

	# Rebuild sentences by combining punctuation marks and their respective sentence parts
	sentences = []
	for i in range(0, len(split_sentences) - 1, 3):  # group by 3: sentence, punctuation, space
		sentence = split_sentences[i] + split_sentences[i+1]
		if i + 2 < len(split_sentences):
			sentence += split_sentences[i+2]
		sentences.append(sentence.strip())
	
	# Re-attach sentences that might have been split incorrectly after keywords (e.g., Fig., Table., Eq.)
	joined_sentences = []
	skip_next = False
	for i in range(len(sentences)):
		if skip_next:
			skip_next = False
			continue
		
		sentence = sentences[i]
		if any(keyword in sentence for keyword in keywords):
			# if i + 1 < len(sentences) and sentences[i + 1].strip().startswith('<a'):
			if i + 1 < len(sentences):

				# If the next part starts with <a>, join it with the current sentence
				joined_sentences.append(sentence + " " + sentences[i + 1])
				skip_next = True  # Skip the next part because it is already handled
			else:
				joined_sentences.append(sentence)
		else:
			joined_sentences.append(sentence)

	# Strip leading/trailing spaces
	final_sentences = [sentence.strip() for sentence in joined_sentences if sentence.strip()]
	
	return final_sentences

def get_parent_parent(soup):
	a_tags = soup.find_all('a')
	# Tìm tất cả các thẻ là thẻ cha của thẻ cha của thẻ <a>
	for a_tag in a_tags:
		if a_tag.parent and a_tag.parent.parent:
			print("---------------------------------")
			parent_of_parent = a_tag.parent.parent
			print(parent_of_parent.name)  # In ra tên của thẻ là cha của cha của thẻ <a>
			print(parent_of_parent)  # In ra toàn bộ thẻ đó
			break 

def find_title_reference_in_sentence(sentence , doc_soup):
	def find_title_by_tag_a(anchor_tag , soup):
		# Parse the HTML with BeautifulSoup

		# Step 1: Extract the <a> tag with the name attribute "bb0190"
			# print(f'Anchor tag found with name "bb0190": {anchor_tag}')
			
			# Step 2: Extract the href (e.g., href="#bb0190") and clean it up to get the ID
			# href_value = anchor_tag.get('href').replace('#', '')
		href_value = anchor_tag.get('name')
		# print(f'Href value extracted: {href_value}')
		
		# Step 3: Look for the corresponding section with id matching the href value
		reference_tag = soup.find('a', {'href': f'#{href_value}'})
		if reference_tag:
			# Now find the surrounding reference part containing the title
			reference_section = reference_tag.find_next('span', class_='reference')
			# print('reference section ', reference_section)
			if reference_section:
				# Step 4: Extract the title of the paper
				# title_tag = reference_section.find('div', class_='title')
				title_infor = reference_section.get_text().strip()
				_ = title_infor.split('\n')
				a = [t.strip() for t in _ if t.strip() != '']
				title_infor = "\n".join(a).replace("\n","<f>")
				# print('title tag ' , title_tag)
				# if title_tag:
				# # 	title = title_tag.text.strip()
				if title_infor is not None: 
					return title_infor.replace("\n","<<<<f>>>>")
				else:
					return " "
			else:
				return " "
		else:
			return " "
	soup_sentence = BeautifulSoup(sentence , 'html.parser')
	a_tags = soup_sentence.find_all('a') #find all the tag <a> in the given sentence 

	# Print each <a> tag and its href attribute
	list_title = []  
	for tag in a_tags:
		# print('----------------------------')
		# print('tag a ' , tag )
		paper_title = find_title_by_tag_a(tag ,  doc_soup)
		# print('corresponding title ' , paper_title)
		list_title.append(paper_title)
	return list_title
	

def has_desired_a_tag(tag):
	# Tìm thẻ <a> con thỏa mãn các điều kiện
	a_tag = tag.find('a', attrs={'href': lambda href: href and href.startswith('#b'),
								 'name': lambda name: name and name.startswith('bb')})
	return a_tag is not None

def find_all_a_child(soup):
	# tags_with_anchor = soup.find_all(lambda tag: tag.find('a') is not None)
	tags_with_anchor = soup.find_all('a',recursive=False, attrs={'href': lambda href: href and href.startswith('#b'),
											 'name': lambda name: name and name.startswith('bb')})


# Lưu nội dung vào file
	# Extract all of the content and save it to a file
	with open('tags_with_anchor.html', 'w', encoding='utf-8') as file:
		for parent_tag in tags_with_anchor:
			# Write each tag with the <a> tag to the file, including prettifying the content
			file.write(parent_tag.prettify())
			file.write("\n") 


def find_all_section(soup):
	sections = soup.find_all('section')

	# Xuất ra nội dung của từng thẻ <section>
	for idx, section in enumerate(sections, start=1):
		# print(f"Nội dung của thẻ section {idx}:\n")
		print(section.prettify())
		# print("\n----------------------------\n")

	# Nếu muốn lưu vào file
	with open('sections_content.html', 'w', encoding='utf-8') as file:
		for section in sections:
			file.write(section.prettify())
			# file.write("")

def transform_citations(text):
	# Regular expression to find the citation ID in the HTML tags
	pattern = r'<a[^>]*data-xocs-content-id="([^"]*)"[^>]*>.*?</a>'

	# Function to replace the HTML tag with the citation ID in square brackets
	def replace_citation_tag(match):
		citation_id = match.group(1)
		return f'[{citation_id}]'

	# Perform the replacement
	result = re.sub(pattern, replace_citation_tag, text)

	# Adjust for the parentheses around the entire citation list
	result = re.sub(r'\(([^)]*)\)', r'(\1)', result)

	return str(result)


def handle_tag_a(soup):

	sections = soup.find_all('section')
	# print(sections)
	data = []
	list_sent , list_title = [] , [] 

	with open('sentence.txt' , 'w', encoding='utf-8') as f , open('sentence_title.txt' , 'w', encoding='utf-8') as f_w:
		for section in sections:
			# f1.write(section + "\n")
			sec_id = section.get('id')
			# print('sec id ', sec_id)
			if sec_id and sec_id.startswith('s'):
				paragraphs = section.find_all('div')
				for paragraph in paragraphs:
					# Check if paragraph is inside a table
					if paragraph.find_parent('table') is None:
						# f1.write(paragraph.decode_contents() + "\n")
						paragraph_text = transform_citations(paragraph.decode_contents())
						# Decode HTML entities properly
						paragraph_text = html.unescape(paragraph_text)
						paragraph_text = remove_redun_space(paragraph_text.replace('“', '"').replace('”', '"')).replace("\n","")
						# sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph_text)
						# Merge segments correctly
						# sentences = merge_segments(sentences)
						# for sentence in sentences:
						# 	# f3.write(sentence + "\n")
						# 	clean_sentence = BeautifulSoup(sentence, 'html.parser').get_text().strip()
						# 	# f4.write(clean_sentence +"\n")
						# 	data.append({'sec_id': sec_id, 'sentence': clean_sentence})
						sentences = sentence_split(paragraph_text)
						for sent in sentences:
							# f.write(sent + "\n")
							titles = find_title_reference_in_sentence(sent , soup)
							clean_sent = BeautifulSoup(sent).get_text().strip()
							f_w.write(clean_sent + '\t    list reference    \t ' + "<reference>".join(titles) + "\n")
							list_sent.append(clean_sent)
							list_title.append(titles)
	return list_sent , list_title

def find_ciation_with_cited_paper(cited_title , soup):
	#find all the citation that mention the paper with the
	#get all sentence with list of corresponding title for all the reference in this sentence
	#after that, search to find out which sentence contain the cited_title 
	list_sent , list_title = handle_tag_a(soup)
	result = [] 
	for i in range(len(list_sent)):
		titles = list_title[i]
		for title in titles : 
			# print('title ' , title)
			if cited_title.strip() in title:
				result.append(list_sent[i])
	return result

if __name__ == '__main__':
	file_path = 'soup_output_1.html'

	# Đọc nội dung tệp HTML
	with open(file_path, 'r', encoding='utf-8') as file:
		html_content = file.read()

	# Phân tích nội dung HTML
	soup = BeautifulSoup(html_content, 'html.parser')

	# output_file_path = 'output_file.html'

	# # Giả sử bạn đã có đối tượng soup (sau khi đã thực hiện các thao tác trên nó)
	# # Ví dụ: soup = BeautifulSoup(html_content, 'html.parser')

	# # Lưu đối tượng BeautifulSoup vào tệp HTML
	# with open(output_file_path, 'w', encoding='utf-8') as file:
	#     file.write(str(soup))  # Chuyển đối tượng soup thành chuỗi HTML 
	# find_all_a_child(soup)
	# parent_tags = soup.find_all(has_desired_a_tag)
	# with open('parent_tags_with_a.html', 'w', encoding='utf-8') as file:
	#     for parent_tag in parent_tags:
	#         # Ghi thẻ cha vào file với định dạng đẹp
	#         file.write(parent_tag.prettify())
	#         file.write("\n\n")
# Tìm tất cả các thẻ cha chứa thẻ con <a> thỏa mãn điều kiện
	# def has_desired_a_tag(tag):
	#     # Tìm thẻ <a> con thỏa mãn các điều kiện
	#     a_tag = tag.find('a', attrs={'href': lambda href: href and href.startswith('#b'),
	#                                 'name': lambda name: name and name.startswith('bb')})
	#     return a_tag is not None   
	# parent_tags = soup.find_all(has_desired_a_tag)

	# # Xuất ra nội dung của các thẻ cha
	# for parent_tag in parent_tags:
	#     print(parent_tag.prettify())
	#     print("\n----------------------------\n")

	# # Lưu nội dung vào file nếu cần
	# with open('parent_tags_with_a_content.html', 'w', encoding='utf-8') as file:
	#     for parent_tag in parent_tags:
	#         file.write(parent_tag.prettify())
	#         file.write("\n\n")
	# find_all_section(soup)
	# handle_tag_a(soup)
# 	text = """With recent advancements in extensive modern sensing technology, advanced control theory, and artificial intelligence, autonomous driving has been widely recognized as an effective solution to the reduction in traffic accidents ( <a class="anchor u-display-inline-flex anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="b0115" data-xocs-content-type="reference" href="#b0115" name="bb0115"> <span class="anchor-text-container"> <span class="anchor-text"> Ren et al., 2022 </span> </span> </a> ; <a class="anchor u-display-inline-flex anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="b0190" data-xocs-content-type="reference" href="#b0190" name="bb0190"> <span class="anchor-text-container"> <span class="anchor-text"> Zhang et al., 2023 </span> </span> </a> , <a class="anchor u-display-inline-flex anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="b0180" data-xocs-content-type="reference" href="#b0180" name="bb0180"> <span class="anchor-text-container"> <span class="anchor-text"> Zhang et al., 2023 </span> </span> </a> ).
# """
# 	sentences = sentence_split(text )
# 	for i , sent in enumerate(sentences):
# 		print( i , sent)
# 		print('================================')
# 		list_title = find_title_reference_in_sentence(sent , soup)
	# with open('sentence.txt' , 'r') as f_r , open("sentence_title.txt",'w') as f_w:
	# 	lines = f_r.readlines()
	# 	for line in lines:
	# 		line = line.strip()
	# 		list_title = find_title_reference_in_sentence(line , soup)
	# 		clean_sent = BeautifulSoup(line).get_text().strip()
	# 		f_w.write(clean_sent + '\t    list reference    \t ' + "<reference>".join(list_title) + "\n")
	cited_title = """Tire-Road Peak Adhesion Coefficient Estimation Method Based on Fusion of Vehicle Dynamics and Machine Vision
"""
	citations = find_ciation_with_cited_paper(cited_title , soup)
	# for citation in citations: 
	# 	print('---------------------')
	# 	print(citation)
	set_citation = list(set(citations))
	print(len(citations) , len(set_citation))
	print('list reference ')
	for citation in set_citation:
		print(citation )
		print('-----------')
