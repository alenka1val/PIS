from model.test import test
from view.questionForm import questionForm


class testController():
    def createTest(settings, hill, city):
        vytvorenyTest = test(0, hill, city)

        settings.destroy()
        app = questionForm(master=settings.master)


