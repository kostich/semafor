#!/usr/bin/python3 -B

import sqlite3
from config import *

def checkanswer(questionnum, part, answer, window, checkbutton, label):
    conn = sqlite3.connect(programdir + '/data.db')
    c = conn.cursor()

    # Load the question
    query = 'SELECT correct_answers FROM ' + part + ' WHERE id = ' + questionnum
    c.execute(query)
    result = c.fetchall()
    correctanswer = str(result)
    correctanswer = correctanswer.replace('[(\'','')
    correctanswer = correctanswer.replace('\\n','\n')
    correctanswer = correctanswer.replace('\',)]','')
    correctanswer = correctanswer.splitlines()

    origanswer = answer # we need the answer with the chars at the end, for colorizing

    # remove , and . from answer because we added it and these chars aren't in data.db
    answer = answer[:-1]
    correctanswercount = len(correctanswer)

    #conn.close()
    if checkbutton.get_active(): #only if the button is actually marked
        if correctanswercount == 1:
            if answer == correctanswer[0]:
                label.set_markup("<span foreground='#269F19'>" +
                origanswer + "</span>")
                answer.set_disabled(True)
                return True
            else:
                label.set_markup("<span foreground='#B92300'>" +
                origanswer + "</span>")
                return False
        elif correctanswercount == 2:
            if answer == correctanswer[0] or answer == correctanswer[1]:
                label.set_markup("<span foreground='#269F19'>" +
                origanswer + "</span>")
                answer.set_disabled(True)
                return True
            else:
                label.set_markup("<span foreground='#B92300'>" +
                origanswer + "</span>")
                return False
        else:
            if answer == correctanswer[0] or answer == correctanswer[1] or \
        answer == correctanswer[2]:
                label.set_markup("<span foreground='#269F19'>" +
                origanswer + "</span>")
                answer.set_disabled(True)
                return True
            else:
                label.set_markup("<span foreground='#B92300'>" +
                origanswer + "</span>")
                return False

    conn.close()
