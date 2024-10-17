from bs4 import BeautifulSoup

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

if __name__ == '__main__':
    with open('soup.html' , 'r') as f:
        soup = f.read()
    soup = BeautifulSoup(soup , 'html.parser')
    replaced_text , all_tag_a = replace_tag_a(soup)

    replaced_text = replaced_text.get_text()
    with open('replaced_text.txt' , 'w', encoding='utf-8') as f:
        f.write(replaced_text)

    # print(len(all_tag_a) , len(set(all_tag_a)))
    sent = """In term of short and noise texts, enhancing word co-occurrence href50, href51, href52, href53, href54, href55, href56, href57 and exploiting external knowledge href58, href59, href60, href61, href62, href63, href64 have emerged as the two major approaches."""
    print(map_sent_to_refer(sent , all_tag_a)[0])