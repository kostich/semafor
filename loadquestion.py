#!/usr/bin/python3 -B

import os, sys, sqlite3, tempfile

from config import *
from checkanswer import *
from random import shuffle

def loadquestion(questionnum, part, window):
    conn = sqlite3.connect(programdir + '/data.db')
    c = conn.cursor()

    # Load the question
    query = 'SELECT question FROM ' + part + ' WHERE id = ' + questionnum
    c.execute(query)
    result = c.fetchall()
    question = str(result)
    question = question.replace('[(\'','')
    question = question.replace('\\n','\n')
    question = question.replace('\',)]','')
    window.question.set_markup(questionnum + '. ' + question)

    # Uncheck all the answers and enable them
    window.answer1.set_active(False)
    window.answer2.set_active(False)
    window.answer3.set_active(False)
    window.answer4.set_active(False)
    window.answer5.set_active(False)
    window.answer6.set_active(False)

    # Reflow the images
    query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
    try:
        c.execute(query)
    except sqlite3.OperationalError:
        # If there is error, solutions column does not exist and that means
        # that this part doesn't have images so we hide picturegrid.
        window.picturegrid.hide()

    result = c.fetchall()
    if len(str(result).split('\\n')) == 3:
        # pic1 pic2 pic3
        window.picturegrid.show()
        window.image1 = window.questionbuilder.get_object("image11")
        window.image2 = window.questionbuilder.get_object("image12")
        window.image3 = window.questionbuilder.get_object("image13")
        # Image widgets bellow are not needed so we hide them
        window.image4 = window.questionbuilder.get_object("image21")
        window.image5 = window.questionbuilder.get_object("image22")
        window.image6 = window.questionbuilder.get_object("image23")
        window.image4.hide()
        window.image5.hide()
        window.image6.hide()

        window.solution1 = window.questionbuilder.get_object("solution11")
        window.solution2 = window.questionbuilder.get_object("solution12")
        window.solution3 = window.questionbuilder.get_object("solution13")
        # Solution labels bellow are not needed so we hide them
        window.solution4 = window.questionbuilder.get_object("solution21")
        window.solution5 = window.questionbuilder.get_object("solution22")
        window.solution6 = window.questionbuilder.get_object("solution23")
        window.solution4.hide()
        window.solution5.hide()
        window.solution6.hide()
    elif len(str(result).split('\\n')) > 4:
        # pic1 pic2 pic3
        # pic4 pic5 pic6
        window.picturegrid.show()
        window.image1 = window.questionbuilder.get_object("image11")
        window.image2 = window.questionbuilder.get_object("image12")
        window.image3 = window.questionbuilder.get_object("image13")
        window.image4 = window.questionbuilder.get_object("image21")
        window.image5 = window.questionbuilder.get_object("image22")
        window.image6 = window.questionbuilder.get_object("image23")

        window.solution1 = window.questionbuilder.get_object("solution11")
        window.solution2 = window.questionbuilder.get_object("solution12")
        window.solution3 = window.questionbuilder.get_object("solution13")
        window.solution4 = window.questionbuilder.get_object("solution21")
        window.solution5 = window.questionbuilder.get_object("solution22")
        window.solution6 = window.questionbuilder.get_object("solution23")
    else:
        # pic1
        #  OR
        # pic1 pic2
        #  OR
        # pic1 pic2
        # pic3 pic4
        window.picturegrid.show()
        window.image1 = window.questionbuilder.get_object("image11")
        window.image2 = window.questionbuilder.get_object("image12")
        window.image3 = window.questionbuilder.get_object("image21")
        window.image4 = window.questionbuilder.get_object("image22")
        # Image widgets bellow are not needed so we hide them
        window.image5 = window.questionbuilder.get_object("image13")
        window.image6 = window.questionbuilder.get_object("image23")
        window.image5.hide()
        window.image6.hide()

        window.solution1 = window.questionbuilder.get_object("solution11")
        window.solution2 = window.questionbuilder.get_object("solution12")
        window.solution3 = window.questionbuilder.get_object("solution21")
        window.solution4 = window.questionbuilder.get_object("solution22")
        # Solution labels bellow are not needed so we hide them
        window.solution5 = window.questionbuilder.get_object("solution13")
        window.solution6 = window.questionbuilder.get_object("solution23")
        window.solution5.hide()
        window.solution6.hide()

    # Load the solutions (pics + labels)
    try:
        window.image1.show()
        query = 'SELECT picture1 FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        picture = c.fetchone()[0]
        if picture == None:
            raise sqlite3.OperationalError
        # We have to do this because of the bug in NamedTemporaryFile
        # on Windows. https://bugs.python.org/issue14243#msg155278
        if os.name == "nt":
            f = tempfile.NamedTemporaryFile('wb', delete=False)
            f.write(picture)
            f.close()
            window.image1.set_from_file(f.name)
            os.remove(f.name)
        elif os.name == "posix":
            f = tempfile.NamedTemporaryFile('wb')
            f.write(picture)
            window.image1.set_from_file(f.name)
            f.close()
    except sqlite3.OperationalError:
        window.image1.hide()

    try:
        window.solution1.show()
        query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        result = c.fetchall()
        if str(result) == '[(None,)]':
            raise sqlite3.OperationalError
        elif len(str(result).split('\\n')) < 1:
            raise sqlite3.OperationalError
        else:
            solution = str(result).split('\\n')
            solution = str(solution[0])
            solution = solution.replace('[(\'','')
            solution = solution.replace('\',)]','')
            window.solution1.set_label(solution)
    except sqlite3.OperationalError:
        window.solution1.hide()

    try:
        window.image2.show()
        query = 'SELECT picture2 FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        picture = c.fetchone()[0]
        if picture == None:
            raise sqlite3.OperationalError
        # We have to do this because of the bug in NamedTemporaryFile
        # on Windows. https://bugs.python.org/issue14243#msg155278
        if os.name == "nt":
            f = tempfile.NamedTemporaryFile('wb', delete=False)
            f.write(picture)
            f.close()
            window.image2.set_from_file(f.name)
            os.remove(f.name)
        elif os.name == "posix":
            f = tempfile.NamedTemporaryFile('wb')
            f.write(picture)
            window.image2.set_from_file(f.name)
            f.close()
    except sqlite3.OperationalError:
        window.image2.hide()

    try:
        window.solution2.show()
        query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        result = c.fetchall()
        if str(result) == '[(None,)]':
            raise sqlite3.OperationalError
        elif len(str(result).split('\\n')) < 2:
            raise sqlite3.OperationalError
        else:
            solution = str(result).split('\\n')
            solution = str(solution[1])
            solution = solution.replace('[(\'','')
            solution = solution.replace('\',)]','')
            window.solution2.set_label(solution)
    except sqlite3.OperationalError:
        window.solution2.hide()

    try:
        window.image3.show()
        query = 'SELECT picture3 FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        picture = c.fetchone()[0]
        if picture == None:
            raise sqlite3.OperationalError
        # We have to do this because of the bug in NamedTemporaryFile
        # on Windows. https://bugs.python.org/issue14243#msg155278
        if os.name == "nt":
            f = tempfile.NamedTemporaryFile('wb', delete=False)
            f.write(picture)
            f.close()
            window.image3.set_from_file(f.name)
            os.remove(f.name)
        elif os.name == "posix":
            f = tempfile.NamedTemporaryFile('wb')
            f.write(picture)
            window.image3.set_from_file(f.name)
            f.close()
    except sqlite3.OperationalError:
        window.image3.hide()

    try:
        window.solution3.show()
        query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        result = c.fetchall()
        if str(result) == '[(None,)]':
            raise sqlite3.OperationalError
        elif len(str(result).split('\\n')) < 3:
            raise sqlite3.OperationalError
        else:
            solution = str(result).split('\\n')
            solution = str(solution[2])
            solution = solution.replace('[(\'','')
            solution = solution.replace('\',)]','')
            window.solution3.set_label(solution)
    except sqlite3.OperationalError:
        window.solution3.hide()

    try:
        window.image4.show()
        query = 'SELECT picture4 FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        picture = c.fetchone()[0]
        if picture == None:
            raise sqlite3.OperationalError
        # We have to do this because of the bug in NamedTemporaryFile
        # on Windows. https://bugs.python.org/issue14243#msg155278
        if os.name == "nt":
            f = tempfile.NamedTemporaryFile('wb', delete=False)
            f.write(picture)
            f.close()
            window.image4.set_from_file(f.name)
            os.remove(f.name)
        elif os.name == "posix":
            f = tempfile.NamedTemporaryFile('wb')
            f.write(picture)
            window.image4.set_from_file(f.name)
            f.close()
    except sqlite3.OperationalError:
        window.image4.hide()

    try:
        window.solution4.show()
        query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        result = c.fetchall()
        if str(result) == '[(None,)]':
            raise sqlite3.OperationalError
        elif len(str(result).split('\\n')) < 4:
            raise sqlite3.OperationalError
        else:
            solution = str(result).split('\\n')
            solution = str(solution[3])
            solution = solution.replace('[(\'','')
            solution = solution.replace('\',)]','')
            window.solution4.set_label(solution)
    except sqlite3.OperationalError:
        window.solution4.hide()

    try:
        window.image5.show()
        query = 'SELECT picture5 FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        picture = c.fetchone()[0]
        if picture == None:
            raise sqlite3.OperationalError
        # We have to do this because of the bug in NamedTemporaryFile
        # on Windows. https://bugs.python.org/issue14243#msg155278
        if os.name == "nt":
            f = tempfile.NamedTemporaryFile('wb', delete=False)
            f.write(picture)
            f.close()
            window.image5.set_from_file(f.name)
            os.remove(f.name)
        elif os.name == "posix":
            f = tempfile.NamedTemporaryFile('wb')
            f.write(picture)
            window.image5.set_from_file(f.name)
            f.close()
    except sqlite3.OperationalError:
        window.image5.hide()

    try:
        window.solution5.show()
        query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        result = c.fetchall()
        if str(result) == '[(None,)]':
            raise sqlite3.OperationalError
        elif len(str(result).split('\\n')) < 5:
            raise sqlite3.OperationalError
        else:
            solution = str(result).split('\\n')
            solution = str(solution[4])
            solution = solution.replace('[(\'','')
            solution = solution.replace('\',)]','')
            window.solution5.set_label(solution)
    except sqlite3.OperationalError:
        window.solution5.hide()

    try:
        window.image6.show()
        query = 'SELECT picture6 FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        picture = c.fetchone()[0]
        if picture == None:
            raise sqlite3.OperationalError
        # We have to do this because of the bug in NamedTemporaryFile
        # on Windows. https://bugs.python.org/issue14243#msg155278
        if os.name == "nt":
            f = tempfile.NamedTemporaryFile('wb', delete=False)
            f.write(picture)
            f.close()
            window.image6.set_from_file(f.name)
            os.remove(f.name)
        elif os.name == "posix":
            f = tempfile.NamedTemporaryFile('wb')
            f.write(picture)
            window.image6.set_from_file(f.name)
            f.close()
    except sqlite3.OperationalError:
        window.image6.hide()

    try:
        window.solution6.show()
        query = 'SELECT solutions FROM ' + part + ' WHERE id = ' + questionnum
        c.execute(query)
        result = c.fetchall()
        if str(result) == '[(None,)]':
            raise sqlite3.OperationalError
        elif len(str(result).split('\\n')) < 6:
            raise sqlite3.OperationalError
        else:
            solution = str(result).split('\\n')
            solution = str(solution[5])
            solution = solution.replace('[(\'','')
            solution = solution.replace('\',)]','')
            window.solution6.set_label(solution)
    except sqlite3.OperationalError:
        window.solution6.hide()

    # Load the answers
    query = 'SELECT possible_answers FROM ' + part + ' WHERE id = ' +questionnum
    c.execute(query)
    answers = c.fetchall()
    # Randomize the answers
    answers = str(answers).split('\\n')
    shuffle(answers)

    try:
        window.answer1.show()
        answer = str(answers[0])
        answer = answer.replace('[(\'','')
        answer = answer.replace('\',)]','')
        window.label1.set_label(answer + ',')
    except IndexError:
        window.answer1.hide()

    try:
        window.answer2.show()
        answer = str(answers[1])
        answer = answer.replace('[(\'','')
        answer = answer.replace('\',)]','')
        window.label2.set_label(answer + ',')
    except IndexError:
        window.answer2.hide()
        try:
            previousanswer = str(answers[0])
            previousanswer = previousanswer.replace('[(\'','')
            previousanswer = previousanswer.replace('\',)]','')
            window.label1.set_label(previousanswer + '.')
        except IndexError:
            pass

    try:
        window.answer3.show()
        answer = str(answers[2])
        answer = answer.replace('[(\'','')
        answer = answer.replace('\',)]','')
        window.label3.set_label(answer + ',')
    except IndexError:
        window.answer3.hide()
        try:
            previousanswer = str(answers[1])
            previousanswer = previousanswer.replace('[(\'','')
            previousanswer = previousanswer.replace('\',)]','')
            window.label2.set_label(previousanswer + '.')
        except IndexError:
            pass

    try:
        window.answer4.show()
        answer = str(answers[3])
        answer = answer.replace('[(\'','')
        answer = answer.replace('\',)]','')
        window.label4.set_label(answer + ',')
    except IndexError:
        window.answer4.hide()
        try:
            previousanswer = str(answers[2])
            previousanswer = previousanswer.replace('[(\'','')
            previousanswer = previousanswer.replace('\',)]','')
            window.label3.set_label(previousanswer + '.')
        except IndexError:
            pass

    try:
        window.answer5.show()
        answer = str(answers[4])
        answer = answer.replace('[(\'','')
        answer = answer.replace('\',)]','')
        window.label5.set_label(answer + ',')
    except IndexError:
        window.answer5.hide()
        try:
            previousanswer = str(answers[3])
            previousanswer = previousanswer.replace('[(\'','')
            previousanswer = previousanswer.replace('\',)]','')
            window.label4.set_label(previousanswer + '.')
        except IndexError:
            pass

    try:
        window.answer6.show()
        answer = str(answers[5])
        answer = answer.replace('[(\'','')
        answer = answer.replace('\',)]','')
        window.label6.set_label(answer + '.')
    except IndexError:
        window.answer6.hide()
        try:
            previousanswer = str(answers[4])
            previousanswer = previousanswer.replace('[(\'','')
            previousanswer = previousanswer.replace('\',)]','')
            window.label5.set_label(previousanswer + '.')
        except IndexError:
            pass

    conn.close()
