from bs4 import BeautifulSoup

tag_a = """<a aria-label="Reference 2008" data-test="citation-ref" data-track="click" data-track-action="reference anchor" 
data-track-label="link" href="/article/10.1007/s10844-024-00886-5#ref-CR20" 
id="ref-link-section-d67334732e6502" 
title="van der Maaten L, &amp; Hinton G (2008) Visualizing data using t-sne. Journal of Machine Learning Research 9(86), 2579–2605. 
http://jmlr.org/papers/v9/vandermaaten08a.html">2008</a>
"""

# Parse the tag once
tag_a = BeautifulSoup(tag_a, 'html.parser')

# Get the 'title' attribute value
title_value = tag_a.a.get('title')

print(title_value)
