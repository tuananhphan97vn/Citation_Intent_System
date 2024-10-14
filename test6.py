from bs4 import BeautifulSoup
import re 
import nltk 
# Input text
# text = '''With the rapid development of multimedia data on the Internet, multimodal summarization has attracted widespread attention from researchers. Recently proposed Multimodal Summarization with Multimodal Output (Zhu et al., <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e305" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. https://doi.org/10.18653/v1/D18-1448 "> 2018 </a> ) (MSMO) that condenses long multimodal news to a short pictorial version, as shown in Fig. <a data-track="click" data-track-action="figure anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#Fig1"> 1 </a> . This innovative approach has been substantiated to significantly enhance users’ ability to swiftly grasp key news points, thereby elevating user satisfaction (Zhu et al., <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e311" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. https://doi.org/10.18653/v1/D18-1448 "> 2018 </a> ).'''

# # Parse the HTML using BeautifulSoup
# soup = BeautifulSoup(text, "html.parser")

# # Initialize an empty list
# a_tags_list = []

# # Extract all <a> tags
# a_tags = soup.find_all('a')

# # Iterate over each <a> tag and store its information in a tuple
# for i, a_tag in enumerate(a_tags):
#     # Get the full tag as a string
#     full_tag = str(a_tag)
	
#     # Extract the text within the tag
#     text_in_tag = a_tag.get_text()
	
#     # Create a tuple (bibX, full_tag, text_in_tag)
#     a_tags_list.append((f'href{i+1}', full_tag, text_in_tag))

# # Output the list of tuples
# for item in a_tags_list:
#     print(item)
#     # print('\n')
def sentence_split(text, keywords = ["Fig.", "Table.", "Eq.", "fig.", "Tab.", "eq.","tab.","al.","al. (", "al. ["]):
	sentences = nltk.sent_tokenize(text)
	fixed_sentences = []
	buffer = ""
	
	for sentence in sentences:
		# Check if the sentence ends with "et al." or contains parentheses split
		if re.search(r'et al\.$', sentence) or re.match(r'^\(\w+', sentence):
			buffer += sentence + " "
		else:
			if buffer:
				fixed_sentences.append(buffer + sentence)
				buffer = ""
			else:
				fixed_sentences.append(sentence)
	
	return fixed_sentences

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
	
def replace_tag_a(soup):
	a_tags = soup.find_all('a')

	# Iterate over each <a> tag and replace it with the corresponding bib value
	for i, a_tag in enumerate(a_tags):
		# Generate the bib value like bib1, bib2, etc.
		bib_value = f'href{i}'
		
		# Replace the <a> tag with the bib value
		a_tag.replace_with(bib_value)

	# Output the modified text
	# modified_text = str(soup)
	return soup.get_text(), a_tags

def split_sent_and_match_reference(soup):

	def map_sent_to_refer(sent, a_tags):
		#a_tags is the list of tag <a> inside the referecence 
		N = len(a_tags)
		result = [] 
		for i in range(N):
			if ' href' + str(i) + " " in sent:
				result.append(a_tags[i])
				sent = sent.replace(' href' + str(i) + " ", a_tags[i].get_text())
		return sent, result

	html_text , a_tags = replace_tag_a(soup)
	

	print('html text ', html_text)

	sents = sentence_split(html_text)
	
	for i ,sent in enumerate(sents):
		print(i, sent)

	sent_matchs = []
	for sent in sents: 
		sent_match = map_sent_to_refer(sent,  a_tags)
		# print(sent_match)
		# print('-------------')

def remove_redun_space(text):
	# Loại bỏ khoảng trắng thừa
	text = re.sub(r'\s+', ' ', text).strip()
	return text

def norm_text(text):
	text = remove_redun_space(text)
	text.replace("\n<a>","<a>").replace("\n <a>"," <a>").replace('</a>\n','</a>')
	return text 

def clean_new_line_inside_tag(soup):

	all_a_tags = soup.find_all('a')
	# Loại bỏ ký tự \n trong tất cả các thuộc tính của thẻ <a>
	for tag in all_a_tags:
		for attr, value in tag.attrs.items():
			if isinstance(value, str):
				tag[attr] = value.replace('\n', '')
					
	return soup 

