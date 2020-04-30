from zeep import Client
from zeep.transports import Transport
from model.test import test
from model.testForKnowledge import testFromDB
from model.question import question
import time
import random

class webServices():
    mesta = None
    vrchy = None
    vzdialenost = None
    ukladanie = None
    stop = True

    def setWebServices():
        transport = Transport(timeout=5)
        nieco = 0
        while nieco == 0:
            try:
                webServices.mesta = Client('http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Cities?WSDL',transport=transport)
                nieco = 1
                print('nastavene WSDL mesta')
                break
            except Exception:
                print('chyba inicializacie miest')
                time.sleep(1)

        nieco = 0
        while nieco == 0:
            try:
                webServices.vrchy = Client('http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Peaks?WSDL',transport=transport)
                nieco = 1
                print('nastavene WSDL vrchy')
                break
            except Exception:
                print('chyba inicializacie vrchov')
                time.sleep(1)

        nieco = 0
        while nieco == 0:
            try:
                webServices.vzdialenost = Client('http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Locations?WSDL',transport=transport)
                nieco = 1
                print('nastavene WSDL vzdialenosti')
                break
            except Exception:
                print('chyba inicializacie vzdialenosti')
                time.sleep(1)

        nieco = 0
        while nieco == 0:
            try:
                webServices.ukladanie = Client('http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team033Tests?WSDL',transport=transport)
                nieco = 1
                print('nastavene WSDL ukladania')
                break
            except Exception:
                print('chyba inicializacie ukladania')
                time.sleep(1)

    def setGP(nazov, typ):
        if typ == 'Mesto':
            nieco = 0

            for x in range (0, 5):
                try:
                    result = webServices.mesta.service.searchByName(nazov)
                    nieco = 1
                    print('preslo zistovanie lat a lon mesta')
                    break
                except Exception:
                    print('chyba zistovania mesta')
                time.sleep(1)

            if nieco == 1 :
                return result
            else:
                print('Nepodarilo sa zistit mesto.')
                return nazov

        elif typ == 'Vrch':
            nieco = 0

            for x in range (0, 5):
                try:
                    result = webServices.vrchy.service.searchByName(nazov)
                    nieco = 1
                    print('preslo zistovanie lat a lon vrchu')
                    break
                except Exception:
                    print('chyba zistovania vrchu')
                time.sleep(1)

            if nieco == 1 :
                return result
            else:
                print('Nepodarilo sa zistit vrchol.')
                return nazov


    def findDistance(point1, point2):
            nieco = 0

            for x in range(0, 5):
                try:
                    result = webServices.vzdialenost.service.distanceByGPS(point1.lat, point1.lon, point2.lat, point2.lon)
                    nieco = 1
                    print('preslo zistovanie vzdialenosti medzi zadanymi miestami')
                    break
                except Exception:
                    print('chyba zistovania vzdialenosti')
                time.sleep(1)

            if nieco == 1:
                print('Vzdialenost medzi', point1.name, 'a', point2.name, 'je:', result, 'm')
                quest = question(point1, point2, result)
                test.addQuestion(quest)
                test.printTest()
            else:
                print('Nepodarilo sa najst vzdialenost')
                return 'Nepodarilo sa najst vzdialenost'

    def saveTest():
        nieco = 0
        otazka = 1
        zaznamy = []
        zaznam = ''
        mnozstvo = len(test.questions)
        vrch = True
        mesto = True

        print('mnozstvo otazok: ', mnozstvo)
        print('nastavenia testu su:  vrch:', test.hill, ', mesto: ', test.town)

        if test.hill == '0':
            vrch = False
            print('Vrch je FALSE')
            print(vrch)
        else:
            print('Vrch je TRUE')

        status = test.status

        if test.town == '0':
            mesto = False

        for x in test.questions:
            zaznam = (x.point1.name + ' @ ' + x.point1.hint + ' @ ' + x.point2.name + ' @ ' + x.point2.hint + ' @ ' + str(x.answer))
            print(zaznam)
            zaznamy.append(zaznam)

        for y in range(0, 5):
            zaznamy.append('')

        for x in range(0, 5):
            try:
                result = webServices.ukladanie.service.insert(team_id='033', team_password='P77N64',
                             Tests={'id': 0, 'name': 'testingInProgram', 'Author':'testUser', 'Peaks': vrch, 'Cities': mesto,
                                   'Q1': zaznamy[0],
                                   'Q2': zaznamy[1],
                                   'Q3': zaznamy[2],
                                   'Q4': zaznamy[3],
                                   'Q5': zaznamy[4],
                                    'status': status})
                nieco = 1
                print('preslo ukladanie vzdialenosti')
                break
            except Exception:
                print('nepodarilo sa ulozit test')
            time.sleep(1)

    def getTest():
        result = []
        schopneTesty = []
        preslo = 0
        otazky = []
        print('vypisujem nastavenia testu vo funkcii getTest:', test.status, ' ', test.hill, ' ', test.town)

        for x in range(0, 5):
            try:
                result = webServices.ukladanie.service.getAll()
                print('preslo nacitanie testov')
                preslo = 1
                break
            except Exception:
                print('nepodarilo sa nacitat test')
            time.sleep(1)

        if preslo == 0:

            return 1


        for x in result:
            if (x.status == 1):
                if (test.hill == '1' and x.Peaks == True and test.town == '1' and x.Cities  == True):
                        schopneTesty.append(x)
                elif (test.hill == '1' and x.Peaks == True and test.town == '0' and x.Cities  == False):
                        schopneTesty.append(x)
                elif (test.hill == '0' and x.Peaks == False and test.town == '1' and x.Cities == False):
                        schopneTesty.append(x)

        if len(schopneTesty) == 0:

            return 2

        a = random.randint(0, len(schopneTesty) -1)
        print('nahodne cislo je: ', a)

        otazka = schopneTesty[a].Q1.split('@')
        otazky.append(otazka)
        otazka = schopneTesty[a].Q2.split('@')
        otazky.append(otazka)
        if schopneTesty[a].Q3 != None:
            otazka = schopneTesty[a].Q3.split('@')
            otazky.append(otazka)
        if schopneTesty[a].Q4 != None:
            otazka = schopneTesty[a].Q4.split('@')
            otazky.append(otazka)
        if schopneTesty[a].Q5 != None:
            otazka = schopneTesty[a].Q5.split('@')
            otazky.append(otazka)

        print(otazky)
        testNaTestovanie = testFromDB(otazky)
        return 0