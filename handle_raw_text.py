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

	def map_sent_to_refer(sent, a_tags):
		#a_tags is the list of tag <a> inside the referecence 
		N = len(a_tags)
		result = [] 
		for i in range(N):
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

if __name__ == '__main__':
	with open('html_text2.txt' , 'r', encoding='utf-8') as f:
		text = f.read()
	all_tag_a = read_all_tag_a()
	print(len(all_tag_a))
	sent_matches = match_sent_ref(text , all_tag_a)
	# for i, sent_match in enumerate(sent_matches):
	# 	print(i , sent_match)
	print(len(set(all_tag_a)))


