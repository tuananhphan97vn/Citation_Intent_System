from bs4 import BeautifulSoup
import re 
import nltk 


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
	
	sents = sentence_split(html_text)

	sent_matchs = []
	for sent in sents: 
		sent_match = map_sent_to_refer(sent,  a_tags)
		sent_matchs.append(sent_match)
	return sent_matchs

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
	from bs4 import BeautifulSoup

	# Example HTML
	html = """
	<html>
		<body>
			<div>
				<p>Some text</p>
				<a href="https://example.com">Link 1</a>
			</div>
			<div class="parent">
				<a href="https://example.com/2">Link 2</a>
			</div>
			<span>
				<a href="https://example.com/3">Link 3</a>
			</span>
		</body>
	</html>
	"""

	# Initialize BeautifulSoup
	# soup = BeautifulSoup(html, 'html.parser')

	# # Find all <a> tags
	# links = soup.find_all('a')

	# # Loop through each <a> tag and replace it with {hrefi}
	# for i, link in enumerate(links, 1):
	# 	# Create the replacement string
	# 	replacement = f"href{i}"
		
	# 	# Replace the <a> tag with the replacement string
	# 	link.replace_with(replacement)

	# # Output the modified HTML
	# print(soup.prettify())

	# print("\n")
	# print(soup.get_text())
	text = """
1 IntroductionWith the rapid development of multimedia data on the Internet, multimodal summarization has attracted widespread attention from researchers. Recently proposed Multimodal Summarization with Multimodal Output (Zhu et al., href33) (MSMO) that condenses long multimodal news to a short pictorial version, as shown in Fig. href34. This innovative approach has been substantiated to significantly enhance users’ ability to swiftly grasp key news points, thereby elevating user satisfaction (Zhu et al., href35).While several methods have been proposed to tackle the MSMO task (Zhu et al., href36, href37; Jiang et al., href38), effectively handling the relationship between the image and text modalities remains a challenging problem. Zhang et al. (href39) extends the text encoder to a multimodal encoder, which takes the concatenation of textual and visual embeddings as input to obtain their contextualized joint representations. However, experimental results indicate that merely concatenating textual and visual embeddings cannot well capture the intricate relationships between modalities, such as sentence-image relationships. Jiang et al. (href40) takes sentences related to images as additional input rather than relying directly on image information. Although a image-text alignment mechanism was introduced in the sentence selection stage to leverage the relationships between images and sentences, this valuable relationship was not considered in the summarization stage.Fig. 1href41An example of multimodal summarization with multimodal output taskhref42We believe that there are extensive many-to-many relationships between images and sentences. By effectively leveraging both the relevance and irrelevance between sentences and images, we can more accurately extract salient sentences and critical images. Taking Fig. href43 as an example, the first sentence succinctly summarizes the main points of the news article: “Eating fruits and vegetables could cut the risk of heart attacks and strokes.” This guides our selection of the vegetable image which is relevant to it. Compared to the third sentence, which is only related to the BMI image, the second sentence mentions both vegetables and BMI. In this case, further selecting the second sentence, which covers different aspects of the topic, can provide a more comprehensive summary.To effectively leverage the many-to-many relationships between sentences and images for multimodal summarization, an intuitive approach is to employ graph structures for modeling these relationships. In recent years, numerous studies (Jia et al., href44; Song & King, href45) have been dedicated to exploring the application of Graph Neural Networks (GNNs) in the realm of text summarization with impressive results. Specifically, GNNs are able to model complex relationships between semantic units. By building graphs on semantic units, such as sentences, words (Wang et al., href46), latent topics (Cui et al., href47), or passages (Phan et al., href48), GNNs can enhance representations of semantic units for text summarization. Different from these works, we propose a novel heterogeneous graph for multimodal summarization. This graph includes nodes representing words, sentences, and images, with edges connecting sentences to both images and words. In this graph, images and sentences can serve as intermediaries for each other, thus enhancing their representations for multimodal summarization.To compute node representations of this graph, we propose the heterogeneous Graphormer (HeterGraphormer for short) by enhancing Graphormer (Ying et al., href49) to effectively model intricate relationships between multiple modalities. Graphormer leverages self-attention to enable attention to all nodes when updating nodes, thereby alleviating the over-smoothing issue caused by traditional GNNs. We enhance Graphormer in the follow three aspect. First, we introduce type embedding and apply distinct spatial and edge embeddings for different heterogeneous edges to more effectively handle the heterogeneity of nodes and edges. Second, the centrality embedding was removed to optimize its performance for document graphs. Third, unconnected nodes are considered during node updates, as unrelated relationships are also valuable.Overall, we propose a heterogeneous graph-based model for multimodal summarization (HGMS). The model first constructs a heterogeneous graph containing nodes for words, sentences and images. Subsequently, HeterGraphormer is employed to iteratively update the representations of nodes in the heterogeneous graph, aiming to more effectively model intricate relationships between nodes. Experimental results show that our model significantly enhances the performance of multimodal summarization. The contributions of our paper are as follows: 
"""
	sents = sentence_split(text)
	for sent in sents : 
		print( sent + "\n")
