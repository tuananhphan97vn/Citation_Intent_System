from bs4 import BeautifulSoup

# Example HTML content
html_content = '''
<html>
<body>
    <a href="link1.html">Some Link</a>
    <a href="link2.html">Cited by 10</a>
    <a href="link3.html">Another Link</a>
    <a href="link4.html">Cited by 15</a>
</body>
</html>
'''

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the first <a> tag that contains the text 'Cited by'
first_cited_by_link = soup.find('a', string=lambda text: text and 'Cited by' in text)

# Output the found link and its text
if first_cited_by_link:
    print("Found:", first_cited_by_link['href'])
    print("Text:", first_cited_by_link.text)
else:
    print("No 'Cited by' link found")
