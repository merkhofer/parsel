import nltk.data
from nltk.tokenize import WordPunctTokenizer,RegexpTokenizer,WhitespaceTokenizer,TreebankWordTokenizer
from collections import Counter

def nltk_magic(text, processes):
	return_me = {'tokenized' : None, 'bag_of_words' : None, 'pos' : None}
	if processes['sent_tokenize']:
		tokenized = sent_tokenize(text)
		return_me['tokenized'] = tokenized
	else:
		#don't add this "tokenization" to product
		#however, put in [] for consistency.
		tokenized = [text]	
	if 'tokenizer_type'[0]:
		tokenized = [tokenize(sent, processes['tokenizer_type']) for sent in tokenized]
		return_me['tokenized'] = tokenized
	if processes['make_bag']:
		return_me['bag_of_words'] = make_bag(tokenized)
	if 'pos_tag':
		return_me['pos'] = pos_tag(tokenized)
	return return_me	

def sent_tokenize(in_string):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	return sent_detector.tokenize(in_string.strip())


def tokenize(sent,tokenizer_type):
	#tokenizer_type is [0] the tokenizer [1] the REGEX or ''
	tokenizer = 'not_implemented'
	#split on custom is the only non-nltk tokenizer
	if tokenizer_type == 'split_on_custom':
		return [sent.split(tokenizer_type[1]) for sent in sents]
	if tokenizer_type[0] == 'whitespace':
		tokenizer = WhitespaceTokenizer()
	if tokenizer_type[0] == 'wordpunkt':
		tokenizer = WordPunctTokenizer()
	if tokenizer_type[0] == 'regexp':
		tokenizer = RegexpTokenizer(tokenizer_type[1])
	if tokenizer_type[0] == 'treebank':
		tokenizer = TreebankWordTokenizer()
	try:
		if tokenizer != "not_implemented":
			return tokenizer.tokenize(sent)
		else:
			return 'NOT IMPLEMENTED!'
	except ValueError: #if the input is not a list of strings
		pass

def make_bag(list_of_tokens):
	#TODO: flatten the list first
	bag = Counter(list_of_tokens)
	return "HELLO"

def pos_tag(tokenized_sent):
	#NOT IMPLEMENTED
	return tokenized_sent	





