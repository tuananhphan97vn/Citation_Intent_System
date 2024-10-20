# from resp.apis.serp_api import Serp
# from resp.apis.cnnp import connected_papers
# from resp.apis.semantic_s import Semantic_Scholar
# from resp.apis.acm_api import ACM
# from resp.apis.arxiv_api import Arxiv
# from resp.resp import Resp
# import pickle 
# from bs4 import BeautifulSoup

# # # Paper_names = ['Spatial-temporal graph neural network for traffic forecasting: An overview and open research issues']
# # # # keyword     = ['Zero-shot learning']
# # # api_key     = '52b380088039e73a27b352abcde765d079d3158a7f6f85c5bfb15a74d79d88c2'

# # # qs      = Serp(api_key)
# # # result = qs.get_citations(Paper_names[0])

# # # pickle.dump( result , open('result_test.sav' , 'wb'))

# result = pickle.load(open('result_test.sav' ,'rb'))['3eb5d93feaef6b88fb18e3a01ae06461']
# result.to_csv('output.csv', index=False)
# print(result.columns)
# links = result['link']
# # for link in links[:10]:
# #     print(link)

# from newspaper import Article

# url = "https://www.scraperapi.com/blog/python-newspaper3k/"
# print('url  ' , url)
# article = Article(url)
# article.download()
# # print(article.parse())
# html_text = article.html 
# print('html text ' , html_text)
# soup = BeautifulSoup(html_text, 'html.parser')

# with open('soup.html' , 'w') as f:
#     f.write(str(soup))
# import httpx
# import time

# def scopus_paper_date(paper_doi,apikey):
#     apikey=apikey
#     headers={
#         "X-ELS-APIKey":apikey,
#         "Accept":'application/json'
#          }
#     timeout = httpx.Timeout(10.0, connect=60.0)
#     client = httpx.Client(timeout=timeout,headers=headers)
#     query="&view=FULL"
#     url=f"https://api.elsevier.com/content/article/doi/10.1016/j.neunet.2024.106207"
#     r=client.get(url)
#     print(r)
#     return r

# y = scopus_paper_date('10.1016/j.solmat.2021.111326',"58289bcb3b83e71def92493b40e8a7c2")
# # Parse document
# import json
# json_acceptable_string = y.text
# print(json_acceptable_string)
import json
import requests
from time import sleep
# from api_key import myAPIKey

# for xml download
# elsevier_url = "https://api.elsevier.com/content/article/"
# doi1 = 'pii/S0925231222008785' # example Tetrahedron Letters article
# fulltext1 = requests.get(elsevier_url + doi1 + "?APIKey=" + '690d5b41c1b9892147c527f73fb03f18' + "&httpAccept=text/xml")

# print(fulltext1.text)
# # save to file
# with open('fulltext1.xml', 'w', encoding='utf-8') as outfile:
#     outfile.write(fulltext1.text)

import requests

# Replace with your Elsevier API Key
api_key = '690d5b41c1b9892147c527f73fb03f18'
# Replace with the DOI of the paper you're interested in 
doi = 'S1566253520302992'
# URL for ScienceDirect API
url = f'https://api.elsevier.com/content/article/pii/{doi}'

# Setting up the request headers with API key
headers = {
	'X-ELS-APIKey': api_key,
	'Accept': 'application/json'
}

# Making the API request
response = requests.get(url, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
	# Parse the JSON response
	paper_data = response.json()
	with open('result.json', 'w') as f:
		json.dump(paper_data , f, indent=4)
else:
	print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")