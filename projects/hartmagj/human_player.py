import alNum_code as al
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import time


class Delegate(object):
    def __init__(self):
        self.running = True

    def print_robot_message(self, message):
        self.label.configure(text=message)

    def set_label(self, label):
        self.label = label


def main():
    print('start')
    my_delegate = Delegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    print('connected')
    c1 = al.Code()
    c1.initialize()
    time.sleep(5)
    print('before message')
    mqtt_client.send_message('handle_code', [c1.alphabet])
    print('after message')

    sentence_window(c1, mqtt_client, my_delegate)


def sentence_window(code, client, my_delegate):
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
    test['command'] = lambda: hint_test(inp_box, code, client)
    test.grid()
    instructions2 = ttk.Label(root, text='     The terminal will hold your results.     ')
    instructions2.grid()

    answer = 'the rest is noise'
    lAnswer = answer_split(answer, client)
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
    buttonFinal = ttk.Button(root, text='check sentence')
    buttonFinal['command'] = lambda: sentence_guess(entryFinal, answer)
    buttonFinal.grid()

    robot_messages = ttk.Label(root, text='     Robot messages will show up here     ')
    robot_messages.grid()

    my_delegate.set_label(robot_messages)

    root.mainloop()


# button functions:


def hint_test(box, code, client):
    contents = box.get()

    for k in range(len(code.alphabet)):
        if code.alphabet[k][0] == contents:
            print(code.alphabet[k])

    client.send_message('speed_up')


def sentence_guess(box, answer):
    contents = box.get()

    if contents == answer:
        print('********************     WIN     ********************')
    else:
        print('keep trying')


def answer_split(string, client):
    lAnswer = string.split()
    client.send_message('handle_key', [lAnswer])
    print('key sent')
    return lAnswer



main()
