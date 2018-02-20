import alNum_code as al
import tkinter
from tkinter import ttk


def main():
    c1 = al.Code()
    c1.initialize()
    sentence_window(c1)


def sentence_window(code):
    root = tkinter.Tk()
    root.title = 'Human window'
    frame = ttk.Frame(root, padding=50)
    frame.grid()

    instructions = ttk.Label(root, text='     Input letters that you wish to know the identity of.  You get as many '
                                        'hints as you want, but each hint speeds up the robot.  Each hint will display '
                                        'the letter with its corresponding number in the terminal     ')
    instructions.grid()
    inp_box = ttk.Entry(root, width='19')
    inp_box.grid()
    test = ttk.Button(root, text='enter')
    test['command'] = lambda: hint_test(inp_box, code)
    test.grid()
    instructions2 = ttk.Label(root, text='     The terminal will hold your results.     ')
    instructions2.grid()

    answer = 'i bless the rains down in africa'
    lAnswer = answer.split()
    question = []
    for k in range(len(lAnswer)):
        question.append(code.encode(lAnswer[k]))
    for k in range(len(question)):
        string = ttk.Label(root, text=str(question[k]))
        string.grid()
    instructions3 = ttk.Label(root, text='     Using your discovered letters, determine what the above string says'
                                         ' and type it into the box below, no punctuation or capitalization     ')
    instructions3.grid()

    entryFinal = ttk.Entry(root)
    entryFinal.grid()
    buttonFinal = ttk.Button(root, text='check sentance')
    buttonFinal['command'] = lambda: sentence_guess(entryFinal, answer)
    buttonFinal.grid()

    root.mainloop()


# button functions:


def hint_test(box, code):
    contents = box.get()

    for k in range(len(code.alphabet)):
        if code.alphabet[k][0] == contents:
            print(code.alphabet[k])


def sentence_guess(box, answer):
    contents = box.get()

    if contents == answer:
        print('********************     WIN     ********************')
    else:
        print('keep trying')



main()
