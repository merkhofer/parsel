Parsel
======

Parsel is a very simple NLTK demo using Flask. The user selects which NLTK preprocessing/parsing techniques to run on an input string. Currently, sentence tokenizers, word tokenizers, "bag of words", POS tagging, chunking, and named entity recognition are included (though not all classes are implemented).

Parsel runs on Python 2.6.x because that's what my host has, and that's more than enough for NLTK. It's live at http://parsel.blackmarketsnakes.com .

It is primarily being built a training ground for me on Flask/Jinja.

Dependencies:
-------------
- NLTK

- numpy

- Flask

In addition to installing nltk, you will need to download a few models. Start with:
```
python
import nltk
nltk.download()
```
and get punkt , maxent_ne_chunker , maxent_treebank_pos_tagger , and corpora: words.

TODO:
-----
- Take a URL (use Beautiful Soup)

- Unigram not working (pickle loading)

- Add more NLTK functionality.
   * Draw parse trees (chunking)
   * Relationship extraction
   * Additional POS taggers, chunkers, etc

- Aesthetics

- Un-click radio buttons
