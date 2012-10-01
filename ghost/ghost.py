'''
Ghost.py
Plays the game Ghost. Opponent can be either human or computer.
'''

import string
import lexicon
from ghostplayer import SimpleGhostPlayer

YES_STRINGS = ['', 'y', 'yes', 'yep', 'yea', 'ok', 'sure', 'okay']
NO_STRINGS = ['n', 'no', 'nah', 'naw', 'nope', 'never']

class Ghost(object):
    ''' Plays the game Ghost '''

    _FORMED_WORD = 0
    _WON_CHALLENGE = 1 
    _LOST_CHALLENGE = 2
    _MIN_WORD_LENGTH = 3
    _WELCOME_MESSAGE = '''Welcome to Ghost!
You and your opponent will add letters to a growing word fragment
Choose your letters carefully. The word fragment has to be the beginning
of a word, without being a word itself. Walk this tightrope of ambiguity 
carefully. First one to fall off loses!  

Tip: The game will check if the fragment is a word, but it will not
check if the fragment is the beginning of a word. If you suspect your
opponent is bluffing, type '!' to challenge them.

Note: The game only checks for words that have 3 or more letters. The 
Scrabble dictionary is littered with annoyingly obscure 2 words.
'''
    def __init__(self):
        self._names = ['', '']
        self._wins = [0, 0]
        self._prev_winner = 0
        self._prev_loser = 1
        self._games_played = 0
        
    def play(self):
        ''' Plays one or more games of Ghost '''
        self.welcome()
        self.play_game()
        while self.yes_or_no('Play again? '):
            self.play_game()
        self.display_stats()

    def welcome(self):
        ''' Sets up the game: user names, play against computer, etc. '''
        print Ghost._WELCOME_MESSAGE        
        self._names[0] = raw_input('Player 1, choose your name: ').strip()
        self._play_computer = \
            self.yes_or_no('Play against a computer opponent? ')
        if self._play_computer:
            self._computer = SimpleGhostPlayer()
            self._names[1] = self._computer.get_name()
        else:
            self._names[1] = raw_input('Player 2, choose your name: ').strip()
        self._max_name_length = max(len(name) for name in self._names)
        
    def play_game(self):
        ''' Plays one game of Ghost '''
        print
        print '- Game {0} -'.format(self._games_played + 1)
        fragment = ''
        current, opponent = \
            self._prev_loser, self._prev_winner # loser goes first
        # play turns
        while True: 
            letter = self.get_next_letter(current, fragment)
            # just adding a letter
            if letter != '!':
                fragment += letter
                if lexicon.has_word(fragment, Ghost._MIN_WORD_LENGTH):
                    result = Ghost._FORMED_WORD
                    break
            # a challenge was issued
            else:
                word = self.get_word(opponent, fragment)
                if word[:len(fragment)] == fragment and lexicon.has_word(word):
                    result = self.__class__._LOST_CHALLENGE
                else:
                    result = Ghost._WON_CHALLENGE
                break
            current, opponent = opponent, current
        self.process_result(current, opponent, fragment, result)
        self._games_played += 1

    def get_next_letter(self, player, fragment):
        ''' Gets the next move from the current player '''
        name = self._names[player]
        prompt = "{0}'s turn.".format(name).ljust(self._max_name_length + 10)
        prompt += 'Current fragment: {0}'.format(fragment)
        while True:
            # if the player is the computer
            if player == 1 and self._play_computer:
                letter = self._computer.get_next_letter(fragment)
                print prompt + letter
            # if the player is human
            else:
                letter = raw_input(prompt).strip()
            # validating the input
            if letter == '!' and not fragment:
                print '\tCannot challenge on the first turn'
            elif len(letter) != 1 or (letter not in string.letters + '!'):
                print "\tEnter a single letter or '!'"
            else:
                break
        return letter.lower() # the lexicon is all lowercase

    def get_word(self, player, fragment):
        ''' Gets a word from a player who has been challenged '''
        print "\t{0}, you've been challenged!".format(self._names[player])
        prompt = '\tEnter a word that begins with the current fragment: '
        if player == 1 and self._play_computer:
            word = self._computer.get_word(fragment)
            print prompt + word
        else: 
            word = raw_input(prompt)           
        return word.strip()

    def process_result(self, player, opponent, fragment, result):
        ''' Prints the result of a game '''
        print '{0},'.format(self._names[player]),
        if result == Ghost._FORMED_WORD:
            self._prev_winner, self._prev_loser = opponent, player
            print "you lost because '{0}' is a word.".format(fragment)
        elif result == Ghost._WON_CHALLENGE:
            self._prev_winner, self._prev_loser =  player, opponent
            print 'you won because your opponent could not repel your challenge!'
        elif result == Ghost._LOST_CHALLENGE:
            self._prev_winner, self._prev_loser = opponent, player
            print 'you lost because your opponent repelled your challenge.'
        else:
            'Something went wrong here...'
        print
        self._wins[self._prev_winner] += 1

    def yes_or_no(self, prompt):
        ''' Helper function for yes/no questions '''
        while True:
            answer = raw_input(prompt).strip().lower()    
            if answer in YES_STRINGS:
                return True
            elif answer in NO_STRINGS:
                return False
            else:
                print "\tType 'yes' or 'no'" 

    def display_stats(self):
        ''' Prints win tallies for all the games '''
        print
        print '- Final Score -'
        print '{0}  {1} - {2}  {3}'.format(self._names[0], self._wins[0],\
                                               self._wins[1], self._names[1])

if __name__ == '__main__':
    Ghost().play()

