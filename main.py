from PIL import Image
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2

def find_rectangle(img, thresh):
    # 1
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
    dst, conts, hierarchy = cv2.findContours(dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 6
    recs = []
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
            dif1x = cnt[0][0][0] - cnt[1][0][0]
            dif1y = cnt[0][0][1] - cnt[1][0][1]
            dif2x = cnt[0][0][0] - cnt[3][0][0]
            dif2y = cnt[0][0][1] - cnt[3][0][1]
            len1 = math.sqrt(math.pow(dif1x, 2) + math.pow(dif1y, 2))
            len2 = math.sqrt(math.pow(dif2x, 2) + math.pow(dif2y, 2))
            if len1 < len2:
                print len1
                print len2
                recs.append(cnt)

    return src, dst, conts, recs

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
    for fn in glob('/home/vincent/Documents/wh/jaar 3/drone/img/*.png'):
        for x in xrange(0, 255, 15):
            src, dst, conts, recs = find_rectangle(fn, x)
            img = cv2.imread(fn, cv2.IMREAD_COLOR)
            cv2.drawContours(img, recs, -1, (255, 0, 255), 1 )
            cv2.imshow('squares', img)
            ch = 0xFF & cv2.waitKey()
            if ch == 27:
                break
        cv2.destroyWindow('squares')

if __name__ == '__main__':
    show_img()
