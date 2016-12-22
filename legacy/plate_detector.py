import numpy as np
import cv2
import copy
from myMath import myMath
from contour import contour
from contour import rectangle

class plate_detector:

    def __find_contours(self, img, thresh):
        #1
        src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 2
        src = cv2.GaussianBlur(src, (5, 5), 0)
        # Set threshold and maxValue
        #thresh = 200
        maxValue = 255

        # 3
        th, dst = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY);

        # 4
        edges = cv2.Canny(dst, 0, 75, apertureSize=5)

        # 5
        dst, conts, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = []
        print hierarchy[0]
        for x in xrange(0, len(conts), 1):
            a_contour = contour(conts[x], hierarchy[0][x][0], hierarchy[0][x][1], hierarchy[0][x][2], hierarchy[0][x][3])
            contours.append(a_contour)

        return contours

    def __find_rectangles(self, contours):
        mm = myMath()
        rectangles = []
        for cont in conours:
            cont_len = cv2.arcLength(cont.points, True)
            cont = cv2.approxPolyDP(cont.points, 0.02*cnt_len, True)
        # 7
            if len(cont.points) == 4 and cv2.contourArea(cont.points) > 1000 and cv2.isContourConvex(cont.points) and cv2.isContourConvex(cont.points):
                a_rectangle = rectangle(cont)
                rectangles.append(a_rectangle)

        plate_like_rectangles = []
        for rect in rectangles
            r = mm.ratio(get_side_1, get_side_2)
            r2 = mm.ratio(get_side_3, get_side_4)
            #check if ratio is licence plate like
            if (r > 3.0 and r < 8.0) and (r2 > 3.0 and r2 < 8.0):
                plate_like_rectangles.append(rect)
        return plate_like_rectangles

    def __find_plates(self, rectangles, contours):
        plates = []
        for cont in contours:
            #check if rectangle has other shapes inside it (posibly letters)
            if cont.parrent:
                #removing potential noice
                if cv2.contourArea(rect.points) > 1000:
                    plates.append(rect)
        return plates

        '''for square in rectangles:
            j = 0
            for hier in hierarchy[0]:
            #check if rectangle has other shapes inside it (posibly letters)
                if hier[3] == square[0]:
                    #removing potential noice
                    if cv2.contourArea(conts[j]) > 1000:
                        recs.append(square[1])
                j = j + 1'''

    def __sort_plates(self, plates):
        #uses the insertion sort(for development time reasons)
        i = 1
        while i < len(plates):
            j = i
            while j > 0:
                if plates[j-1][0][0][0] > plates[j][0][0][0]:
                    temp = plates[j]
                    plates[j] = plates[j-1]
                    plates[j-1] = temp
                j = j - 1
            i = i + 1
        return plates

    '''def __find_plates(self, recs):
        a = 0
        for rec in recs:
            if a > 0:
                c = np.concatenate((c, rec))
            else:
                c = rec
            a = a+1
        c = self.__sort_plates(c)

        c_copy = copy.deepcopy(c)
        a = 0
        for plate in c_copy:
            if a > 0:
                if plate[0][0][0] % last_plate[0][0][0] < 100:
                    last_plate = plate
                    c = np.delete(c, a)
            else:
                last_plate = plate
            a = a+1
        print c
        return c'''

    def start(self, img):
        plates = []
        for x in xrange(15, 240, 15):
            conts, hierarchy = self.__find_contours(img, x)
            rectangles = self.__find_rectangles(conts)
            recs = self.__find_plates(rectangles, conts)
            if recs != []:
                plates.append(recs)
        #plate_cords = self.__find_plates(plates)
        return plate_cords, plates
