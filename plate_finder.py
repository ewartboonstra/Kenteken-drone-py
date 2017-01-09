from contour import contour
from contour import rectangle
import numpy as np
import cv2

class plate_finder:

    def __find_contours(self, image, thresh):
        contours = []

        #opencv functies die uit de mee gegeven afbeelding contouren en hun hierarchy haalt, zie SAD voor details
        #find contours returned een lijst met contouren, een contour is een lijst met punten.
        #find contours geeft ook een lijst met een hierarchy, een hierarchy is een lijst waarbij de index over een komt met het
        #bijbehorende contour in de hierarchy staan de previous(de vorige contour met de zelfde parrent), de next(het volgende contour met de zelfde parrent), de parrent(welk countour om de contour heen zit) en de child(wat is het eerste contour in ddeze contour)
        #all deze getallen verwijzen naar een index van dit desbetrevvende contour. wenneer een dergelijk veld leeg is is de waarde -1
        #structuur hierarchy: [Next, Previous, First_Child, Parent]
        src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        src = cv2.GaussianBlur(src, (5, 5), 0)
        maxValue = 255
        th, dst = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY);
        edges = cv2.Canny(dst, 0, 75, apertureSize=5)
        dst, conts, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        for index in xrange(0, len(conts)-1, 1):
            cont = contour(conts[index])
            j = hierarchy[0][index][2] #j is de index van de parrent
            if j > -1: #oftewel als er een parrent is
                cont.add_child(j)
                while hierarchy[0][j][0] > -1:#oftewel while er een next child is
                    j = hierarchy[0][j][2] #j is nu index van de volgende child
                    cont.add_child(j)
            contours.append(cont)
        return contours

    def __find_rectangles(self, contours):
        rectangles = []
        for cont in contours:
            cont_len = cv2.arcLength(cont.points, True)
            cont.points = cv2.approxPolyDP(cont.points, 0.02*cont_len, True)

            #isContourConvex kijkt of de contour geen zelf intersecties heeft
            #contourArea berekent het oppervlakte, deze moet groter dan 1000 om mogelijke ruis er uit te filteren
            if len(cont.points) == 4 and cv2.contourArea(cont.points) > 1000 and cv2.isContourConvex(cont.points):
                a_rectangle = rectangle(cont.points, cont.childeren)
                rectangles.append(a_rectangle)
        return rectangles

    def __find_plates(self, rectangles, contours):
        plates =  []
        plate_shaped = []
        for a_rectangle in rectangles:
            ratio1 = a_rectangle.side2/a_rectangle.side1
            ratio2 = a_rectangle.side4/a_rectangle.side3
            #check if ratio is licence plate like
            #between 3 and 8 is the ratio of a EU licenceplate
            #TODO maak van 3 en 8 configureer bare variabelen
            if (ratio1 >= 3.0 and ratio1 <= 8.0) and (ratio2 >= 3.0 and ratio2 <= 8.0):
                plate_shaped.append(a_rectangle)
        for plate in plate_shaped:
            is_plate = False
            for child in plate.childeren:
            #contourArea berekent het oppervlakte, deze moet groeter dan 1000 om mogelijke ruis er uit te filteren
            #TODO maak van het filteren van ruis een functie
                if cv2.contourArea(contours[child].points) > 1000:
                    is_plate = True
            if is_plate:
                plates.append(plate)

        return plates

    def __plate_sorter(self, plates):
        i = 1
        #simpele insertion sort die sorteert op de top_left point van een contour
        while i < len(plates):
            j = i
            while j > 0:
                if plates[j-1].points[0][0][0] > plates[j].points[0][0][0] or plates[j-1].points[0][0][1] > plates[j].points[0][0][1]:
                    temp = plates[j]
                    plates[j] = plates[j-1]
                    plates[j-1] = temp
                j = j - 1
            i = i + 1
        return plates

    def __plate_sqausher(self, plates):
        plates = self.__plate_sorter(plates)
        sqaushed = []
        i = 0
        j = 1
        top_left_x = 0
        top_left_y = 0
        width = 0
        heigth = 0
        #alle nummerborden zijn nu op locatie gesorteert, vergelijk nummerborden of ze erg op elkaar lijken en maak hier dan 1 nummerbord van
        #dmv de breete/hoogte van de hooste/breetste nummerbordt te nemen
        #[100,100][101,99][100,102][200,200][201,202] -> [101,102][201,202]
        while i < len(plates[0]):
            print i
            print j
            while i+j < len(plates[0]) and plates[0][i].is_alike(plates[0][i+j]):
                if plates[0][i+j].maxX > top_left_x:
                    top_left_x = plates[0][i+j].maxX
                if plates[0][i+j].maxY > top_left_y:
                    top_left_y = plates[0][i+j].maxY
                if plates[0][i+j].width > width:
                    width = plates[0][i+j].width
                if plates[0][i+j].heigth > heigth:
                    heigth = plates[0][i+j].heigth
                j = j + 1
            cords = [top_left_x, top_left_y, top_left_y+heigth, top_left_x+width]
            sqaushed.append(cords)
            top_left_x = 0
            top_left_y = 0
            width = 0
            heigth = 0
            i = i + j
            j = 0
        return sqaushed

    def angle_cos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

    def plate_ratio(self, p0, p1, p2, p3):
        len1 = abs(p0[0]-p3[0])
        len2 = abs(p0[1]-p1[1])
        return len1/len2

    def find_squares(self, img):
        img = cv2.GaussianBlur(img, (5, 5), 0)#blur the immage to reduse noice
        squares = []
        for gray in cv2.split(img):
            bin = cv2.Canny(gray, 0, 50, apertureSize=5)#Find edges using the canny edge detector alghorim
            bin = cv2.dilate(bin, None)#Dilation to "increase" the width of the edges for easier detection
            for thrs in xrange(25, 255, 25):
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)#Treshholding the image
                bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#finding contours
                for index, cnt in enumerate(contours):
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)#Simplefies contours using ramer douglas peucker algorithm
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):# check if the contour has 4 pints, the countour isnt so small its possibly noise, and see if the contour soesnt intersect with itself
                        cnt = cnt.reshape(-1, 2)#tranfrom the shape of the array from [a][0]][x/y] to [a][x/y]
                        max_cos = np.max([self.angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)]) #Calculate the angle of each corner
                        if max_cos < 0.1: #if its smaller then 0.1 its around 90 degrees
                            ratio = self.plate_ratio(cnt[0], cnt[1], cnt[2], cnt[3])
                            if ratio > 3 and ratio < 8: #ratio between left and bottom edge of a eu licence plate is between 3 and 8
                                child_count = 0
                                for index2, hier in enumerate(hierarchy[0]):
                                    if hier[3] == index and cv2.contourArea(contours[index2]) > 500:#find any childeren (possible letters) in a contour
                                        child_count = child_count + 1
                                if child_count > 0:
                                    squares.append(cnt)

        return squares


    def find_plate_coordinates(self, image):
        plates = []
        for thresh in xrange(15, 240, 15):
            contours = self.__find_contours(image, thresh)
            rectangles = self.__find_rectangles(contours)
            plates.append(self.__find_plates(rectangles, contours))

        #removing all empty indexes
        while plates.count([]):
            plates.remove([])
        plate_coordinates = self.__plate_sqausher(plates)
        print plate_coordinates
        return plates
