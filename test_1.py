from bs4 import BeautifulSoup
import re 

# Đường dẫn đến tệp HTML
file_path = 'soup_output_1.html'

# Đọc nội dung tệp HTML
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Phân tích nội dung HTML
soup = BeautifulSoup(html_content, 'html.parser')

# tags_with_direct_a = []
# for tag in soup.find_all(True):  # Tìm tất cả các thẻ trong tài liệu
#     # Kiểm tra nếu thẻ hiện tại có chứa thẻ <a> là con trực tiếp
#     for child in tag.children:
#         if child.name == 'a':  # Thẻ con là <a> và là con trực tiếp
#             # clean_content = str(tag).replace('\n', '').replace('\r', '')
#             clean_content =  str(tag).replace('\n', '').replace('\r', '')
#             tags_with_direct_a.append(clean_content)  # Lưu nội dung đã làm sạch
#             break  # Dừng kiểm tra khi tìm thấy thẻ <a> là con trực tiếp
tags_with_direct_a = []
for tag in soup.find_all(True):  # Tìm tất cả các thẻ trong tài liệu
    # Kiểm tra nếu thẻ hiện tại có chứa thẻ <a> là con trực tiếp
    for child in tag.children:
        if child.name == 'a':  # Thẻ con là <a> và là con trực tiếp
            # clean_content = str(tag).replace('\n', '').replace('\r', '')
            clean_content =  str(tag).replace('\n', '')
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            tags_with_direct_a.append(clean_content)  # Lưu nội dung đã làm sạch
            break  # Dừng kiểm tra khi tìm thấy thẻ <a> là con trực tiếp

# Ghi nội dung đã trích xuất vào tệp
with open('output_with_links_1.txt', 'w', encoding='utf-8') as output_file:
    for content in tags_with_direct_a:
        output_file.write(content + '\n')  # Ghi mỗi nội dung vào một dòng mới

# In ra nội dung đã trích xuất
# for content in p_contents:
#     print(content)