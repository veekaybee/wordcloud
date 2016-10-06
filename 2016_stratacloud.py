'''
Parse .ics file into human-readable text format
and create a wordcloud from text titles
'''

from icalendar import Calendar, Event
from datetime import datetime
import glob, os
import sys 
import re 
import html2text
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# date formats for DTSTART and END
start_format = "%a %b %d %H:%M"
end_format = "%H:%M" #only hour needed for end time


def parse_ics(infile):
	
	cal = Calendar.from_ical(infile.read())

	events = []

	for component in cal.walk('vevent'):
		event =   component.get('summary')
		line =  "Summary:%s \n" % (event)
		events.append(line)

	return events

def ics_to_file(filename, events):
	with open(filename, 'w') as f:
		for e in events:
			f.write(e.encode('utf-8')) #include correct encoding

def wordcloud(infile):
	text = open(infile).read()
	mask = np.array(Image.open("elephant.png"))
	wordcloud = WordCloud(max_font_size=40, mask=mask,relative_scaling=.5,margin=10,
               random_state=1).generate(text)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

def convert_file():
	for file in glob.glob("*.ics"):
		outfilename = os.path.splitext(file)[0]
		infile = open(file, 'rb')
		parsed_results = parse_ics(infile)
		ics_to_file('%s.txt' % outfilename, parsed_results) 
		wordcloud('2016Strata.txt')


if __name__ == '__main__':
	convert_file()