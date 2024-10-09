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

if __name__ == '__main__':
    file_path = 'soup_output_1.html'

    # Đọc nội dung tệp HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Phân tích nội dung HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    get_parent_parent(soup)
