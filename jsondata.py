# -*- coding: utf-8 -*-
import json
import base64
import time
import datetime


# convertToJson() methode neemt als argument filepath naar een afbeelding. Vervolgens wordt dit bestand omgezet in
# een base64 string, die samen met een timestamp en GPS coordinaten worden toegevoegd aan een json bestand.
# dit .json bestand wordt nu returned.

class Json(object):
    dateTimeNotation = '%Y-%m-%d %H:%M:%S'

    # deze notatie wordt gebruikt om een timestamp mee te geven.

    # Deze methode wordt gebruikt om een image naar base64 string om te zetten.
    # speciale methode voor convertToBase64 is een designkeuze. Eventueel later uitbreidbaar en 'with' statement
    # werkt als een try/catch statement.
    def convertToBase64(self, imagePath):  # convert image file naar base64 string
        with open(imagePath, "rb") as imageFile:
            string = base64.b64encode(imageFile.read())
            return string

    def convertToJson(self, imagePath):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime(self.dateTimeNotation)  # maakt een timestamp
        base64string = base64.b64encode(imagePath)
        pythonDictionary = {}  # dictionary aanmaken waar de data hieronder aan wordt toegevoegd.
        pythonDictionary['Picture'] = base64string
        pythonDictionary['Gps'] = "N 50.91721° E 5.91775°"  # dummydata
        pythonDictionary['Timestamp'] = st
        return json.dumps(pythonDictionary)
