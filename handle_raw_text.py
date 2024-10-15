from bs4 import BeautifulSoup
import re 
import nltk 

# def sentence_split(text, keywords = ["Fig.", "Table.", "Eq.", "fig.", "Tab.", "eq.","tab.","al.","al. (", "al. ["]):
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

def handle_raw_text(text):
	lines = text.split('\n')
	lines = [   t for t in lines if t.strip() != '']
	list_sent = [] 
	for line in lines: 
		sents = sentence_split(line)
		for sent in sents :
			list_sent.append(sent.strip())
	return list_sent
		
def read_all_tag_a():
	delimiter = "<<<<<<<<<<<>>>>>>>>>>>>"
	with open('all_tag_a.html','r',encoding='utf-8') as f:
		data   = f.read()
		all_tag_a = data.split('<<<<<<<<<<<>>>>>>>>>>>>')
		all_tag_a = [BeautifulSoup(line, 'html.parser') for line in all_tag_a]
		return all_tag_a
	
def match_sent_ref(text , all_tag_a):

	#sent matches return each of sentence with corresponding reference, from the content of reference, we can retrieve and check the reference with original title or doi of cited paper 
	def map_sent_to_refer(sent, a_tags):
		#a_tags is the list of tag <a> inside the referecence 
		N = len(a_tags)
		result = [] 
		for i in range( N-1 , -1 , -1):
			if 'href' + str(i) in sent:
				result.append(a_tags[i])
				sent = sent.replace('href' + str(i), " " + a_tags[i].get_text() + " ")
		return sent, result
	
	sents = handle_raw_text(text)

	sent_matches = []
	for sent in sents: 
		sent_match = map_sent_to_refer(sent,  all_tag_a)
		sent_matches.append(sent_match)
	
	return sent_matches

def check_cited_paper_reference(title_cited_paper  , tag_a):
	title_reference  = tag_a.a.get('title')
	# print('title reference ' , title_reference)
	if title_reference is not None:
		if title_cited_paper in title_reference:
			return True 
		else:
			return False  
	else: 
		return False 
	
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

if __name__ == '__main__':
	with open('html_text2.txt' , 'r', encoding='utf-8') as f:
		text = f.read()
	all_tag_a = read_all_tag_a()
	# print(len(all_tag_a))
	sent_matches = match_sent_ref(text , all_tag_a)
	# for i, sent_match in enumerate(sent_matches):
	# 	if len(sent_match[1]) > 0 :
	# 	# 	if 'constructed a heterogeneous graph' in sent_match[0]:
	# 		print(i , sent_match)
	title_cited_paper ="""Unims: A unified framework for multimodal summarization with knowledge distillation."""
	citation_sents = find_citation_sentence(title_cited_paper , sent_matches)
	for cit_sent in citation_sents:
		print(cit_sent)
# 	text = """Wang et Table. (href67)  Jia et al. (href99) constructed a heterogeneous graph, enriching the cross-sentence relations through the word nodes between sentences. Jia et al. (href99) proposed a hierarchical heterogeneous graph to extract sentences by simultaneously balancing salience and redundancy. Cui et al. (href24) incorporates latent topics into graph propagation via a joint neural topic model, facilitating the extraction of crucial information from documents. Jing et al. (href219) proposed to use multiplex graph to model different types of relationships among sentences and words. Song and King (href107) obtains sentence representations based on constituency trees to leverage syntactic information.
# # """
	# print(handle_raw_text(text))
	# sentence_split(text)
	# print(sentence_split(text))