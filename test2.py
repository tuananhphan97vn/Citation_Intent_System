import json
import requests
from time import sleep

myAPIKey = "690d5b41c1b9892147c527f73fb03f18"
# elsevier_url = "https://api.elsevier.com/content/article/doi/"
# doi1 = '10.1016/j.engappai.2023.106044' # example Tetrahedron Letters article
# fulltext1 = requests.get(elsevier_url + doi1 + "?APIKey=" + myAPIKey + "&httpAccept=text/plain")

# # save to file
# with open('fulltext1.xml', 'w') as outfile:
#     print(fulltext1.text)
#     outfile.write(fulltext1.text)

elsevier_url = "https://api.elsevier.com/content/article/doi/"
doi2 = '10.1016/j.apsadv.2024.100639' # example Tetrahedron Letters article
fulltext2 = requests.get(elsevier_url + doi2 + "?APIKey=" + myAPIKey + "&httpAccept=text/xml")

# save to file
with open('fulltext2.txt', 'w') as outfile:
    print(fulltext2.text)
    outfile.write(fulltext2.text)