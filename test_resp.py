from resp.apis.serp_api import Serp
from resp.apis.cnnp import connected_papers
from resp.apis.semantic_s import Semantic_Scholar
from resp.apis.acm_api import ACM
from resp.apis.arxiv_api import Arxiv
from resp.resp import Resp

Paper_names = ['Zero-shot learning with common sense knowledge graphs']
api_key     = 'get_key_from_serp_api'
qs      = Serp(api_key)
result = qs.get_citations(Paper_names[0])

print(result)