import alNum_code as al
import tkinter
from tkinter import ttk


def main():
    c1 = al.Code()
    c1.initialize()
    math_window(c1)
    sentance_window(c1)


def math_window(code):
    root = tkinter.Tk()
    root.title = 'First phase: hints'
    frame = ttk.Frame(root, padding=50)
    frame.grid()
    instructions = ttk.Label(root, text='     Answer these questions (they should be numbers) and enter the answers in '
                                        'order, separated by spaces only.     ')
    instructions.grid()
    warning = ttk.Label(root, text='     Hurry up, the robot has already begun decoding the riddles.     ')
    warning.grid()
    calc1 = ttk.Label(root, text='     15 / 3 = ?     ') #5
    calc1.grid()
    calc2 = ttk.Label(root, text='     (417 - 313) / 4 = ?     ') #26
    calc2.grid()
    calc3 = ttk.Label(root, text='     Derivative of:  15x^2 - 10x  , where x = 1, = ?     ') #20
    calc3.grid()
    calc4 = ttk.Label(root, text='     The seventh number in the fibonacci sequence = ?     ') #13
    calc4.grid()
    calc5 = ttk.Label(root, text='     The legal drinking age in the U.S. = ?     ') #21
    calc5.grid()
    calc6 = ttk.Label(root, text='     Number of bits in a byte = ?     ') #8
    calc6.grid()
    calc7 = ttk.Label(root, text='     2^16 / 2^15 = ?     ') #2
    calc7.grid()
    calc8 = ttk.Label(root, text='     The last of the teenage years = ?') #19
    calc8.grid()
    calc9 = ttk.Label(root, text='     The first number that appears in this window = ?     ') #15
    calc9.grid()
    inp_box = ttk.Entry(root, width='19')
    inp_box.grid()
    test = ttk.Button(root, text='enter')
    test['command'] = lambda: math_test(inp_box, code)
    test.grid()
    instructions2 = ttk.Label(root, text='     The terminal will hold your results.  Close this window to continue.    '
                                         ' ')
    instructions2.grid()

    root.mainloop()


def sentance_window(code):
    root = tkinter.Tk()
    root.title = 'Second phase: code breaking'
    frame = ttk.Frame(root, padding=50)
    frame.grid()

    answer = 'the robot never stood a chance'
    lAnswer = answer.split()
    question = []
    for k in range(len(lAnswer)):
        question.append(code.encode(lAnswer[k]))

    string = ttk.Label(root, text=str(question))
    string.grid()
    instructions = ttk.Label(root, text='     Using your discovered letters, determine what the above string says'
                                        ' and type it word by word into the boxes below, no punctuation or '
                                        'capitalization     ')
    instructions.grid()

    entry1 = ttk.Entry(root)
    entry1.grid()
    button1 = ttk.Button(root, text='test word 1')
    button1['command'] = lambda: word_guess(entry1, lAnswer[0], 1, code)
    button1.grid()

    entry2 = ttk.Entry(root)
    entry2.grid()
    button2 = ttk.Button(root, text='test word 2')
    button2['command'] = lambda: word_guess(entry2, lAnswer[1], 2, code)
    button2.grid()

    entry3 = ttk.Entry(root)
    entry3.grid()
    button3 = ttk.Button(root, text='test word 3')
    button3['command'] = lambda: word_guess(entry3, lAnswer[2], 3, code)
    button3.grid()

    entry4 = ttk.Entry(root)
    entry4.grid()
    button4 = ttk.Button(root, text='test word 4')
    button4['command'] = lambda: word_guess(entry4, lAnswer[3], 4, code)
    button4.grid()

    entry5 = ttk.Entry(root)
    entry5.grid()
    button5 = ttk.Button(root, text='test word 5')
    button5['command'] = lambda: word_guess(entry5, lAnswer[4], 5, code)
    button5.grid()

    entry6 = ttk.Entry(root)
    entry6.grid()
    button6 = ttk.Button(root, text='test word 6')
    button6['command'] = lambda: word_guess(entry6, lAnswer[5], 6, code)
    button6.grid()

    entryFinal = ttk.Entry(root)
    entryFinal.grid()
    buttonFinal = ttk.Button(root, text='check sentance')
    buttonFinal['command'] = lambda: sentance_guess(entryFinal, answer)
    buttonFinal.grid()

    root.mainloop()


# button functions:


def math_test(box, code):
    contents = box.get()
    hint = []
    if contents == '5 26 20 13 21 8 2 19 15':
        c = contents.split()
        for k in range(len(c)):
            for i in range(len(code.alphabet)):
                if int(c[k]) == code.alphabet[i][1]:
                    hint.append(code.alphabet[i][0])
        print(hint)
        print('These are the letters that go with your answers, use them in the next phase')
        print('I suggest writing these down')
    else:
        print('try again')


def word_guess(box, ans, n, code):
    contents = box.get()

    if contents == ans:
        print('word ' + str(n) + ': correct')
        code.words_cracked += 1
    else:
        print('try again')
    print(code.words_cracked)


def sentance_guess(box, answer):
    contents = box.get()

    if contents == answer:
        print('********************     WIN     ********************')
    else:
        print('keep trying')



main()
