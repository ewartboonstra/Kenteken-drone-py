import cv2
import math

class contour:
    def __init__(self, points):
        self.points = points
        self.childeren = []

    def add_child(self, child):
        self.childeren.append(child)

    def is_alike(self, contour):
        #currently always returns false
        result = False
        #logic
        return result

class rectangle(contour):
    #points[0][0][0] x of point 1
    #points[0][0][1] y of point 1
    #points[1][0][0] x of point 2
    #points[1][0][1] y of point 2
    #points[2][0][0] x of point 3
    #points[2][0][1] y of point 3
    #points[3][0][0] x of point 4
    #points[3][0][1] y of point 4
    #points go counterclockwise starting with the top left one
    #1 is left
    #2 is bottom
    #3 is right
    #4 is top
    def __init__(self, points):
        contour.__init__(self, points)
        self.side1, self.side2, self.side3, self.side4 = self.__calculate_sides(self.points)

    def __init__(self, points, childeren):
        self.points = points
        self.childeren = childeren
        self.side1, self.side2, self.side3, self.side4 = self.__calculate_sides(self.points)
        self.maxX, self.maxY, self.minX, self.minY = self.__calculate_max_and_min(self.points)
        self.width = self.maxX - self.minX
        self.heigth = self.maxY - self.minY

    def __calculate_sides(self, points):
        #pythagoras om de lengte van de zijdes te berekenen
        side1 = abs(math.sqrt(math.pow((points[0][0][0] - points[1][0][0]), 2) + math.pow((points[0][0][1] - points[1][0][1]), 2)))
        side2 = abs(math.sqrt(math.pow((points[1][0][0] - points[2][0][0]), 2) + math.pow((points[1][0][1] - points[2][0][1]), 2)))
        side3 = abs(math.sqrt(math.pow((points[2][0][0] - points[3][0][0]), 2) + math.pow((points[2][0][1] - points[3][0][1]), 2)))
        side4 = abs(math.sqrt(math.pow((points[3][0][0] - points[0][0][0]), 2) + math.pow((points[3][0][1] - points[0][0][1]), 2)))
        return side1, side2, side3, side4

    def __calculate_max_and_min(self, points):
        #max en min van de bounding rectangle
        maxX = 0
        maxY = 0
        minX = 400000
        minY = 400000
        for point in points:
            if point[0][0] > maxX:
                maxX = point[0][0]
            if point[0][1] > maxY:
                maxY = point[0][1]
            if point[0][0] < minX:
                minX = point[0][0]
            if point[0][1] < minX:
                minX = point[0][1]

        return maxX, maxY, minX, minY

    def is_alike(self, rectangle):
        #TODO maak van het verschil percentage een variabel die kan worden mee gegeven
        result = False
        #kijken of er niet meer dan 10% verschil zit in hoogte/breedte/oppervlakte tussen de te vergelijken rectangles
        if self.heigth % rectangle.heigth < self.heigth/10.0 and width % rectangle.width < self.width/10.0 and cv2.contourourArea(self.points) % cv2.contourourArea(rectangle.points) < cv2.contourourArea(self.points)/10.0:
            result = True
        return result
