from plate_finder import plate_finder
import cv2

if __name__ == '__main__':
    plate_finder = plate_finder()
    from glob import glob
    for fn in glob('img/*.JPG'):
        img = cv2.imread(fn, cv2.IMREAD_COLOR)
        cords = plate_finder.find_plate_coordinates(img)
        #print cords
