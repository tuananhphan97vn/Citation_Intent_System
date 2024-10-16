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

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <a> tags
a_tags = soup.find_all('a')

# Iterate through <a> tags and replace them with 'href{i}'
for i, tag in enumerate(a_tags, start=1):
    # Replace the whole tag with 'href{i}'
    tag.replace_with(f'href{i}')

# Print the modified HTML
print(soup.prettify())
