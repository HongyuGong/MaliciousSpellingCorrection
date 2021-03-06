import urllib, re, html.parser
import pickle
from fetch_toxic_score import fetch_toxic_score_online
import matplotlib.pyplot as plt

class GoogleSpellCheckCommand():
	def run(self, edit):
		if len(self.view.sel()) == 1 and self.view.sel()[0].a == self.view.sel()[0].b:
			self.view.run_command("expand_selection", {"to": "word"})

		for sel in self.view.sel():
			if sel.empty():
				continue

			fix = self.correct(self.view.substr(sel))
			edit = self.view.begin_edit()
			self.view.replace(edit, sel, fix)
			self.view.end_edit(edit)

	def correct(self, text):
		# grab html
		my_html = self.get_page('http://www.google.com/search?hl=en&q=' + urllib.request.quote(text) + "&meta=&gws_rd=ssl")
		html_parser = html.parser.HTMLParser()

		# save html for debugging
		# open('page.html', 'w').write(html)

		# pull pieces out
		match = re.search(r'(?:Showing results for|Did you mean|Including results for)[^\0]*?<a.*?>(.*?)</a>', my_html)
		if match is None:
			fix = text
		else:
			fix = match.group(1)
			fix = re.sub(r'<.*?>', '', fix)
			fix = html_parser.unescape(fix)

		# return result
		return fix

	def get_page(self, url):
		# the type of header affects the type of response google returns
		# for example, using the commented out header below google does not 
		# include "Including results for" results and gives back a different set of results
		# than using the updated user_agent yanked from chrome's headers
		# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
		headers = {'User-Agent':user_agent,}
		req = urllib.request.Request(url, None, headers)
		page = urllib.request.urlopen(req)
		my_html = str(page.read())
		page.close()
		return my_html


fn = "output/Correction_All_Sentences_Scores.pickle"
with open(fn, "rb") as handle:
    CASS = pickle.load(handle)

# X_Scores[0..3]: scores for method 0..3
# X_Scores[4]: scores for all methods
Original_Scores = [[],[],[],[],[]]
Revised_Scores = [[],[],[],[],[]]
Corrected_Scores = [[],[],[],[],[]]

for i in range(4):
    for j in range(len(CASS[i])):
        (original_sentence, original_score, revised_sentence, revised_toxic_score, correct_word, \
        new_word_list, correction_word_list, correction_score, corrected_sentence) = CASS[i][j]
        Original_Scores[i].append(original_score)
        Revised_Scores[i].append(revised_toxic_score)
        Corrected_Scores[i].append(correction_score)
        Original_Scores[4].append(original_score)
        Revised_Scores[4].append(revised_toxic_score)
        Corrected_Scores[4].append(correction_score)
        
title_prefix = 'Original vs. Revised vs. Correction Scores - '
title_suffixes = ['add', 'delete', 'replace', 'permute', 'all']
for i in range(5):
    plt.figure(i)
    plt.plot(range(len(Original_Scores[i])),sorted(Original_Scores[i]), 'r',label='original')
    plt.plot(range(len(Revised_Scores[i])),sorted(Revised_Scores[i]), 'g', label='revised')
    plt.plot(range(len(Corrected_Scores[i])),sorted(Corrected_Scores[i]), 'b', label='corrected')
    plt.legend(loc=0)
    plt.xlabel('Data point')
    plt.ylabel('Score')
    plt.title(title_prefix+title_suffixes[i])
    plt.show()
