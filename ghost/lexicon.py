''' Lexicon.py
Efficiently supports checking if a string is a valid English prefix 
or word. The lexicon is backed by a trie data structure.
'''

import sys
import string

WORDS_FILE = 'TWL_2006_ALPHA.txt' # from Scrabble.com

# Internal classes and functions
class _Node(object):
    ''' A node in the trie '''
    def __init__(self, letter):
        self.letter = letter
        self.next = {}
        self.eow = False # end of word marker
       
    def next_letters(self):
        return self.next.keys()

    def debug(self, depth=0):
        print '\t' * depth,
        print self.letter, '--> [' + ', '.join(self.next_letters()) + ']',
        if self.eow:
            print 'EOW'
        print

    def debug_full(self, depth=0):
        self.debug(depth)
        for letter, node in self.next.iteritems():
            node.debug_full(depth + 1)

def _insert_word(word):
    if word:
        _insert_word_rec(word, _dawg)

def _insert_word_rec(word, node):
    if not word:
        node.eow = True
        return
    next_node = node.next.setdefault(word[0], _Node(word[0]))
    _insert_word_rec(word[1:], next_node)

def _traverse(str):
    ''' Returns the node corresponding to the last letter in string str '''
    return _traverse_rec(str, _dawg)

def _traverse_rec(str, node):
    if not str:
        return node
    if str[0] in node.next_letters():
        return _traverse_rec(str[1:], node.next[str[0]])
    else:
        return None

# Initialization script
_dawg = _Node(None) # the root node (it has no letter)
lines_read = 0 
sys.stdout.write('loading lexicon')
sys.stdout.flush()
try:
    f = open(WORDS_FILE)
    for line in f:
        _insert_word(line.strip().lower()) # words are coerced to lowercase
        lines_read += 1
        if lines_read % 25000 == 0: 
            sys.stdout.write('.')
            sys.stdout.flush()
except IOError as e:
    print 'Error opening the file'
else:
    f.close()
    print '{0} words added\n'.format(lines_read)

# Public functions
def has_prefix(prefix):
    return bool(_traverse(prefix))

def has_word(word, min_length=0):
    last_node = _traverse(word)
    return bool(last_node) and last_node.eow and len(word) >= min_length

def valid_continuations(prefix):
    node = _traverse(prefix)
    if node:
        return node.next_letters()
    else: 
        return None

# Sanity checks
if __name__ == '__main__':
    _insert_word('hi')
    _insert_word('hat')
    _insert_word('hit')
    _insert_word('hop')
    _insert_word('hopefulness')
    _dawg.debug_full()
    print has_prefix('h')            # true
    print has_prefix('it')           # false
    print has_prefix('hopefuln')     # true
    print has_word('hopefuln')       # false
    print has_word('hopefulness')    # true
    print valid_continuations('h')   # ['i', 'a', 'o']
    print valid_continuations('haz') # None
