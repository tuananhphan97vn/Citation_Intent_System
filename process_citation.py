import re
from bs4 import BeautifulSoup


def split_text_with_references(text, keywords):
    # Join the keywords into a regex pattern for matching
    keywords_pattern = r'|'.join(re.escape(keyword) for keyword in keywords)
    
    # Regular expression to match sentence-ending punctuation but avoid splitting after specific keywords like Fig., Table., Eq.
    sentence_endings = re.compile(r'([.!?])(\s|$)')
    
    # Split the text using sentence-ending punctuation
    split_sentences = sentence_endings.split(text)

    # Rebuild sentences by combining punctuation marks and their respective sentence parts
    sentences = []
    for i in range(0, len(split_sentences) - 1, 3):  # group by 3: sentence, punctuation, space
        sentence = split_sentences[i] + split_sentences[i+1]
        if i + 2 < len(split_sentences):
            sentence += split_sentences[i+2]
        sentences.append(sentence.strip())
    
    # Re-attach sentences that might have been split incorrectly after keywords (e.g., Fig., Table., Eq.)
    joined_sentences = []
    skip_next = False
    for i in range(len(sentences)):
        if skip_next:
            skip_next = False
            continue
        
        sentence = sentences[i]
        if any(keyword in sentence for keyword in keywords):
            # if i + 1 < len(sentences) and sentences[i + 1].strip().startswith('<a'):
            if i + 1 < len(sentences):

                # If the next part starts with <a>, join it with the current sentence
                joined_sentences.append(sentence + " " + sentences[i + 1])
                skip_next = True  # Skip the next part because it is already handled
            else:
                joined_sentences.append(sentence)
        else:
            joined_sentences.append(sentence)

    # Strip leading/trailing spaces
    final_sentences = [sentence.strip() for sentence in joined_sentences if sentence.strip()]
    
    return final_sentences

def get_parent_parent(soup):
    a_tags = soup.find_all('a')
    # Tìm tất cả các thẻ là thẻ cha của thẻ cha của thẻ <a>
    for a_tag in a_tags:
        if a_tag.parent and a_tag.parent.parent:
            print("---------------------------------")
            parent_of_parent = a_tag.parent.parent
            print(parent_of_parent.name)  # In ra tên của thẻ là cha của cha của thẻ <a>
            print(parent_of_parent)  # In ra toàn bộ thẻ đó
            break 
# Input text
# with open('test_html.txt' , 'r') as f:
#     text = f.read()

# # Get list of sentences while keeping tags
# keywords = ["Fig.", "Table.", "Eq.", "fig.", "Tab.", "eq.","tab."]

# sentences = split_text_with_references(text , keywords)

# # Print each sentence
# for i , sentence in enumerate(sentences):
#     print(i , sentence)
#     print('------------')

def has_desired_a_tag(tag):
    # Tìm thẻ <a> con thỏa mãn các điều kiện
    a_tag = tag.find('a', attrs={'href': lambda href: href and href.startswith('#b'),
                                 'name': lambda name: name and name.startswith('bb')})
    return a_tag is not None

def find_all_a_child(soup):
    # tags_with_anchor = soup.find_all(lambda tag: tag.find('a') is not None)
    tags_with_anchor = soup.find_all('a', attrs={'href': lambda href: href and href.startswith('#b'),
                                             'name': lambda name: name and name.startswith('bb')})


# Lưu nội dung vào file
    # Extract all of the content and save it to a file
    with open('tags_with_anchor.html', 'w', encoding='utf-8') as file:
        for parent_tag in tags_with_anchor:
            # Write each tag with the <a> tag to the file, including prettifying the content
            file.write(parent_tag.prettify())
            file.write("\n") 

if __name__ == '__main__':
    file_path = 'soup_output_1.html'

    # Đọc nội dung tệp HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Phân tích nội dung HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    for script in soup.find_all('script'):
        script.decompose()  # Xóa thẻ <script> khỏi cây DOM
    for script in soup.find_all('button'):
        script.decompose()  # Xóa thẻ <script> khỏi cây DOM
    for script in soup.find_all('svg'):
        script.decompose()  # Xóa thẻ <script> khỏi cây DOM
    for script in soup.find_all('path'):
        script.decompose()  # Xóa thẻ <script> khỏi cây DOM
    for script in soup.find_all('style'):
        script.decompose()  # Xóa thẻ <script> khỏi cây DOM
    # Loại bỏ tất cả các thuộc tính sự kiện JavaScript (onclick, onmouseover, etc.)
    for tag in soup.find_all(True):  # Duyệt qua tất cả các thẻ trong tài liệu
        # Tìm tất cả các thuộc tính bắt đầu với "on", thường là các sự kiện JS
        js_attributes = [attr for attr in tag.attrs if attr.startswith('on')]
        for attr in js_attributes:
            del tag[attr]

    # output_file_path = 'output_file.html'

    # # Giả sử bạn đã có đối tượng soup (sau khi đã thực hiện các thao tác trên nó)
    # # Ví dụ: soup = BeautifulSoup(html_content, 'html.parser')

    # # Lưu đối tượng BeautifulSoup vào tệp HTML
    # with open(output_file_path, 'w', encoding='utf-8') as file:
    #     file.write(str(soup))  # Chuyển đối tượng soup thành chuỗi HTML 
    # find_all_a_child(soup)
    # parent_tags = soup.find_all(has_desired_a_tag)
    # with open('parent_tags_with_a.html', 'w', encoding='utf-8') as file:
    #     for parent_tag in parent_tags:
    #         # Ghi thẻ cha vào file với định dạng đẹp
    #         file.write(parent_tag.prettify())
    #         file.write("\n\n")
# Tìm tất cả các thẻ cha chứa thẻ con <a> thỏa mãn điều kiện
    def has_desired_a_tag(tag):
        # Tìm thẻ <a> con thỏa mãn các điều kiện
        a_tag = tag.find('a', attrs={'href': lambda href: href and href.startswith('#b'),
                                    'name': lambda name: name and name.startswith('bb')})
        return a_tag is not None   
    parent_tags = soup.find_all(has_desired_a_tag)

    # Xuất ra nội dung của các thẻ cha
    for parent_tag in parent_tags:
        print(parent_tag.prettify())
        print("\n----------------------------\n")

    # Lưu nội dung vào file nếu cần
    with open('parent_tags_with_a_content.html', 'w', encoding='utf-8') as file:
        for parent_tag in parent_tags:
            file.write(parent_tag.prettify())
            file.write("\n\n")