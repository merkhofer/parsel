#!/usr/bin/python

import nltk.data
from nltk import pos_tag
from nltk.tokenize import WordPunctTokenizer,RegexpTokenizer,WhitespaceTokenizer,TreebankWordTokenizer
from nltk.tag import UnigramTagger
from collections import Iterable,defaultdict
import pickle

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

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
		return_me['bag_of_words'] = make_bag(processes['make_bag'], tokenized)
	if processes['pos_tag']:
		pos_tagged = [pos_tag(processes['pos_tag'], tokenized_sentence) 
		for tokenized_sentence in tokenized]
		return_me['pos'] = pos_tagged
		#only if pos tagged can you chunk
		if processes['chunk']:
			chunked = [chunk(processes['chunk'], tagged_sent) for tagged_sent in pos_tagged]	
			return_me['chunk'] = chunked
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
			return 'Tokenizer not implemented'
	except ValueError: #if the input is not a list of strings
		pass

def make_bag(bag_type, list_of_tokens):
	flat_list = flatten(list_of_tokens)
	if bag_type == 'lower_bag':
		flat_list = [token.lower() for token in flat_list]
	#server is 2.6, otherwise could just:
	#bag = Counter(flat_list)
	bag = defaultdict(int)
	for word in flat_list:
		bag[word] += 1
	return bag

def pos_tag(pos_type, tokenized_sent):
	if pos_type == 'unigram':
		brown_train = pickle.load(open('res/brown_train.pkl', 'rb'))
		unigram_tagger = UnigramTagger(brown_train)
		return unigram_tagger.tag(tokenized_sent)
	elif pos_type == 'max_pos':
		return nltk.pos_tag(tokenized_sent)

def chunk(chunker_type, pos_sentence):
	return "NOT IMPLEMENTED"		





