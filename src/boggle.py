#sowpods from https://www.wordgamedictionary.com/sowpods/download/sowpods.txt
#compare to https://www.toptal.com/java/the-trie-a-neglected-data-structure
#itertools
#namedtuple
#pickle
#

import numpy as np
import random
from collections import defaultdict

#trie node data structure
#replace with namedtuple
#class Trie_Node:
#    def __init__(self):
#        self.children = {}
#        self.is_word = False
#        self.count = 0

#make trie of all English words
def make_trie(mydict='sowpods'):
    trie_head = {'children':{}, 'is_word':False}
    if mydict is not 'sowpods':
        raise ValueError('Not programmed for dictionary ' + mydict + '.')
    mydict = open('../data/' + mydict + '.txt')
    for nline,line in enumerate(mydict.readlines()):
        if nline < 6:
            continue
        word = line.strip()
        curr_node = trie_head
        for ichar in word:
            if ichar not in curr_node['children']:
                curr_node['children'][ichar] = {'children':{}, 'is_word':False}
            curr_node = curr_node['children'][ichar]
        curr_node['is_word'] = True
    #insert pickle here
    return trie_head

#check if word is in trie
def check_word(word):
    curr_node = trie_head
    for ichar in word:
        if ichar not in curr_node['children']:
            return False
        curr_node = curr_node['children'][ichar]
    return curr_node['is_word']

#class managing dice
class Die:
    #create die with given sides
    def __init__(self, sides):
        if len(sides) != 6:
            raise ValueError('Die {} should have six sides.'.format(sides))
        self.sides = sides
    #roll the die
    def roll(self):
        return random.choice(self.sides)
    
#class managing board
class Board:

    #initialize NxM boggle board - defaults to 4x4
    def __init__(self, dice='standard', n=4, m=4, qu_pip = True):
        if dice is not 'standard':
            raise ValueError('Not currently programmed for nonstandard dice.')
        self.trie_head = make_trie()
        self.dice = [Die([ichar for ichar in die.strip()]) for die in open('../data/' + dice + '_dice.txt', 'r')]
        self.n = n
        self.m = m
        if len(self.dice) != n*m:
            raise ValueError('Number of dice {} not equal to {}x{}. Please add dice or change grid dimensions.'.format(len(dice),n,m))
        self.qu_pip = qu_pip

    #shake board
    def shake(self):
        random.shuffle(self.dice)
        self.grid = []
        for die in self.dice:
            self.grid.append(die.roll())
        self.grid = np.reshape(self.grid,[self.n,self.m])

    #recursive fn that checks if pattern 'word' is a word
    def find_words_from(self, i, j, curr_node, word = None, visited = None):
        if visited is None:
            visited = np.zeros([self.n, self.m])
        if word is None:
            word = []
        visited[i][j] = 1
        word.append(self.grid[i][j])
        child_node = curr_node['children'][self.grid[i][j]]
        if self.qu_pip and self.grid[i][j] == 'q':
            if 'u' not in child_node['children']:
                return
            word.append('u')
            child_node = child_node['children']['u']
        if child_node['is_word']:
            self.words.append(''.join(word))
        #keep dict of neighbors:locations
        for ineigh in range(max(0, i - 1), min(i + 2, self.n)):
            for jneigh in range(max(0, j - 1), min(j + 2, self.m)):
                if ineigh == i and jneigh == j:
                    continue
                ichar = self.grid[ineigh][jneigh]
                if (visited[ineigh][jneigh] == 0) and (ichar in child_node['children']):
                    self.find_words_from(ineigh, jneigh, child_node, word = word, visited = np.copy(visited))
                    
    #finds all words in current board arrangement using recursive fn above
    def find_words(self):
        self.words = []
        for i in range(self.n):
            for j in range(self.m):
                self.find_words_from(i, j, self.trie_head)
        return sorted(self.words)

    def score(self, scoring="standard"):
        if scoring is not 'standard':
            raise ValueError('Not currently programmed for non-standard scoring.')
        scoring_dict = {0:0,1:0,2:0,3:1,4:1,5:2,6:3,7:5}
        scoring_dict = defaultdict(lambda:11, scoring_dict)
        score = 0
        for word in self.words:
            score += scoring_dict[len(word)]
        return score

def main(ngames):
    board = Board()
    counts = defaultdict(int)
    scores = []
    for i in range(ngames):
        board.shake()
        for word in board.find_words():
            counts[word] += 1
        scores.append(board.score())
    return scores, counts
if __name__ == '__main__': main()
