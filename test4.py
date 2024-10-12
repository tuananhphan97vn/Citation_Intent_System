from bs4 import BeautifulSoup

# Ví dụ nội dung HTML
file_path1 = 'paper1.html'
file_path2 = 'paper2.html'
# Đọc nội dung từ tệp
with open(file_path1, 'r', encoding='utf-8') as file:
    html_content1 = file.read()
with open(file_path2, 'r', encoding='utf-8') as file:
    html_content2 = file.read()

# Chuyển đổi nội dung HTML thành đối tượng BeautifulSoup
soup1 = BeautifulSoup(html_content1, 'html.parser')
soup2 = BeautifulSoup(html_content2, 'html.parser')

# soup = BeautifulSoup(html_content, 'html.parser')

# Find all <a> tags
# for a_tag in soup1.find_all('a'):
#     # Iterate through each attribute of the <a> tag
#     for attr, value in a_tag.attrs.items():
#         # Check if the attribute value is a list
#         if isinstance(value, list):
#             # If it's a list, replace newlines in each item
#             cleaned_values = [v.replace('\n', '') for v in value]
#             a_tag[attr] = cleaned_values  # Update the attribute with the cleaned list
#         else:
#             # If it's a single string, replace newlines directly
#             a_tag[attr] = value.replace('\n', '')


def clean_new_line_inside_tag(soup):
    for a_tag in soup.find_all('a'):
        # Get the parent tag of the <a> tag
        parent_tag = a_tag.parent
        
        # Check if the parent tag is not None and remove newline characters from its text
        if parent_tag:
            cleaned_content = str(parent_tag).replace('\n', ' ')  
            parent_tag.clear()  # Xóa nội dung của thẻ cha
            parent_tag.append(BeautifulSoup(cleaned_content, 'html.parser'))  # Thêm lại nội dung đã làm sạch
    return soup

soup1 = clean_new_line_inside_tag(soup1)
# Duyệt qua tất cả các thẻ trong HTML
for element in soup1.find_all(True):
    if element.name != 'a':  # Nếu thẻ không phải <a>
        element.unwrap()  # Giữ lại văn bản và xóa thẻ

for element in soup2.find_all(True):
    if element.name != 'a':  # Nếu thẻ không phải <a>
        element.unwrap()  # Giữ lại văn bản và xóa thẻ

# In ra kết quả, thẻ <a> được giữ lại nguyên vẹn, các thẻ khác chỉ giữ văn bản
with open('out1.txt' , 'w') as f:
    f.write(soup1.prettify())

with open('out2.txt' , 'w') as f:
    f.write(soup2.prettify())
# if __name__ == '__main__':
#     string = """
# <a aria-label="Reference 2015" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR11" id="ref-link-section-d118240408e5208" title="Kingma, D.P., &amp; Ba, J (2015). Adam: A method for stochastic optimization. In: Bengio Y, LeCun Y (Eds.), 3rd International conference on learning representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings,[SPACE]
#                 http://arxiv.org/abs/1412.6980
                
#               ">
#  2015
# </a>"""
#     print(list(string))