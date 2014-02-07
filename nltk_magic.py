#!/usr/bin/python

import nltk.data
from nltk import pos_tag,ne_chunk
from nltk.tokenize import WordPunctTokenizer,RegexpTokenizer,WhitespaceTokenizer,TreebankWordTokenizer
from nltk.tag import UnigramTagger
from collections import Iterable,defaultdict
from nltk.tree import *
from nltk.draw import tree
import pickle
import re

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def nltk_magic(text, processes):
	return_me = {'tokenized' : None, 'bag_of_words' : None, 'pos' : None}
	#can't extract relations without ne chunking
	if not processes['chunk'] and processes['extract_relations']:
		processes['chunk']='ne_chunk'
	
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
		#chunking only works with maximum entropy pos tagging
		if processes['pos_tag'] != 'max_pos':
			pos_tagged = [pos_tag('max_pos', tokenized_sentence) 
		for tokenized_sentence in tokenized]
		chunked = [chunk_sent(processes['chunk'], tagged_sent) for tagged_sent in pos_tagged]	
		return_me['chunk'] = chunked
		entities = {'PERSON': [], 'LOCATION': [], 'ORGANIZATION': [], "FACILITY": [], "GPE": [], "DATE": [],
		"TIME": [], "MONEY" : [], "PERCENT": []}
		for sentence in chunked:
			get_entities(sentence, entities)
		return_me['entities'] = entities
		if processes['extract_relations']:
			relations = [extract_relations(processes['extract_relations'], chunk) for chunk in chunked]
			return_me['relations'] = relations
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

def chunk_sent(chunker_type, pos_sentence):
	#right now, only default chunker is implemented, param ignored
	return ne_chunk(pos_sentence)

def extract_relations(relation_type, chunked_sentence):
	if relation_type == 'in_example':
		IN = re.compile(r'.*\bin\b(?!\b.+ing)')
		#broken
		rels = nltk.sem.extract_rels('ORG', 'LOC', chunked_sentence, pattern = IN)
		return rels
	else:
		return "NOT IMPLEMENTED"	


def get_entities(chunk_tree, ent_dict):
	for chunk in chunk_tree:
		if hasattr(chunk, "node"):
			if chunk.node in ent_dict.keys():
				ent_dict[chunk.node].append(' '.join(c[0] for c in chunk.leaves()))