if __name__ =='__main__':
	from bs4 import BeautifulSoup

	# Input text
	text = '''    While several methods have been proposed to tackle the MSMO task (Zhu et al.,
	<a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e317" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164.                 https://doi.org/10.18653/v1/D18-1448                              ">
	 2018
	</a>
	,
	<a aria-label="Reference 2020" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR46" id="ref-link-section-d206753678e320" title="Zhu, J., Zhou, Y., Zhang, J., et al. (2020). Multimodal summarization with guidance of multimodal reference. Proceedings of the AAAI Conference on Artificial Intelligence, 34(05), 9749–975.                 https://doi.org/10.1609/aaai.v34i05.6525                              ">
	 2020
	</a>
	; Jiang et al.,
	<a aria-label="Reference 2023" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR8" id="ref-link-section-d206753678e323" title="Jiang, C., Xie, R., Ye, W., et al. (2023). Exploiting pseudo image captions for multimodal summarization. In: Rogers A, Boyd-Graber J, Okazaki N (Eds.), Findings of the association for computational linguistics: ACL 2023. Association for Computational Linguistics, Toronto, Canada, pp 161–175.                 https://doi.org/10.18653/v1/2023.findings-acl.12                              ">
	 2023
	</a>
	), effectively handling the relationship between the image and text modalities remains a challenging problem. Zhang et al. (
	<a aria-label="Reference 2022c" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR43" id="ref-link-section-d206753678e326" title="Zhang, Z., Meng, X., Wang, Y., et al. (2022c). Unims: A unified framework for multimodal summarization with knowledge distillation. Proceedings of the AAAI Conference on Artificial Intelligence 36(10) 11757–11764.                 https://doi.org/10.1609/aaai.v36i10.21431                              ">
	 2022c
	</a>
	) extends the text encoder to a multimodal encoder, which takes the concatenation of textual and visual embeddings as input to obtain their contextualized joint representations. However, experimental results indicate that merely concatenating textual and visual embeddings cannot well capture the intricate relationships between modalities, such as sentence-image relationships. Jiang et al. (
	<a aria-label="Reference 2023" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR8" id="ref-link-section-d206753678e329" title="Jiang, C., Xie, R., Ye, W., et al. (2023). Exploiting pseudo image captions for multimodal summarization. In: Rogers A, Boyd-Graber J, Okazaki N (Eds.), Findings of the association for computational linguistics: ACL 2023. Association for Computational Linguistics, Toronto, Canada, pp 161–175.                 https://doi.org/10.18653/v1/2023.findings-acl.12                              ">
	 2023
	</a>
	) takes sentences related to images as additional input rather than relying directly on image information. Although a image-text alignment mechanism was introduced in the sentence selection stage to leverage the relationships between images and sentences, this valuable relationship was not considered in the summarization stage.'''

	# Parse the HTML using BeautifulSoup
	text = norm_text(text)
	# print(text)
	soup = BeautifulSoup(text, "html.parser")
	soup = clean_new_line_inside_tag(soup)
	# print(soup)
	# print('<<<<<<<>>>>>>>>.')
	# # Extract all <a> tags
	# # html_text , a_tags = replace_tag_a(soup)
	# # print(html_text)
	# # print(a_tags)
	split_sent_and_match_reference(soup)
	# import nltk
	# import re

	# Download necessary data for sentence tokenization
	# nltk.download('punkt')

	# The input text
	# text = """While several methods have been proposed to tackle the MSMO task (Zhu et al., href0, href1; Jiang et al., href2), effectively handling the relationship between the image and text modalities remains a challenging problem. Zhang et al. (href3) extends the text encoder to a multimodal encoder, which takes the concatenation of textual and visual embeddings as input to obtain their contextualized joint representations. However, experimental results indicate that merely concatenating textual and visual embeddings cannot well capture the intricate relationships between modalities, such as sentence-image relationships. Jiang et al. (href4) takes sentences related to images as additional input rather than relying directly on image information. Although an image-text alignment mechanism was introduced in the sentence selection stage to leverage the relationships between images and sentences, this valuable relationship was not considered in the summarization stage.
	# """

	# Tokenize the text into sentences
	# sentences = nltk.sent_tokenize(text)

	# # Recombine sentences that were incorrectly split due to "et al." or parentheses
	# def sentence_splits(text):
	# 	sentences = nltk.sent_tokenize(text)
	# 	fixed_sentences = []
	# 	buffer = ""
		
	# 	for sentence in sentences:
	# 		# Check if the sentence ends with "et al." or contains parentheses split
	# 		if re.search(r'et al\.$', sentence) or re.match(r'^\(\w+', sentence):
	# 			buffer += sentence + " "
	# 		else:
	# 			if buffer:
	# 				fixed_sentences.append(buffer + sentence)
	# 				buffer = ""
	# 			else:
	# 				fixed_sentences.append(sentence)
		
	# 	return fixed_sentences

	# # Apply the fix
	# fixed_sentences = sentence_splits(sentences)

	# # Output the sentences
	# for i, sentence in enumerate(fixed_sentences, 1):
	# 	print(f"{i}. {sentence}")
