from zeep import Client
from zeep.transports import Transport
from model.geographic_point import geographic_point
from model.test import test
from model.question import question
import time

class webServices():
    mesta = None
    vrchy = None
    vzdialenost = None

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
                print('chyba mesta')
                time.sleep(1)

        nieco = 0
        while nieco == 0:
            try:
                webServices.vrchy = Client('http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Peaks?WSDL',transport=transport)
                nieco = 1
                print('nastavene WSDL vrchy')
                break
            except Exception:
                print('chyba vrchy')
                time.sleep(1)

        nieco = 0
        while nieco == 0:
            try:
                webServices.vzdialenost = Client('http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Locations?WSDL',transport=transport)
                nieco = 1
                print('nastavene WSDL vzdialenosti')
                break
            except Exception:
                print('chyba vzdialenosti')
                time.sleep(1)

    def setGP(nazov, typ, hint):
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
                lat1 = result[0].coord_lat
                lon1 = result[0].coord_lon
                pointA = geographic_point(nazov, typ, hint, lat1, lon1)
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
                lat1 = result[0].coord_lat
                lon1 = result[0].coord_lon
                pointA = geographic_point(nazov, typ, hint, lat1, lon1)
            else:
                print('Nepodarilo sa zistit vrchol.')
                return nazov

        return pointA

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
