from bs4 import BeautifulSoup

html = '''
<li>
	<span class="label u-font-sans">
	<a class="anchor anchor-primary" data-aa-button="sd:product:journal:article:location=references:type=anchor:name=citation-name" href="#bb0175" id="ref-id-b0175">
		<span class="anchor-text-container">
		<span class="anchor-text">
			Yuan et al., 2023
		</span>
		</span>
	</a>
	</span>
	<span class="reference" id="h0175">
	<div class="contribution">
		<div class="authors u-font-sans">
		D. Yuan, T. Luo, D. Zhang, K. Zhu
		</div>
		<div class="title text-m" id="ref-id-h0175">
		A Physics-Assisted Online Learning Method for Tool Wear Prediction
		</div>
	</div>
	<div class="host u-font-sans">
		IEEE Transactions on Instrumentation and Measurement, 72 (2023), pp. 1-11,
		<a class="anchor anchor-primary" href="https://doi.org/10.1109/TIM.2023.3273683" target="_blank">
		<span class="anchor-text-container">
			<span class="anchor-text">
			10.1109/TIM.2023.3273683
			</span>
			<svg aria-label="Opens in new window" class="icon icon-arrow-up-right-tiny arrow-external-link" focusable="false" height="20" viewbox="0 0 8 8">
			<path d="M1.12949 2.1072V1H7V6.85795H5.89111V2.90281L0.784057 8L0 7.21635L5.11902 2.1072H1.12949Z">
			</path>
			</svg>
		</span>
		</a>
	</div>
	<div class="ReferenceLinks u-font-sans">
		<span class="link lazy-third-party-pdf-link">
		<span>
		</span>
		</span>
		<a aria-describedby="ref-id-h0175" class="anchor link anchor-primary" href="https://scholar.google.com/scholar_lookup?title=A%20Physics-Assisted%20Online%20Learning%20Method%20for%20Tool%20Wear%20Prediction&amp;publication_year=2023&amp;author=D.%20Yuan&amp;author=T.%20Luo&amp;author=D.%20Zhang&amp;author=K.%20Zhu" rel="noopener noreferrer" target="_blank">
		<span class="anchor-text-container">
			<span class="anchor-text">
			Google Scholar
			</span>
			<svg aria-label="Opens in new window" class="icon icon-arrow-up-right-tiny arrow-external-link" focusable="false" height="20" viewbox="0 0 8 8">
			<path d="M1.12949 2.1072V1H7V6.85795H5.89111V2.90281L0.784057 8L0 7.21635L5.11902 2.1072H1.12949Z">
			</path>
			</svg>
		</span>
		</a>
	</div>
	</span>
</li>


<li>
<span class="label u-font-sans">
<a class="anchor anchor-primary" data-aa-button="sd:product:journal:article:location=references:type=anchor:name=citation-name" href="#bb0190" id="ref-id-b0190">
<span class="anchor-text-container">
<span class="anchor-text">
 Zhang et al., 2023
</span>
</span>
</a>
</span>
<span class="reference" id="h0190">
<div class="contribution">
<div class="authors u-font-sans">
 Z. Zhang, L. Zhang, C. Wang, M. Wang, D. Cao, Z. Wang
 </div>
<div class="title text-m" id="ref-id-h0190">
 Integrated Decision Making and Motion Control for Autonomous Emergency Avoidance Based on Driving Primitives Transition
 </div>
</div>
<div class="host u-font-sans">
 IEEE Transactions on Vehicular Technology, 72 (4) (2023), pp. 4207-4221,
 <a class="anchor anchor-primary" href="https://doi.org/10.1109/TVT.2022.3221807" target="_blank">
<span class="anchor-text-container">
<span class="anchor-text">
 10.1109/TVT.2022.3221807
 </span>
</span>
</a>
</div>
</span>
</li>

<a class="anchor u-display-inline-flex anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="b0190" data-xocs-content-type="reference" href="#b0190" name="bb0190">
<span class="anchor-text-container">
<span class="anchor-text">
 Zhang et al., 2023
</span>
</span>
</a>

<a class="anchor u-display-inline-flex anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="b0175" data-xocs-content-type="reference" href="#b0175" name="bb0175">
	<span class="anchor-text-container">
	<span class="anchor-text">
		Yuan et al., 2023
	</span>
	</span>
</a>
'''
soup = BeautifulSoup(html, 'html.parser')

def find_title_by_tag_a(anchor_tag , soup):
	# Parse the HTML with BeautifulSoup

	# Step 1: Extract the <a> tag with the name attribute "bb0190"
		# print(f'Anchor tag found with name "bb0190": {anchor_tag}')
		
		# Step 2: Extract the href (e.g., href="#bb0190") and clean it up to get the ID
		# href_value = anchor_tag.get('href').replace('#', '')
	href_value = anchor_tag.get('name')
	# print(f'Href value extracted: {href_value}')
	
	# Step 3: Look for the corresponding section with id matching the href value
	reference_tag = soup.find('a', {'href': f'#{href_value}'})
	if reference_tag:
		# Now find the surrounding reference part containing the title
		reference_section = reference_tag.find_next('span', class_='reference')
		# print('reference section ', reference_section)
		if reference_section:
			# Step 4: Extract the title of the paper
			title_tag = reference_section.find('div', class_='title')
			# print('title tag ' , title_tag)
			if title_tag:
				title = title_tag.text.strip()
				print(f'Title of the paper: {title}')
			else:
				print('Title not found.')
		else:
			print('Reference section not found.')
	else:
		print(f'Reference tag with href="#{href_value}" not found.')

string = """
<a class="anchor u-display-inline-flex anchor-primary" data-sd-ui-side-panel-opener="true" data-xocs-content-id="b0175" data-xocs-content-type="reference" href="#b0175" name="bb0175">
	<span class="anchor-text-container">
	<span class="anchor-text">
		Yuan et al., 2023
	</span>
	</span>
</a>"""
anchor_tag = BeautifulSoup(string , 'html.parser').find('a')
find_title_by_tag_a(anchor_tag , soup)