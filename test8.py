from bs4 import BeautifulSoup
import nltk, re 

# Example HTML content
html_content = '''
<html>
<body>
	<a href="link3.html">Third Link</a>
	<a href="link2.html">Second Link</a>
	<a href="link3.html">Third Link</a>
	<a href="link4.html">Fourth Link</a>
</body>
</html>
'''

# # Parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find all <a> tags
# a_tags = soup.find_all('a')

# # Iterate through <a> tags and replace them with 'href{i}'
# for i, tag in enumerate(a_tags, start=1):
#     # Replace the whole tag with 'href{i}'
#     tag.replace_with(f'href{i}')

# # Print the modified HTML
# print(soup.prettify())

# def replace_tag_a(soup):
#     #replace all tag a with the href{i}, with i is the order of the tag <a> in the html soup file
#     links = soup.find_all('a')
#     # print(len(links))
#     links = list(set(links)) #get all unique tag a from the html soup object 
#     all_tag_a = links
#     # Loop through each <a> tag and replace it with {hrefi}
#     for i, link in enumerate(links):
#         # Create the replacement string
#         replacement = f"href{i}"
#         # Replace the <a> tag with the replacement string
#         link.replace_with(replacement)
#     return soup , all_tag_a

def replace_tag_a(soup):
	#replace all tag a with the href{i}, with i is the order of the tag <a> in the html soup file
	links = soup.find_all('a')
	# print(len(links))
	# links = list(set(links)) #get all unique tag a from the html soup object 
	all_tag_a = links
	# Loop through each <a> tag and replace it with {hrefi}
	for i, link in enumerate(links):
		# Create the replacement string
		replacement = f"href{i}"
		# Replace the <a> tag with the replacement string
		link.replace_with(replacement)
	return soup , all_tag_a

def map_sent_to_refer(sent, a_tags):
	#a_tags is the list of tag <a> inside the referecence 
	N = len(a_tags)
	result = [] 
	for i in range( N-1 , -1 , -1):
		if 'href' + str(i) in sent:
			result.append(a_tags[i])
			sent = sent.replace('href' + str(i), " " + a_tags[i].get_text() + " ")
	return sent, result

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

if __name__ == '__main__':
	with open('soup.html' , 'r') as f:
		soup = f.read()
	soup = BeautifulSoup(soup , 'html.parser')
	replaced_text , all_tag_a = replace_tag_a(soup)

	sents = sentence_split(replaced_text.get_text())
	
	with open('sent.txt','w') as f:
		f.write("\n".join(sents))

	replaced_text = replaced_text.get_text()
	with open('replaced_text.txt' , 'w', encoding='utf-8') as f:
		f.write(replaced_text)

	# print(len(all_tag_a) , len(set(all_tag_a)))
	sent = """In term of short and noise texts, enhancing word co-occurrence href50, href51, href52, href53, href54, href55, href56, href57 and exploiting external knowledge href58, href59, href60, href61, href62, href63, href64 have emerged as the two major approaches."""
	print(map_sent_to_refer(sent , all_tag_a)[0])