Parsel
======

Dependencies:
*NLTK
*numpy
*flask

Parsel is a very simple NLTK demo using Flask. A user can select which NLTK preprocessing techniques to run on an input string. Currently, sentence tokenizers, word tokenizers, "bag of words" and POS tagging are included (though not all fully implemented).

Parsel runs on Python 2.6.x because that's what my host has, and that's more than enough for NLTK.

It is primarily being built a training ground for me on Flask/Jinja.

In addition to installing nltk, you will need to download a few models. Start with:
```
python
import nltk
nltk.download()
```
and get punkt , maxent_ne_chunker , maxent_treebank_pos_tagger , and corpora: words.

TODO:
Take a URL (use Beautiful Soup)

Add more NLTK functionality.

Aesthetics

Un-click radio buttons
