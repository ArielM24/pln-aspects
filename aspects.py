import nltk
import spacy
import pickle as pk
import glob
import operator
import re

def compute_ngrams(sequence, n):
	return zip(*[sequence[index:] for index in range(n)])

def get_pol_words(file):
	pols = {}
	f = open(file,"r",encoding="latin1")
	i = 0
	for line in f.readlines():
		try:
			value = float(re.findall('^.*pol="(-?[0-9]+\\.[0-9]+)".*$',line)[0])
			word = re.findall('^.*<.*>(.*)<.*>$',line)[0].strip()
			pols[word] = value
		except:
			pass
	f.close()
	return pols

def write_pols():
	pols = get_pol_words("/home/ariel/Documents/pln/aspects/ML-SentiCon/senticon.es.xml")
	f = open("pols.bit","wb")
	pk.dump(pols,f)
	f.close()

def read_pols():
	f = open("pols.bit","rb")
	pols = pk.load(f)
	f.close()	
	return pols

def get_text():
	txt = ""
	files = glob.glob("/home/ariel/Documents/pln/aspects/musica/*.txt")
	for file in files:
		f = open(file,"r",encoding="latin1")
		txt = txt + f.read()
		f.close()
	return txt

def get_ngrams(n):
	#get_nouns(nltk.word_tokenize(get_text()))
	nouns = read_nouns()
	ngrams = compute_ngrams(nouns,n)
	freq = {}
	for n in ngrams:
		if n in freq:
			freq[n] = freq[n] + 1
		else:
			freq[n] = 1

	return sorted(freq.items(), key=operator.itemgetter(1),reverse=True)
	
def get_nouns(text):
	nouns = []
	tokens = get_lemmas(text)
	for t in tokens:
		if t[1] == "NOUN" or t[1] == "PROPN" and t[0] != "''":
			nouns.append(t[0])
			print(t[0],t[1])
	f = open("nouns.bit","wb")
	pk.dump(nouns,f)
	f.close()
	return nouns

def get_lemmas(tokens):
	tag_tokens = []
	nlp = spacy.load("es_core_news_sm")

	for token in tokens:
		doc = nlp(token)
		pos = doc[0].lemma_, doc[0].pos_
		tag_tokens.append(pos)
		#print(pos)
	return tag_tokens

def write_lemmas(tokens):
	f = open("lemmas.bit","wb")
	pk.dump(get_lemmas(nltk.word_tokenize(get_text())),f)
	f.close()

def read_lemmas():
	f = open("lemmas.bit","rb")
	lemmas = pk.load(f)
	f.close()
	return lemmas

def get_lemmatized_text():
	#write_lemmas(get_text())
	txt = ""
	for l in read_lemmas():
		txt = txt + l[0] + " "
	return txt

def read_nouns():
	f = open("nouns.bit","rb")
	nouns = pk.load(f)
	f.close()
	return nouns

def get_aspects():
	ngrams = get_ngrams(1)
	return [ngrams[0][0][0],ngrams[1][0][0],ngrams[2][0][0],ngrams[3][0][0],ngrams[4][0][0],ngrams[6][0][0],ngrams[7][0][0]]

def get_sentences():
	return nltk.sent_tokenize(get_lemmatized_text())

def get_sent_aspects():
	snt = {}
	asp = get_aspects()
	for i in range(7):
		snt[asp[i]] = ""
	for s in get_sentences():
		for i in range(len(asp)):
			if asp[i] in  s:
				snt[asp[i]] = snt[asp[i]] + s
	return snt


def get_sents_pol():
	asp = get_aspects()
	values = []
	snt = get_sent_aspects()
	for i in range(len(asp)):
		values.append((asp[i],get_sent_pol(snt[asp[i]])))
	return values

def get_sent_pol(sent):
	p = 0
	pols = read_pols()
	s = sent.split()
	for w in s:
		try:
			p = p + pols[w]
		except:
			pass
	return p/len(s)

if __name__ == '__main__':
	#nouns = read_nouns()
	#print(nouns[:100])
	#print(get_sentences())
	#disco temer canción grupo voz guitarra rock
	#print(get_aspects()[0][0][0])
	
	print(get_sents_pol())
