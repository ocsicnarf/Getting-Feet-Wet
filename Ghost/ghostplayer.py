''' ghostplayer.py
Defines an abstract class for computer Ghost players.
Provides an implementation of a simple computer player
at the moment
'''

import string
import random
import lexicon

class GhostPlayer(object):
    
    def get_name(self):
        ''' Returns the computer player's name '''
        raise NotImplementedError

    def get_next_letter(self, fragment):
        ''' Returns the computer player's next move '''
        raise NotImplementedError
    
    def get_word(self, fragment):
        ''' Returns a word should the computer player be challenged '''
        raise NotImplementedError

class SimpleGhostPlayer(GhostPlayer):

    def __init__(self):
        self.name = 'COMPUTER'

    def get_name(self):
        return self.name

    def get_next_letter(self, fragment):
        # always challenge if fragment is not a prefix
        if not lexicon.has_prefix(fragment):
            return '!'
        # choose a random next letter
        else:
            next_letter = random.choice(lexicon.valid_continuations(fragment))
            # if that next letter completes a word, challenge instead
            # for now, GhostPlayer does not know about Ghost._MIN_WORD_LENGTH
            if lexicon.has_word(fragment + next_letter): 
                return '!'
            # otherwise, just play that letter
            else:
                return next_letter
                           
    def get_word(self, fragment):
        # return any word with fragment as a prefix
        while not lexicon.has_word(fragment):
            next_letter = random.choice(lexicon.valid_continuations(fragment))
            fragment += next_letter
        return fragment


