import random

alphabet = [['a', 0], ['b', 0], ['c', 0], ['d', 0], ['e', 0], ['f', 0], ['g', 0], ['h', 0], ['i', 0], ['j', 0],
            ['k', 0], ['l', 0], ['m', 0], ['n', 0], ['o', 0], ['p', 0], ['q', 0], ['r', 0], ['s', 0], ['t', 0],
            ['u', 0], ['v', 0], ['w', 0], ['x', 0], ['y', 0], ['z', 0]]
alNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]


def main():
    code_initializer()
    print(alphabet)
    print('apple')
    z = encode('apple')
    print(z)
    x = decode(z)
    print(x)


def code_initializer():
    for k in range(len(alphabet)):
        code = random.randint(0, len(alNum) - 1)
        alphabet[k][1] = alNum[code]
        alNum.remove(alNum[code])


def encode(message):
    encMessage = []
    for k in range(len(message)):
        for i in range(len(alphabet)):
            if message[k] == alphabet[i][0]:
                encMessage.append(alphabet[i][1])

    return encMessage


def decode(numList):
    decMessage = ''
    for k in range(len(numList)):
        for i in range(len(alphabet)):
            if numList[k] == alphabet[i][1]:
                decMessage += alphabet[i][0]

    return decMessage


main()
