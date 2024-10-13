import re 

def remove_redun_space(text):
	# Loại bỏ khoảng trắng thừa
	text = re.sub(r'\s+', ' ', text).strip()
	return text

def norm_text(text):
	text = remove_redun_space(text)
	text.replace("\n<a>","<a>").replace("\n <a>"," <a>")
	return text 

def sentence_split(text, keywords = ["Fig.", "Table.", "Eq.", "fig.", "Tab.", "eq.","tab.","al."]):
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

def clean_new_line_inside_tag(soup):
	
	for a_tag in soup.find_all('a'):
		# Get the parent tag of the <a> tag
		parent_tag = a_tag.parent
		
		if parent_tag:
			# Clean the parent's text content while keeping the <a> tags
			# Get all the text from the parent while skipping the <a> tags
			text_content = ''.join(parent_tag.find_all(text=True, recursive=False)).replace('\n', '')
			
			# Update the parent's content by clearing only the text
			for element in parent_tag.contents:
				if element != a_tag:
					element.extract()  # Remove any element that is not <a>

			# Append the cleaned text back to the parent tag
			parent_tag.insert(0, text_content)  # Add text before the <a> tag

	return soup

if __name__ == '__main__':

	text = """    With the rapid development of multimedia data on the Internet, multimodal summarization has attracted widespread attention from researchers. Recently proposed Multimodal Summarization with Multimodal Output (Zhu et al.,
    <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e305" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164.                 https://doi.org/10.18653/v1/D18-1448                              ">
     2018
    </a>
    ) (MSMO) that condenses long multimodal news to a short pictorial version, as shown in Fig.
    <a data-track="click" data-track-action="figure anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#Fig1">
     1
    </a>
    . This innovative approach has been substantiated to significantly enhance users’ ability to swiftly grasp key news points, thereby elevating user satisfaction (Zhu et al.,
    <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e311" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164.                 https://doi.org/10.18653/v1/D18-1448                              ">
     2018
    </a>
    ).
"""
	text = norm_text(text)
	print(text )
	sentences = sentence_split(text )
	for i , sent in enumerate(sentences):
		print( i , sent)
		print('================================')
# 	from bs4 import BeautifulSoup

# 	# Example HTML content
# 	html_content = '''
#    <p>
# 	With the rapid development of multimedia data on the Internet, multimodal summarization has attracted widespread attention from researchers. Recently proposed Multimodal Summarization with Multimodal Output (Zhu et al.,
# 	<a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d129259303e305" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. 
# 				https://doi.org/10.18653/v1/D18-1448
				
# 			  ">
# 	 2018
# 	</a>
# 	) (MSMO) that condenses long multimodal news to a short pictorial version, as shown in Fig.
# 	<a data-track="click" data-track-action="figure anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#Fig1">
# 	 1
# 	</a>
# 	. This innovative approach has been substantiated to significantly enhance users’ ability to swiftly grasp key news points, thereby elevating user satisfaction (Zhu et al.,
# 	<a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d129259303e311" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. 
# 				https://doi.org/10.18653/v1/D18-1448
				
# 			  ">
# 	 2018
# 	</a>
# 	).
#    </p>
# 	'''

# 	html_content = """
# <html>
#   <body>
# 	<div>
# 		<p>Some text here\nwith newline
# 		<a href="https://example.com \n \n hello" >Link to example</a>
# 		</p>
# 	</div>
# 	<div>
# 		<a href="https://example2.com">Example 2 Link</a> 

# 		bo lo ba la
# 	</div>
#   </body>
# </html>"""
# 	# Create a BeautifulSoup object
# 	def clean_tag(soup):

# 		for p_tag in soup.find_all('p'):
# 			# Lấy toàn bộ văn bản trong thẻ <p>, loại bỏ '\n'
# 			cleaned_text = p_tag.get_text(separator="", strip=True).replace('\n', '')
			
# 			# Xóa toàn bộ nội dung hiện tại của thẻ <p>
# 			p_tag.clear()
			
# 			# Thêm lại văn bản đã làm sạch vào thẻ <p>
# 			p_tag.append(cleaned_text)
			
# 			# Thêm lại tất cả các thẻ con vào thẻ <p>
# 			for child in p_tag.find_all(True):  # Tìm tất cả các thẻ con
# 				if child.name == 'a':  # Chỉ thêm lại thẻ <a>
# 					p_tag.append(child)

# 		return soup 

# 	# Print the modified HTML
# 	soup = BeautifulSoup(html_content, 'html.parser')
# 	print('before cleaning ......... ')
# 	print(soup)
# 	soup = clean_tag(soup)
# 	print('after cleaning................')
# 	print(soup)
# 	# divs = soup.find_all('div')
# 	# for div in divs:
# 	# 	print('-------')
# 	# 	print(div)
