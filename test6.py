from bs4 import BeautifulSoup

# Input text
# text = '''With the rapid development of multimedia data on the Internet, multimodal summarization has attracted widespread attention from researchers. Recently proposed Multimodal Summarization with Multimodal Output (Zhu et al., <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e305" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. https://doi.org/10.18653/v1/D18-1448 "> 2018 </a> ) (MSMO) that condenses long multimodal news to a short pictorial version, as shown in Fig. <a data-track="click" data-track-action="figure anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#Fig1"> 1 </a> . This innovative approach has been substantiated to significantly enhance users’ ability to swiftly grasp key news points, thereby elevating user satisfaction (Zhu et al., <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e311" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. https://doi.org/10.18653/v1/D18-1448 "> 2018 </a> ).'''

# # Parse the HTML using BeautifulSoup
# soup = BeautifulSoup(text, "html.parser")

# # Initialize an empty list
# a_tags_list = []

# # Extract all <a> tags
# a_tags = soup.find_all('a')

# # Iterate over each <a> tag and store its information in a tuple
# for i, a_tag in enumerate(a_tags):
#     # Get the full tag as a string
#     full_tag = str(a_tag)
    
#     # Extract the text within the tag
#     text_in_tag = a_tag.get_text()
    
#     # Create a tuple (bibX, full_tag, text_in_tag)
#     a_tags_list.append((f'href{i+1}', full_tag, text_in_tag))

# # Output the list of tuples
# for item in a_tags_list:
#     print(item)
#     # print('\n')

if __name__ =='__main__':
    from bs4 import BeautifulSoup

    # Input text
    text = '''With the rapid development of multimedia data on the Internet, multimodal summarization has attracted widespread attention from researchers. Recently proposed Multimodal Summarization with Multimodal Output (Zhu et al., <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e305" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. https://doi.org/10.18653/v1/D18-1448 "> 2018 </a> ) (MSMO) that condenses long multimodal news to a short pictorial version, as shown in Fig. <a data-track="click" data-track-action="figure anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#Fig1"> 1 </a> . This innovative approach has been substantiated to significantly enhance users’ ability to swiftly grasp key news points, thereby elevating user satisfaction (Zhu et al., <a aria-label="Reference 2018" data-test="citation-ref" data-track="click" data-track-action="reference anchor" data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR45" id="ref-link-section-d206753678e311" title="Zhu, J., Li, H., Liu, T., et al. (2018). MSMO: Multimodal summarization with multimodal output. In: Riloff E, Chiang D, Hockenmaier J, et al (eds) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Brussels, Belgium, pp 4154–4164. https://doi.org/10.18653/v1/D18-1448 "> 2018 </a> ).'''

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")

    # Extract all <a> tags
    a_tags = soup.find_all('a')

    # Iterate over each <a> tag and replace it with the corresponding bib value
    for i, a_tag in enumerate(a_tags):
        # Generate the bib value like bib1, bib2, etc.
        bib_value = f'bib{i+1}'
        
        # Replace the <a> tag with the bib value
        a_tag.replace_with(bib_value)

    # Output the modified text
    modified_text = str(soup)

    # Print the modified text
    print(modified_text)

