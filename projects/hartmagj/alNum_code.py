import random

# the alphabet list that will be used to store the code
alphabet = [['a', 0], ['b', 0], ['c', 0], ['d', 0], ['e', 0], ['f', 0], ['g', 0], ['h', 0], ['i', 0], ['j', 0],
            ['k', 0], ['l', 0], ['m', 0], ['n', 0], ['o', 0], ['p', 0], ['q', 0], ['r', 0], ['s', 0], ['t', 0],
            ['u', 0], ['v', 0], ['w', 0], ['x', 0], ['y', 0], ['z', 0]]
# a list of numbers to help with the generation process
alNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

# the object that stores the codes


class Code(object):
    def __init__(self):
        # pass through the alphabet, the number list, and another variable that is used in the human side code
        self.alphabet = [['a', 0], ['b', 0], ['c', 0], ['d', 0], ['e', 0], ['f', 0], ['g', 0], ['h', 0], ['i', 0],
                         ['j', 0], ['k', 0], ['l', 0], ['m', 0], ['n', 0], ['o', 0], ['p', 0], ['q', 0], ['r', 0],
                         ['s', 0], ['t', 0], ['u', 0], ['v', 0], ['w', 0], ['x', 0], ['y', 0], ['z', 0]]
        self.alNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        self.words_cracked = 0

    def __repr__(self):
        # we want the alphabet displayed when the object is printed
        return str(self.alphabet)

    # function to create the code
    def initialize(self):
        # cycle through the alphabet
        for k in range(len(self.alphabet)):
            # get a random integer in the range of the number list
            code = random.randint(0, len(self.alNum) - 1)
            # set the number component of each alphabet to the randomized number
            self.alphabet[k][1] = self.alNum[code]
            # remove the randomized number from the number list to avoid assigning the same number to multiple letters
            self.alNum.remove(self.alNum[code])

    # function to convert any string (without spaces) into a coded message
    def encode(self, message):
        # the message to return
        encMessage = []
        # cycle through the string parameter
        for k in range(len(message)):
            # cycle through the alphabet
            for i in range(len(self.alphabet)):
                # if the current message letter is the same as the current alphabet letter
                if message[k] == self.alphabet[i][0]:
                    # add the number that correlates to that letter to the returned message
                    encMessage.append(self.alphabet[i][1])

        return encMessage
