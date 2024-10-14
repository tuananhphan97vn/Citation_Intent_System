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
		


if __name__ == '__main__':
	with open('html_text2.txt' , 'r', encoding='utf-8') as f:
		text = f.read()
	list_sent = handle_raw_text(text)
	for i , sent in enumerate(list_sent) :
		print(i , ' -------- ' , sent)
