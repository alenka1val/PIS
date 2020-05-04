import re

class testFromDB():
    questions = []
    sucasna_otazka = 0
    body = 0
    bodyCelkovo = 0
    dalsi = 1

    def __init__(self, otazky):
        testFromDB.questions = otazky
        testFromDB.sucasna_otazka = 0
        testFromDB.dalsi = 1
        testFromDB.body = 0
        testFromDB.bodyCelkovo = 0


    def setPoints(odpoved):
        print('odpoved je: ', odpoved)
        vzdialenost = re.sub(' ', '', testFromDB.questions[testFromDB.sucasna_otazka][4])
        real = float(vzdialenost)
        real = int(real)
        uhadnute = int(odpoved)
        if real == 0:
            real = 0.00000000000000001
        if uhadnute == 0:
            uhadnute = 0.00000000000000001

        if abs(real - uhadnute) <= real:
            if uhadnute > real:
                sucasneBody = (real * 100) / uhadnute
            else:
                sucasneBody = (uhadnute * 100) / real
        else:
            sucasneBody = 0

        testFromDB.bodyCelkovo += sucasneBody
        testFromDB.body = testFromDB.bodyCelkovo/len(testFromDB.questions)
        print('r: ', real, ' u: ', uhadnute, ' b: ', sucasneBody)

        testFromDB.sucasna_otazka += 1
        if testFromDB.sucasna_otazka >= len(testFromDB.questions):
            testFromDB.dalsi = 0