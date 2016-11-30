from PIL import Image
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2

def distance_between_points(p1, p2):
    #c^2 = (xA - xB)^2 + (yA - yB)^2
    #c = root((xA - xB)^2 + (yA - yB)^2)
    return abs(math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2)))

def ratio(line1, line2):
    return line2 / line1

#finds all the contours and returns them with thier hieracrhy
def find_contours(img, thresh):
    #1
    src = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
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

    return conts, hierarchy

def find_squares(conts):
    squares = []
    current_index = 0
    for cnt in conts:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
    # 7
        if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt) and cv2.isContourConvex(cnt):
            #cnt[0][0][0] x of point 1
            #cnt[0][0][1] y of point 1
            #cnt[1][0][0] x of point 2
            #cnt[1][0][1] y of point 2
            #cnt[2][0][0] x of point 3
            #cnt[2][0][1] y of point 3
            #cnt[3][0][0] x of point 4
            #cnt[3][0][1] y of point 4
            #points go counterclockwise starting with the top left one
            #1 is left
            #2 is bottom
            #3 is right
            #4 is top
            len1 = distance_between_points(cnt[0][0],cnt[1][0])
            len2 = distance_between_points(cnt[1][0],cnt[2][0])
            len3 = distance_between_points(cnt[2][0],cnt[3][0])
            len4 = distance_between_points(cnt[3][0],cnt[1][0])
            #check if ratio is licence plate like
            if (ratio(len1, len2) > 3.0 and ratio(len1, len2) < 8.0) and (ratio(len3, len4) > 3.0 and ratio(len3, len4) < 8.0):
                square = current_index, cnt
                squares.append(square)
        current_index = current_index + 1
    return squares

def find_potential_plate(squares, hierarchy, conts):
    recs = []
    for square in squares:
        j = 0
        print square[1]
        for hier in hierarchy[0]:
        #check if rectangle has other shapes inside it (posibly letters)
            if hier[3] == square[0]:
                #removing potential noice
                if cv2.contourArea(conts[j]) > 1000:
                    recs.append(square[1])
            j = j + 1
    return recs

def find_rectangle(img, thresh):
    # 1
    conts, hierarchy = find_contours(img, thresh)
    squares = find_squares(conts)
    plates = find_potential_plate(squares, hierarchy, conts)
    return plates
    # 6


    '''
    Stappenplan herkennen rechthoek
    1 Convert from RGB to grayscale (cvCvtColor)
    2 Smooth (cvSmooth)
    3 Threshold (cvThreshold)
    4 Detect edges (cvCanny)
    5 Find contours (cvFindContours)
    6 Approximate contours with linear features (cvApproxPoly)
    7 Find "rectangles" which were structures that: had polygonalized contours possessing 4 points, were of sufficient area, had adjacent edges were ~90 degrees, had distance between "opposite" vertices was of sufficient size, etc.
    '''

def show_img():
    from glob import glob
    for fn in glob('/home/vincent/Documents/wh/jaar 3/deze drone is wel goed/img/*.JPG'):
        plates = []
        for x in xrange(15, 240, 15):
            plates.append(find_rectangle(fn, x))
        img = cv2.imread(fn, cv2.IMREAD_COLOR)
        for plate in plates:
            cv2.drawContours(img, plate, -1, (255, 0, 255), 6 )
        cv2.namedWindow('squares', cv2.WINDOW_NORMAL)
        cv2.imshow('squares', img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyWindow('squares')

if __name__ == '__main__':
    show_img()
