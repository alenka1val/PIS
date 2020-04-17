class test():
    status = ''
    hill = ''
    town = ''
    questions = []

    def __init__(self, status, hill, town):
        test.status = status
        test.hill = hill
        test.town = town
        test.questions = []

        print(status, ' ', hill, ' ', town)

    def addQuestion(question):
        test.questions.append(question)

    def printTest():
        print('vypisujem nastavenia testu:', test.status, ' ', test.hill, ' ', test.town)