'''
1) Takes an HTML file saved from Strata 2013 schedule 
2) Converts to text
3) Parses out talk all_titles
4) Does a simple wordcount
5) Generates wordcloud
'''


# encoding=utf8  
import sys 
import re 
import html2text
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# specify UTF-8 encoding for weird formatting
reload(sys)  
sys.setdefaultencoding('utf8')

def html_to_text(infile, outfile):
	'''
	Putting original html into text format for further parsing
	A good alternative to BeautifulSoup if the HTML input you have is HORRIBLE
	'''
	html = open(infile).read()
	text = html2text.html2text(html)
	with open(outfile, 'w') as out:
		for line in text:
			out.write(line)

def wordcount(infile, outfile, wordcloud):
	'''
	takes text file, cleans it up a little with regex, matches only titles
	and then does a wordcount on individual word popularity
	'''
	with open(infile, 'r') as stripped:
		all_titles = []
		# a bunch of ugly file cleaning and stripping from the leftover html tags
		# filters out names of rooms of talks as well
		regex = re.compile('&gt;|&lt;|/a| &lt;|/li| /div|&amp;|amp;|/ \
							|Rhinelander|Sutton|span|Sponsor*|Murray|Beekman|South|North|East|West\
							Pavilion|Center|Suite|Ballroom|Gramercy|h3|Grand|div|\
							Parlor|attend|registration|rating|regent|Nassau|Hill|Sessions\
							Please|Average|Parlor|Hall|Information|Foyer')
		for line in stripped:
			matchResult = re.search(r'&gt;\w.+ ', line)
			if matchResult:
				all_titles.append(matchResult.group())
			
		wordcount={}

		for title in all_titles:
			cleaned = regex.sub(' ', title)
			for word in cleaned.split(' '):
				if word not in wordcount:
					wordcount[word] = 1
				else:
					wordcount[word] += 1
		

		sorted_dict = sorted(wordcount.items(), key=lambda kv: kv[1])

		with open(outfile,'w') as out:
			for i in sorted_dict:
				out.write(str(i) + '\n') #tuple to string for file write

		with open(wordcloud,'w') as out:
			for title in all_titles:
				cleaned = regex.sub(' ', title)
				out.write(str(cleaned) + '\n')

def wordcloud(infile):
	text = open(infile).read()
	mask = np.array(Image.open("elephant.png"))
	wordcloud = WordCloud(max_font_size=40, mask=mask,relative_scaling=.5,margin=10,
               random_state=1).generate(text)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

if __name__ == '__main__':
	# html_to_text('stratany2013_public_schedule_full_public.html','stratany2013.txt')
	wordcount('stratany2013.txt','2013wordcount.txt','wordcloud.txt')
	wordcloud('wordcloud.txt')
	



