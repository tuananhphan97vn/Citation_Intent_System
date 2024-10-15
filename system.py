
#full system, the system receive the title or DOI of the paper and return
# 
# output : all of the journal citing paper that cite considered paper (cited paper) along with all of the citation sentences in the citing paper.  

from bs4 import BeautifulSoup
import re 
import nltk 

def read_all_tag_a(file_name):
	delimiter = "<<<<<<<<<<<>>>>>>>>>>>>"
	with open(file_name,'r',encoding='utf-8') as f:
		data   = f.read()
		all_tag_a = data.split('<<<<<<<<<<<>>>>>>>>>>>>')
		all_tag_a = [BeautifulSoup(line, 'html.parser') for line in all_tag_a]
		return all_tag_a

def extract_citation_sent(title, full_text_citing_paper, list_tag_a):
	#given the title of the paper, and the full text of citing paper, the list of all tag a in the html file, return all the citaton sentence that mention current paper
	#the full text of citing paper is the result of html.get_text() with all the tag a are replaced with the 'href'+order of tag a, Note: the tag a is unique because there are some duplicate link
	
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
		title_reference  = tag_a.a.get('title')
		# print('title reference ' , title_reference)
		if title_reference is not None:
			if title_cited_paper in title_reference:
				return True 
			else:
				return False  
		else: 
			return False 
		
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
	
	def handle_raw_text(text):
		lines = text.split('\n')
		lines = [   t for t in lines if t.strip() != '']
		list_sent = [] 
		for line in lines: 
			sents = sentence_split(line)
			for sent in sents :
				list_sent.append(sent.strip())
		return list_sent
	
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

	sent_matches = match_sent_ref(full_text_citing_paper , list_tag_a)
	citation_sents = find_citation_sentence(title , sent_matches)
	return citation_sents

if __name__ == '__main__':
	with open('html_text2.txt' , 'r', encoding='utf-8') as f:
		text = f.read()
	title_cited_paper ="""Unims: A unified framework for multimodal summarization with knowledge distillation."""

	all_tag_a = read_all_tag_a('all_tag_a.html')
	result = extract_citation_sent(title_cited_paper , text , all_tag_a)
	for sent in result : 
		print(sent)
