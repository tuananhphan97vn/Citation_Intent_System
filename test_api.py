from resp.apis.serp_api import Serp
from resp.apis.cnnp import connected_papers
from resp.apis.semantic_s import Semantic_Scholar
from resp.apis.acm_api import ACM
from resp.apis.arxiv_api import Arxiv
from resp.resp import Resp
import pickle 
from bs4 import BeautifulSoup

# # Paper_names = ['Spatial-temporal graph neural network for traffic forecasting: An overview and open research issues']
# # # keyword     = ['Zero-shot learning']
# # api_key     = '52b380088039e73a27b352abcde765d079d3158a7f6f85c5bfb15a74d79d88c2'

# # qs      = Serp(api_key)
# # result = qs.get_citations(Paper_names[0])

# # pickle.dump( result , open('result_test.sav' , 'wb'))

result = pickle.load(open('result_test.sav' ,'rb'))['3eb5d93feaef6b88fb18e3a01ae06461']
result.to_csv('output.csv', index=False)
print(result.columns)
links = result['link']
# for link in links[:10]:
#     print(link)

from newspaper import Article

url = "https://www.scraperapi.com/blog/python-newspaper3k/"
print('url  ' , url)
article = Article(url)
article.download()
# print(article.parse())
html_text = article.html 
print('html text ' , html_text)
# soup = BeautifulSoup(html_text, 'html.parser')

# with open('soup.html' , 'w') as f:
#     f.write(str(soup))