from model.test import test
from controller.webServices import webServices

class testController():
    def createTest(hill, city):
        vytvorenyTest = test(0, hill, city)

    def addQuestion(pointA, pointB):
        webServices.findDistance(pointA, pointB)

        print("Question len: " + str(test.questions.__len__()))