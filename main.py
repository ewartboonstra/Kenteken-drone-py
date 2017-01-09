from plate_finder import plate_finder
import cv2

if __name__ == '__main__':
    plate_finder = plate_finder()
    from glob import glob
    for fn in glob('img/*.JPG'):
        img = cv2.imread(fn, cv2.IMREAD_COLOR)
        cords = plate_finder.find_squares(img)
        cv2.drawContours( img, cords, -1, (0, 255, 0), 3 )
        for cord in cords:
            print cord
            bounding  = cv2.boundingRect(cord)
            print bounding
            crop_img = img[bounding[1]:bounding[1]+bounding[3], bounding[0]:bounding[0]+bounding[2]]# Crop from x, y, w, h -> 100, 200, 300, 400
            # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
            cv2.namedWindow(fn, cv2.WINDOW_NORMAL)
            cv2.imshow(fn, crop_img)
            ch = 0xFF & cv2.waitKey()
            if ch == 27:
                break
    cv2.destroyAllWindows()
        #print cords
